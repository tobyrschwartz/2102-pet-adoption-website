# Pet Adoption API Contract

This document outlines the API contract for our pet adoption application. It describes all available endpoints, their input parameters, and expected responses.

## Authentication

### Login

- **Method**: POST
- **Path**: `/login`
- **Input**: 
  - `email` (string): User's email address
  - `password` (string): User's password
- **Output**:
  - `message` (string): Success or error message
  - `user_id` (integer): ID of the authenticated user (if successful)
  - `role` (integer): Role of the authenticated user (if successful)
- **Status Codes**:
  - 200: Success
  - 401: Authentication failed

### Logout

- **Method**: GET
- **Path**: `/logout`
- **Input**: None
- **Output**:
  - `message` (string): Logout confirmation message
- **Status Codes**:
  - 200: Success

## Users

### List All Users

- **Method**: GET
- **Path**: `/api/users`
- **Input**: None
- **Output**:
  - Array of user objects, each containing:
    - `user_id` (integer): Unique identifier for the user
    - `email` (string): User's email address
    - `full_name` (string): User's full name
    - `phone` (string): User's phone number
    - `role` (integer): User's role in the system
- **Status Codes**:
  - 200: Success
  - 401: Not authenticated
  - 403: Not authorized (requires ADMIN role)

### Create User

- **Method**: POST
- **Path**: `/api/users`
- **Input**:
  - `email` (string): User's email address
  - `password_hash` (string): Hash of the user's password
  - `full_name` (string): User's full name
  - `phone` (string): User's phone number
  - `role` (integer, optional): User's role in the system (defaults to USER)
- **Output**:
  - `user_id` (integer): Unique identifier for the created user
  - `email` (string): User's email address
  - `password_hash` (string): Hash of the user's password
  - `full_name` (string): User's full name
  - `phone` (string): User's phone number
  - `role` (integer): User's role in the system
- **Status Codes**:
  - 201: Created
  - 401: Not authenticated
  - 403: Not authorized (requires ADMIN role)

### Get User Details

- **Method**: GET
- **Path**: `/api/users/{user_id}`
- **Input**:
  - `user_id` (integer): ID of the user to retrieve
- **Output**:
  - `user_id` (integer): Unique identifier for the user
  - `email` (string): User's email address
  - `full_name` (string): User's full name
  - `phone` (string): User's phone number
  - `role` (integer): User's role in the system
- **Status Codes**:
  - 200: Success
  - 401: Not authenticated
  - 403: Not authorized (requires at least USER role)
  - 404: User not found

## Pets

### List All Pets

- **Method**: GET
- **Path**: `/api/pets`
- **Input**: None
- **Output**:
  - Array of pet objects, each containing:
    - `pet_id` (integer): Unique identifier for the pet
    - `name` (string): Pet's name
    - `species` (string): Pet's species (e.g., Dog, Cat)
    - `breed` (string): Pet's breed
    - `age` (integer): Pet's age in years
    - `description` (string): Description of the pet
    - `status` (string): Pet's adoption status
    - `image_url` (string): URL to the pet's image
- **Status Codes**:
  - 200: Success

### Search Pets

- **Method**: GET
- **Path**: `/api/pets`
- **Input** (query parameters):
  - `species` (string, optional): Filter by pet species
  - `breed` (string, optional): Filter by pet breed
  - `status` (string, optional): Filter by adoption status
- **Output**:
  - Array of pet objects matching the search criteria
- **Status Codes**:
  - 200: Success

### Create Pet

- **Method**: POST
- **Path**: `/api/pets`
- **Input**:
  - `name` (string): Pet's name
  - `species` (string): Pet's species (e.g., Dog, Cat)
  - `breed` (string): Pet's breed
  - `age` (integer): Pet's age in years
  - `description` (string): Description of the pet
  - `image_url` (string, optional): URL to the pet's image
- **Output**:
  - `pet_id` (integer): Unique identifier for the created pet
  - `name` (string): Pet's name
  - `species` (string): Pet's species
  - `breed` (string): Pet's breed
  - `age` (integer): Pet's age
  - `description` (string): Description of the pet
  - `status` (string): Pet's adoption status (default: "Available")
  - `image_url` (string): URL to the pet's image
- **Status Codes**:
  - 201: Created
  - 401: Not authenticated
  - 403: Not authorized (requires STAFF role)

### Get Pet Details

- **Method**: GET
- **Path**: `/api/pets/{pet_id}`
- **Input**:
  - `pet_id` (integer): ID of the pet to retrieve
