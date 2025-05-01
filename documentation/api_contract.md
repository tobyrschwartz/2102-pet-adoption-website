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
  - 400: Invalid data  
  - 401: Authentication failed  

### Logout

- **Method**: POST  
- **Path**: `/logout`  
- **Input**: None  
- **Output**:  
  - `message` (string): Logout confirmation message  
- **Status Codes**:  
  - 200: Success  

### Register User

- **Method**: POST  
- **Path**: `/register`  
- **Input**:  
  - `email` (string): User's email address  
  - `password` (string): Plain-text password  
  - `full_name` (string): User's full name  
  - `phone` (string): User's phone number  
  - `role` (integer, optional): Role in the system (default: USER)  
- **Output**:  
  - `user_id` (integer): ID of the created user  
- **Status Codes**:  
  - 201: Created  
  - 400: Invalid or missing data  

## Users

### List All Users

- **Method**: GET  
- **Path**: `/api/users`  
- **Input**: None  
- **Output**:  
  - Array of user objects:  
    - `user_id` (integer)  
    - `email` (string)  
    - `full_name` (string)  
    - `phone` (string)  
    - `role` (integer)  
- **Status Codes**:  
  - 200: Success  
  - 401: Not authenticated  
  - 403: Not authorized (requires ADMIN role)  

### Create User

- **Method**: POST  
- **Path**: `/api/users`  
- **Input**:  
  - `email` (string)  
  - `password_hash` (string)  
  - `full_name` (string)  
  - `phone` (string)  
  - `role` (integer, optional)  
- **Output**:  
  - Same as input plus `user_id`  
- **Status Codes**:  
  - 201: Created  
  - 401: Not authenticated  
  - 403: Not authorized (requires ADMIN role)  

### Get User Details

- **Method**: GET  
- **Path**: `/api/users/{user_id}`  
- **Input**:  
  - `user_id` (integer)  
- **Output**:  
  - User object as above  
- **Status Codes**:  
  - 200: Success  
  - 401: Not authenticated  
  - 403: Not authorized (requires STAFF role)  
  - 404: User not found  

## Pets

### List All Pets / Search Pets

- **Method**: GET  
- **Path**: `/api/pets`  
- **Input** (optional query parameters):  
  - `species` (string)  
  - `breed` (string)  
  - `status` (string)  
- **Output**:  
  - Array of pet objects  
- **Status Codes**:  
  - 200: Success  

### Create Pet

- **Method**: POST  
- **Path**: `/api/pets`  
- **Input**:  
  - `name` (string)  
  - `species` (string)  
  - `breed` (string)  
  - `age` (integer)  
  - `description` (string)  
  - `image_url` (string, optional)  
- **Output**:  
  - Pet object including `pet_id` and default status `"Available"`  
- **Status Codes**:  
  - 201: Created  
  - 401: Not authenticated  
  - 403: Not authorized (requires STAFF role)  

### Get Pet Details

- **Method**: GET  
- **Path**: `/api/pets/{pet_id}`  
- **Input**:  
  - `pet_id` (integer)  
- **Output**:  
  - Pet object  
- **Status Codes**:  
  - 200: Success  
  - 404: Pet not found  

### Update Pet

- **Method**: PUT  
- **Path**: `/api/pets/{pet_id}`  
- **Input**:  
  - Partial or full pet object  
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
  - `pet_id` (integer)  
- **Output**:  
  - `message` (string)  
  - `pet_id` (integer)  
- **Status Codes**:  
  - 200: Success  
  - 401: Not authenticated  
  - 403: Not authorized (requires STAFF role)  
  - 404: Pet not found  

### Update Pet Status

- **Method**: PUT  
- **Path**: `/api/pets/{pet_id}/status`  
- **Input**:  
  - `status` (string)  
- **Output**:  
  - Updated pet object  
- **Status Codes**:  
  - 200: Success  
  - 400: Invalid data  
  - 401: Not authenticated  
  - 403: Not authorized (requires STAFF role)  
  - 404: Pet not found  

### Get All Species

- **Method**: GET  
- **Path**: `/api/pets/species`  
- **Output**:  
  - Array of species (string)  
- **Status Codes**:  
  - 200: Success  

### Get All Breeds

- **Method**: GET  
- **Path**: `/api/pets/breeds`  
- **Output**:  
  - Array of breeds (string)  
- **Status Codes**:  
  - 200: Success  

## Applications

### List Applications

- **Method**: GET  
- **Path**: `/api/applications`  
- **Input** (optional query param):  
  - `status` (string)  
- **Output**:  
  - Applications (filtered or user-specific)  
- **Status Codes**:  
  - 200: Success  
  - 401: Not authenticated  
  - 403: Not authorized (STAFF if using status param)  

### Create Application

- **Method**: POST  
- **Path**: `/api/applications`  
- **Input**:  
  - `pet_id` (integer)  
  - `application_data` (object)  
    - `housing_type` (string)  
    - `has_yard` (boolean)  
    - `previous_experience` (boolean)  
- **Output**:  
  - Application object  
- **Status Codes**:  
  - 201: Created  
  - 401: Not authenticated  
  - 403: Not authorized (requires USER role)  

### Get Application Details

- **Method**: GET  
- **Path**: `/api/applications/{application_id}`  
- **Output**:  
  - Application object  
- **Status Codes**:  
  - 200: Success  
  - 401: Not authenticated  
  - 404: Not found  

### Update Application Status

- **Method**: PUT  
- **Path**: `/api/applications/{application_id}`  
- **Input**:  
  - `status` (string): `"Approved"` or `"Rejected"`  
- **Output**:  
  - Updated application status  
- **Status Codes**:  
  - 200: Success  
  - 401: Not authenticated  
  - 403: Not authorized (requires STAFF role)  
  - 404: Not found  

### Get Application Count

- **Method**: GET  
- **Path**: `/api/applications/count`  
- **Input**:  
  - `status` (string, optional)  
- **Output**:  
  - Count (integer)  
- **Status Codes**:  
  - 200: Success  
  - 403: Not authorized (requires STAFF role)  

## Questionnaires

### Get Questionnaire

- **Method**: GET  
- **Path**: `/api/questionnaires`  
- **Output**:  
  - Array of questions  
- **Status Codes**:  
  - 200: Success  

### Submit Questionnaire Answers

- **Method**: POST  
- **Path**: `/api/questionnaires/submit`  
- **Input**:  
  - `answers` (object)  
- **Output**:  
  - Confirmation message  
- **Status Codes**:  
  - 200: Success  
  - 400: Invalid data  
  - 401: Not authenticated  

### Get Questionnaire by User ID

- **Method**: GET  
- **Path**: `/api/questionnaires/{user_id}`  
- **Status Codes**:  
  - 200: Success  
  - 403: Forbidden  

### Check for Open Questionnaire

- **Method**: GET  
- **Path**: `/api/questionnaires/hasOpen`  
- **Input**:  
  - `user_id` (optional query param)  
- **Output**:  
  - Boolean  
- **Status Codes**:  
  - 200: Success  
  - 403: Forbidden  

### Review Questionnaires

- **Method**: GET  
- **Path**: `/api/questionnaires/review`  
- **Output**:  
  - Array of unreviewed questionnaires  
- **Status Codes**:  
  - 200: Success  
  - 403: Not authorized (requires STAFF role)  

### Approve Questionnaire

- **Method**: POST  
- **Path**: `/api/users/{user_id}/approve`  
- **Output**:  
  - Confirmation message  
- **Status Codes**:  
  - 200: Success  
  - 403: Not authorized (requires STAFF role)  
