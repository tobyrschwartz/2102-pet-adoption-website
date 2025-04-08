from flask import jsonify
from enums import ApplicationStatus, PetStatus#, Role i'll implement role stuff later



def create_pet(name: str, species: str, breed: str, age: int, size, status: PetStatus): # **this is a mock function**
    """
    Create a new pet with the given details.
    
    :param name: Name of the pet
    :param species: Species of the pet (e.g., Dog, Cat)
    :param breed: Breed of the pet
    :param age: Age of the pet in years
    :param size: Size of the pet (e.g., Small, Medium, Large)
    :param status: Adoption status of the pet (e.g., Available, Adopted)
    :return: JSON response with the created pet details
    """

    new_pet = {
        "name": name,
        "species": species,
        "breed": breed,
        "age": age,
        "size": size,
        "status": status
    }
    return jsonify(new_pet), 201

def get_applications(): # **this is a mock function**
    """
    Retrieve all applications.
    
    :return: JSON response with a list of applications
    """
    applications = [
        {
        "application_id": 1,
        "user_id": "user",
        "pet_id": 1,
        "submit_date": "2025-04-07",
        "status": "Pending",
        "reviewer_id": "",
        "review_date": ""
        },
        {
        "application_id": 2,
        "user_id": "adopter",
        "pet_id": 2,
        "submit_date": "2025-04-01",
        "status": "Approved",
        "reviewer_id": "admin",
        "review_date": "2025-04-07"
        }
    ]
    return jsonify(applications), 200

def get_application(application_id): # **this is a mock function**
    """
    Retrieve a specific application by its ID.

    :param application_id: ID of the application to retrieve
    :return: JSON response with the application details
    """
    application = {
        "application_id": application_id,
        "user_id": "user",
        "pet_id": 1,
        "submit_date": "2025-04-01",
        "status": "Approved",
        "reviewer_id": "admin",
        "review_date": "2025-04-07"
    }
    return jsonify(application), 200

def update_application(application_id, status: ApplicationStatus): # **this is a mock function**
    """
    Update the status of an application.

    :param application_id: ID of the application to update
    :param status: New status for the application
    :return: JSON response with the updated application details
    """
    updated_application = {
        "application_id": application_id,
        "status": status
    }
    # logic for the notification system would go here
    return jsonify(updated_application), 200

def get_application_by_status(status: ApplicationStatus): # **this is a mock function**
    """
    Retrieve applications by their status.

    :param status: Status of the applications to retrieve
    :return: JSON response with a list of applications matching the status
    """
    applications = [
        {
        "application_id": 1,
        "user_id": "user",
        "pet_id": 1,
        "submit_date": "2025-04-07",
        "status": status,
        "reviewer_id": "",
        "review_date": ""
        }
    ]
    return jsonify(applications), 200