- **Output**:
  - `pet_id` (integer): Unique identifier for the pet
  - `name` (string): Pet's name
  - `species` (string): Pet's species
  - `breed` (string): Pet's breed
  - `age` (integer): Pet's age
  - `description` (string): Description of the pet
  - `status` (string): Pet's adoption status
  - `image_url` (string): URL to the pet's image
- **Status Codes**:
  - 200: Success
  - 404: Pet not found

### Update Pet

- **Method**: PUT
- **Path**: `/api/pets/{pet_id}`
- **Input**:
  - `pet_id` (integer): ID of the pet to update
  - `name` (string, optional): Pet's name
  - `species` (string, optional): Pet's species
  - `breed` (string, optional): Pet's breed
  - `age` (integer, optional): Pet's age
  - `description` (string, optional): Description of the pet
  - `status` (string, optional): Pet's adoption status
  - `image_url` (string, optional): URL to the pet's image
- **Output**:
  - Updated pet object
- **Status Codes**:
  - 200: Success
  - 401: Not authenticated
  - 403: Not authorized (requires STAFF role)
  - 404: Pet not found

### Delete Pet

- **Method**: DELETE
- **Path**: `/api/pets/{pet_id}`
- **Input**:
  - `pet_id` (integer): ID of the pet to delete
- **Output**:
  - `message` (string): Success message
  - `pet_id` (integer): ID of the deleted pet
- **Status Codes**:
  - 200: Success
  - 401: Not authenticated
  - 403: Not authorized (requires STAFF role)
  - 404: Pet not found

## Applications

### List User Applications

- **Method**: GET
- **Path**: `/api/applications`
- **Input**: None (uses authenticated user's ID)
- **Output**:
  - Array of application objects for the current user
- **Status Codes**:
  - 200: Success
  - 401: Not authenticated

### List Applications by Status

- **Method**: GET
- **Path**: `/api/applications?status={status}`
- **Input**:
  - `status` (string): Application status to filter by
- **Output**:
  - Array of application objects matching the status
- **Status Codes**:
  - 200: Success
  - 401: Not authenticated
  - 403: Not authorized (requires STAFF role)

### Create Application

- **Method**: POST
- **Path**: `/api/applications`
- **Input**:
  - `pet_id` (integer): ID of the pet being applied for
  - `application_data` (object): Additional application information
    - `housing_type` (string): Type of housing
    - `has_yard` (boolean): Whether the applicant has a yard
    - `previous_experience` (boolean): Whether the applicant has previous pet experience
- **Output**:
  - `application_id` (integer): Unique identifier for the created application
  - `user_id` (integer): ID of the user who submitted the application
  - `pet_id` (integer): ID of the pet being applied for
  - `submit_date` (string): Date the application was submitted
  - `status` (string): Application status (default: "Pending")
  - `reviewer_id` (integer|null): ID of the staff member who reviewed the application
  - `review_date` (string|null): Date the application was reviewed
  - `application_data` (object): Additional application information
- **Status Codes**:
  - 201: Created
  - 401: Not authenticated
  - 403: Not authorized (requires USER role)

### Get Application Details

- **Method**: GET
- **Path**: `/api/applications/{application_id}`
- **Input**:
  - `application_id` (integer): ID of the application to retrieve
- **Output**:
  - `application_id` (integer): Unique identifier for the application
  - `user_id` (integer): ID of the user who submitted the application
  - `pet_id` (integer): ID of the pet being applied for
  - `submit_date` (string): Date the application was submitted
  - `status` (string): Application status
  - `reviewer_id` (integer|null): ID of the staff member who reviewed the application
  - `review_date` (string|null): Date the application was reviewed
  - `application_data` (object): Additional application information
- **Status Codes**:
  - 200: Success
  - 401: Not authenticated
  - 404: Application not found

### Update Application Status

- **Method**: PUT
- **Path**: `/api/applications/{application_id}`
- **Input**:
  - `application_id` (integer): ID of the application to update
  - `status` (string): New application status ("Approved" or "Rejected")
- **Output**:
  - `application_id` (integer): Unique identifier for the application
  - `status` (string): Updated application status
  - `reviewer_id` (integer): ID of the staff member who updated the status
  - `review_date` (string): Date the application was reviewed
- **Status Codes**:
  - 200: Success
  - 401: Not authenticated
  - 403: Not authorized (requires STAFF role)
  - 404: Application not found