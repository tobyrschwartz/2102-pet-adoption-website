"""The module for handling pet adoption applications."""
import sqlite3
from flask import jsonify
from enums import ApplicationStatus
from mock_data import get_mock_application, get_mock_application_list

def get_db_connection():
    """
    Create a database connection to the SQLite database.
    :return: SQLite connection object
    """
    conn = sqlite3.connect('petadoption.db')
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

# @ future us: we need to refactor this class to follow the ER diagram we created
def create_application(user_id: int, pet_id: int, application_data: dict):
    """
    Create a new adoption application for a pet.
    
    :param user_id: ID of the user submitting the application
    :param pet_id: ID of the pet being applied for
    :param application_data: Additional application data (housing info, experience, etc.)
    :return: JSON response with the created application details
    """
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
    application = get_mock_application(application_id)
    # Add application_data for this specific endpoint
    application["application_data"] = {
        "housing_type": "Apartment",
        "has_yard": False,
        "previous_experience": True
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
    applications = get_mock_application_list(user_id)
    return jsonify(applications), 200

def get_applications_by_status(status: ApplicationStatus):
    """
    Retrieve applications by their status.

    :param status: Status of the applications to retrieve
    :return: JSON response with a list of applications matching the status
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM applications WHERE status = ?
    ''', (status,))
    applications = cursor.fetchall()
    conn.close()

    applications = [dict(row) for row in applications]
    return jsonify(applications), 200
