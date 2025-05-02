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


def create_application(user_id: int, pet_id: int):
    """
    Create a new adoption application for a pet.
    
    :param user_id: ID of the user submitting the application
    :param pet_id: ID of the pet being applied for
    :param application_data: Additional application data (housing info, experience, etc.)
    :return: JSON response with the created application details
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    if pet_id is None:
        conn.close()
        return jsonify({"error": "Pet ID cannot be null"}), 400

    cursor.execute('''
        INSERT INTO applications (user_id, pet_id, status)
        VALUES (?, ?, ?)
    ''', (user_id, pet_id, ApplicationStatus.PENDING))
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
    conn.close()
    if application is None:
        return jsonify({"error": "Application not found"}), 404
    application = dict(application)
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

    cursor.execute('SELECT * FROM applications WHERE application_id = ?', (application_id,))
    app_row = cursor.fetchone()
    if not app_row:
        conn.close()
        return jsonify({"error": "Application not found"}), 404

    application = dict(app_row)

    cursor.execute('''
        SELECT qr.question_id, q.question_text AS question_text, qr.answer_text 
        FROM questionnaire_responses qr
        JOIN questions q ON qr.question_id = q.question_id
        WHERE qr.user_id = ?
    ''', (application['user_id'],))
    responses = [dict(row) for row in cursor.fetchall()]
    conn.close()

    return jsonify({
        "application": application,
        "responses": responses
    }), 200

def get_all_applications():
    """
    Retrieve all applications in the system.
    :return: JSON response with a list of all applications
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT 
            a.application_id as id,
            a.application_id,
            a.user_id as applicantId,
            u.full_name as applicantName,
            a.status,
            a.pet_id,
            a.submitted_at,
            a.updated_at,
            a.reviewed_at,
            a.reviewer_id
        FROM applications a
        JOIN users u ON a.user_id = u.user_id
    ''')
    applications = cursor.fetchall()
    conn.close()
    if not applications:
        return jsonify([]), 200
    applications = [dict(row) for row in applications]
    for app in applications:
        app['status'] = ApplicationStatus(app['status']).name
    return jsonify(applications), 200


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

def get_applications_by_pet(pet_id: int):
    """
    Retrieve applications for a specific pet.

    :param pet_id: ID of the pet whose applications to retrieve
    :return: JSON response with a list of applications for the pet
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM applications WHERE pet_id = ?
    ''', (pet_id,))
    applications = cursor.fetchall()
    conn.close()

    applications = [dict(row) for row in applications]
    if not applications:
        return jsonify({"error": "No applications found for this pet"}), 404
    for application in applications:
        application['status'] = ApplicationStatus(application['status']).name
    return jsonify(applications), 200

def get_application_count():
    """
    Retrieve the total number of applications in the system.

    :return: JSON response with the count of applications
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) FROM applications
    ''')
    count = cursor.fetchone()[0]
    conn.close()
    return jsonify({"application_count": count}), 200

def get_application_count_by_status(status: ApplicationStatus):
    """
    Retrieve the count of applications by their status.
    :param status: Status of the applications to count
    :return: JSON response with the count of applications matching the status
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT COUNT(*) FROM applications WHERE status = ?
    ''', (status,))
    count = cursor.fetchone()[0]
    conn.close()
    return jsonify({"application_count": count}), 200

def get_application_status(status: str):
    """
    Convert a string status to the corresponding ApplicationStatus enum.
    :param status: String representation of the application status
    :return: ApplicationStatus enum value
    """
    try:
        return ApplicationStatus[status.upper()]
    except KeyError:
        return None
