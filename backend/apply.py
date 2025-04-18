"""The module for handling pet adoption applications."""
import sqlite3
from flask import jsonify
from enums import ApplicationStatus

def get_db_connection():
    """
    Create a database connection to the SQLite database.
    :return: SQLite connection object
    """
    conn = sqlite3.connect('petadoption.db')
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn


def create_application(user_id: int, pet_id: int, application_data: dict):
    """
    Create a new adoption application for a pet.
    
    :param user_id: ID of the user submitting the application
    :param pet_id: ID of the pet being applied for
    :param application_data: Additional application data (housing info, experience, etc.)
    :return: JSON response with the created application details
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO applications (user_id, pet_id, status)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, pet_id,  ApplicationStatus.PENDING))

    application_id = cursor.lastrowid
    for question_id, answer_text in application_data.items():
        cursor.execute('''
            INSERT INTO questionaire_responses (application_id, question_id, answer_text)
            VALUES (?, ?, ?)
        ''', (application_id, question_id, answer_text))
    conn.commit()
    conn.close()
    return jsonify("Application created successfully."), 201

def get_application_full(application_id: int):
    """
    Retrieve a specific application by its ID.

    :param application_id: ID of the application to retrieve
    :return: JSON response with the application details
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM applications WHERE application_id = ?
    ''', (application_id,))
    application = cursor.fetchone()
    cursor.execute('''
        SELECT * FROM questionaire_responses WHERE application_id = ?
    ''', (application_id,))
    responses = cursor.fetchall()
    conn.close()
    if application is None:
        return jsonify({"error": "Application not found"}), 404
    application = dict(application)
    application['responses'] = [dict(response) for response in responses]
    application['status'] = ApplicationStatus(application['status']).name
    return jsonify(application), 200

def get_application(application_id: int):
    """
    Retrieve a specific application by its ID.

    :param application_id: ID of the application to retrieve
    :return: JSON response with the application details
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM applications WHERE application_id = ?
    ''', (application_id,))
    application = cursor.fetchone()
    conn.close()
    if application is None:
        return jsonify({"error": "Application not found"}), 404
    application = dict(application)
    application['status'] = ApplicationStatus(application['status']).name
    return jsonify(application), 200

def update_application_status(application_id: int, status: ApplicationStatus, reviewer_id: int):
    """
    Update the status of an application.

    :param application_id: ID of the application to update
    :param status: New status for the application
    :param reviewer_id: ID of the staff member reviewing the application
    :return: JSON response with the updated application details
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE applications
        SET status = ?, reviewed_at = CURRENT_TIMESTAMP, reviewer_id = ?
        WHERE application_id = ?
    ''', (status, reviewer_id, application_id))
    conn.commit()
    conn.close()
    if cursor.rowcount == 0:
        return jsonify({"error": "Application not found"}), 404
    return jsonify("Application updated successfully."), 200

def get_user_applications(user_id: int):
    """
    Retrieve all applications submitted by a specific user.

    :param user_id: ID of the user whose applications to retrieve
    :return: JSON response with a list of the user's applications
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM applications WHERE user_id = ?
    ''', (user_id,))
    applications = cursor.fetchall()
    conn.close()
    if not applications:
        return jsonify({"error": "No applications found for this user"}), 404
    applications = [dict(application) for application in applications]
    for application in applications:
        application['status'] = ApplicationStatus(application['status']).name
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
    if not applications:
        return jsonify({"error": "No applications found with this status"}), 404
    for application in applications:
        application['status'] = ApplicationStatus(application['status']).name
    return jsonify(applications), 200
