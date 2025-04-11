"""The module for handling pet adoption applications."""
from flask import jsonify
from enums import ApplicationStatus

def create_application(user_id: int, pet_id: int, application_data: dict):
    """
    Create a new adoption application for a pet.
    
    :param user_id: ID of the user submitting the application
    :param pet_id: ID of the pet being applied for
    :param application_data: Additional application data (housing info, experience, etc.)
    :return: JSON response with the created application details
    """
    # This is a mock function
    new_application = {
        "application_id": 1,
        "user_id": user_id,
        "pet_id": pet_id,
        "submit_date": "2025-04-11",
        "status": ApplicationStatus.PENDING,
        "reviewer_id": None,
        "review_date": None,
        "application_data": application_data
    }
    return jsonify(new_application), 201

def get_application(application_id: int):
    """
    Retrieve a specific application by its ID.

    :param application_id: ID of the application to retrieve
    :return: JSON response with the application details
    """
    # This is a mock function
    application = {
        "application_id": application_id,
        "user_id": 1,
        "pet_id": 1,
        "submit_date": "2025-04-01",
        "status": ApplicationStatus.PENDING,
        "reviewer_id": None,
        "review_date": None,
        "application_data": {
            "housing_type": "Apartment",
            "has_yard": False,
            "previous_experience": True
        }
    }
    return jsonify(application), 200

def update_application_status(application_id: int, status: ApplicationStatus, reviewer_id: int):
    """
    Update the status of an application.

    :param application_id: ID of the application to update
    :param status: New status for the application
    :param reviewer_id: ID of the staff member reviewing the application
    :return: JSON response with the updated application details
    """
    # This is a mock function
    updated_application = {
        "application_id": application_id,
        "status": status,
        "reviewer_id": reviewer_id,
        "review_date": "2025-04-11"
    }
    return jsonify(updated_application), 200

def get_user_applications(user_id: int):
    """
    Retrieve all applications submitted by a specific user.

    :param user_id: ID of the user whose applications to retrieve
    :return: JSON response with a list of the user's applications
    """
    # This is a mock function
    applications = [
        {
            "application_id": 1,
            "user_id": user_id,
            "pet_id": 1,
            "submit_date": "2025-04-07",
            "status": ApplicationStatus.PENDING,
            "reviewer_id": None,
            "review_date": None
        },
        {
            "application_id": 2,
            "user_id": user_id,
            "pet_id": 2,
            "submit_date": "2025-04-01",
            "status": ApplicationStatus.APPROVED,
            "reviewer_id": 3,
            "review_date": "2025-04-07"
        }
    ]
    return jsonify(applications), 200

def get_applications_by_status(status: ApplicationStatus):
    """
    Retrieve applications by their status.

    :param status: Status of the applications to retrieve
    :return: JSON response with a list of applications matching the status
    """
    # This is a mock function
    applications = [
        {
            "application_id": 1,
            "user_id": 1,
            "pet_id": 1,
            "submit_date": "2025-04-07",
            "status": status,
            "reviewer_id": None,
            "review_date": None
        }
    ]
    return jsonify(applications), 200
