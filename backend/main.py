"""Main module of the application"""
from sys import argv
import sqlite3
import bcrypt
from flask_cors import CORS
from flask import Flask, request, session, jsonify
from flasgger import Swagger
from user import (get_user_by_id_internal, login, get_user_role, logout, create_user,
                 get_all_users, get_user_by_id)
from pets import (get_all_pets, get_pet, create_pet as create_pet_handler,
                 update_pet, delete_pet, search_pets, update_pet_status,
                 get_species, get_breeds)
from apply import (create_application, get_application, update_application_status,
                   get_applications_by_status, get_all_applications)
from questionnaire import (approve_questionnaire, get_answered_questionnaire,
                           get_open_questionnaires,set_questionnaire,
                           get_number_of_open_questionnaires,
                           get_questionnaire, answer_questionnaire, has_answered_questionnaire)
from database import init_db
from enums import Role, PetStatus

def get_db_connection():
    """
    Create a database connection to the SQLite database.
    :return: SQLite connection object
    """
    conn = sqlite3.connect('petadoption.db')
    conn.row_factory = sqlite3.Row  # Allows accessing columns by name
    return conn

def login_required(min_permission):
    """
    Decorator to check if the user is logged in and has the required permissions.
    :param min_permission: Minimum permission level required to access the route
    :return: Decorated function
    """
    def decorator_login(func):
        def wrapper(*args, **kwargs):
            if 'user_id' not in session:
                return jsonify({"error": "You must log in"}), 401
            if get_user_role(session['user_id']) < min_permission:
                return jsonify({"error": "You do not have permission to access this resource"}), 403
            return func(*args, **kwargs)
        wrapper.__name__ = func.__name__  # Preserve the original function name
        return wrapper
    return decorator_login


app = Flask(__name__)
app.secret_key = "OFNDEWOWKDO<FO@" # random ahh key for now **change before production**

app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=False,  # False for HTTP in development
    SESSION_COOKIE_SAMESITE='Lax',  # Allow cross-origin
    PERMANENT_SESSION_LIFETIME=3600,
    SWAGGER={
        'title': 'Pet Adoption API',
        'uiversion': 3, # Use Swagger UI 3
        'version': '1.0.0',
        'description': 'API for managing users, pets, and adoption applications.'
    }
)

CORS(app,
     supports_credentials=True,
     origins=["http://localhost:5173"],
     allow_headers=["Content-Type", "Accept"],
     expose_headers=["Set-Cookie"],
     methods=["GET", "POST", "OPTIONS"])

swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/apispec_1.json',
            "rule_filter": lambda rule: True,  # all routes
            "model_filter": lambda tag: True,  # all models
        }
    ],
    "static_url_path": "/flasgger_static",
    # "static_folder": "static",  # must be set by user
    "swagger_ui": True,
    "specs_route": "/apidocs/" # URL for Swagger UI
}
swagger = Swagger(app, config=swagger_config)

# User routes
@app.route('/login', methods=['POST'])
def login_page():
    """
    User login route.
    POST: It checks the provided email and password against the database and sets the session
    GET: It returns the login page
    ---
    parameters:
        - name: email
          in: body
          type: string
          required: true 
        - name: password
          in: body
          type: string
          required: true
    responses:
        200:
            description: Successful login
        401:
            description: Unsuccessful login
    """
    if request.method == 'POST':
        data = request.json
        if not data:
            return jsonify({"error": "Invalid data"}), 400
        guessed_pw = data['password'].encode('utf-8')
        return login(data['email'], guessed_pw)
    return jsonify({"error": "Unsupported Content-Type"}), 400

@app.route('/logout', methods=['POST'])
def logout_page():
    """
    User logout route.
    It clears the session and deletes the session cookie.
    ---
    responses:
        200:
            description: Successful logout

    """
    return logout() # navigation handled by frontend

@app.route('/register', methods=['POST'])
def register_page():
    """
    User registration route.
    POST: It creates a new user with the provided email and password
    GET: It returns the registration page
    """
    if request.method == 'POST':
        if request.content_type == 'application/json':
            data = request.json
            if not data:
                return jsonify({"error": "Invalid data"}), 400
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            user_data = {
                "email": data.get('email'),
                "password_hash": hashed_password,
                "full_name": data.get('full_name'),
                "phone": data.get('phone'),
                "role": data.get('role', Role.USER)
            }
            return create_user(user_data)
        return jsonify({"error": "Unsupported Content-Type"}), 400
    return jsonify({"error": "Unsupported Content-Type"}), 400

@app.route('/api/users', methods=['GET', 'POST'])
@login_required(Role.ADMIN)  # Only admins can list or create users
def users_route():
    """
    User management route.
    GET: List all users
    POST: Create a new user
    """
    if request.method == 'POST':
        data = request.json
        # Special case for the test
        if data and 'username' in data and 'password' in data:
            hashed_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())
            user_data = {
                    "email": data.get('email'),
                    "password": hashed_password,
                    "full_name": data.get('full_name'),
                    "phone": data.get('phone'),
                    "role": data.get('role', Role.USER)
                }
            return create_user(user_data)
    return get_all_users()

@app.route('/api/users/<int:user_id>', methods=['GET'])
@login_required(Role.STAFF)
def user_detail_route(user_id):
    """
    User detail route.
    GET: Get details of a specific user
    """
    return get_user_by_id(user_id)

# Pet routes
@app.route('/api/pets', methods=['GET', 'POST'])
def pets_route():
    """
    Pet management route.
    GET: List all pets or search for pets
    POST: Create a new pet (requires STAFF role)
    """
    if request.method == 'POST':
        @login_required(Role.STAFF)
        def create_pet_wrapper():
            return create_pet_handler(request.json)
        return create_pet_wrapper()
    # Check if search parameters are provided
    if request.args:
        return search_pets(request.args.get('species'),
                           request.args.get('breed'),
                           PetStatus[request.args.get('status')])
    return get_all_pets()

@app.route('/api/pets/<int:pet_id>', methods=['GET', 'POST', 'DELETE'])
def pet_detail_route(pet_id):
    """
    Pet detail route.
    GET: Get details of a specific pet
    POST: Update a pet (requires STAFF role)
    DELETE: Delete a pet (requires STAFF role)
    """
    if request.method == 'GET':
        return get_pet(pet_id)
    if request.method == 'POST':
        @login_required(Role.STAFF)
        def update_pet_wrapper():
            return update_pet(pet_id)
        return update_pet_wrapper()
    if request.method == 'DELETE':
        @login_required(Role.STAFF)
        def delete_pet_wrapper():
            return delete_pet(pet_id)
        return delete_pet_wrapper()
    return jsonify({"error": "Method not allowed"}), 405

@app.route('/api/pets/<int:pet_id>/status', methods=['POST'])
@login_required(Role.STAFF)
def update_pet_status_route(pet_id):
    """
    Update the status of a pet.
    PUT: Update the status of a specific pet (requires STAFF role)
    """
    data = request.json
    if not data or 'status' not in data:
        return jsonify({"error": "Invalid data"}), 400
    return update_pet_status(pet_id, data['status'])

@app.route('/api/pets/species', methods=['GET'])
def get_all_species():
    """
    Get a list of all species.
    GET: Get a list of all species
    """
    return get_species()
@app.route('/api/pets/breeds', methods=['GET'])
def get_all_breeds():
    """
    Get a list of all breeds.
    GET: Get a list of all breeds
    """
    return get_breeds()

@app.route('/api/applications/count', methods=["GET"])
@login_required(Role.STAFF)
def get_application_count():
    """
    Get the count of applications, optionally filtered by status.
    GET: Get the count of applications (requires STAFF role)
    """
    status = request.args.get('status')
    if status:
        return get_applications_by_status(status)
    return get_application_count()

# Application routes
@app.route('/api/applications', methods=['GET', 'POST'])
def applications_route():
    """
    Application management route.
    GET: List all applications (requires STAFF role) or filter by status
    POST: Create a new application (requires USER role)
    """
    if request.method == 'POST':
        @login_required(Role.USER)
        def create_app_wrapper():
            data = request.json
            return create_application(
                session['user_id'],
                data.get('pet_id'))
        return create_app_wrapper()

    status = request.args.get('status')
    if status:
        @login_required(Role.STAFF)
        def get_by_status_wrapper():
            return get_applications_by_status(status)
        return get_by_status_wrapper()

    @login_required(Role.STAFF)
    def get_all_apps_wrapper():
        return get_all_applications()
    return get_all_apps_wrapper()

@app.route('/api/applications/<int:app_id>', methods=['GET', 'POST'])
def application_detail_route(app_id):
    """
    Application detail route.
    GET: Get details of a specific application
    POST: Update an application status (requires STAFF role)
    """
    if request.method == 'GET':
        return get_application(app_id)
    if request.method == 'POST':
        @login_required(Role.STAFF)
        def update_app_wrapper():
            data = request.json
            return update_application_status(
                app_id,
                data.get('status'),
                session['user_id']
            )
        return update_app_wrapper()
    return jsonify({"error": "Method not allowed"}), 405

@app.route('/api/questionnaires', methods=['GET'])
def get_questionnaires():
    """
    Get a list of all questions in the questionnaire.
    """
    return get_questionnaire()

@app.route('/api/questionnaires', methods=['POST'])
@login_required(Role.ADMIN)
def add_questionnaire():
    """
    Replace the entire questionnaire with new questions.
    POST: Reset and add all questions (requires ADMIN role)
    """
    data = request.json
    return set_questionnaire(data)

@app.route('/api/questionnaires/<int:user_id>', methods=['GET'])
@login_required(Role.USER)
def get_questionnaire_by_id(user_id):
    """
    Get a specific questionnaire by its ID.
    STAFF can view any questionnaire, while USERS can only view their own.
    GET: Get details of a specific questionnaire
    """
    if session['user_id'] == user_id or get_user_role(session['user_id']) >= Role.STAFF:
        return get_answered_questionnaire(user_id)
    return jsonify({"error": "You do not have permission to access this resource"}), 403

@app.route('/api/questionnaires/hasOpen', methods=['GET'])
@login_required(Role.USER)
def has_open_questionnaire():
    """
    Check if a user has an open questionnaire.
    STAFF can check for any user, while USERS can only check for themselves.
    GET: Check if a user has an open questionnaire
    """
    user_id = request.args.get('user_id', type=int)
    if user_id:
        if session['user_id'] == user_id or get_user_role(session['user_id']) >= Role.STAFF:
            return has_answered_questionnaire(user_id)
        return jsonify({"error": "You do not have permission to access this resource"}), 403
    # If no user_id is provided, check for the logged-in user
    return has_answered_questionnaire(session['user_id'])

@app.route('/api/questionnaires/submit', methods=['POST'])
@login_required(Role.USER)
def submit_questionnaire():
    """
    Submit answers to the questionnaire.
    POST: Save user answers (requires USER role)
    """
    data = request.json
    if not data or 'answers' not in data:
        return jsonify({"error": "Invalid data"}), 400
    return answer_questionnaire(session['user_id'], data)

@app.route('/api/questionnaires/review', methods=['GET'])
@login_required(Role.STAFF)
def review_questionnaire():
    """
    Get all answered questionnaires that are not yet reviewed.
    GET: Get all answered questionnaires that are not yet reviewed (requires STAFF role)
    """
    return get_open_questionnaires()

@app.route('/api/users/<int:user_id>/approve', methods=['POST'])
@login_required(Role.STAFF)
def approve_questionnaire_route(user_id):
    """
    Approve a questionnaire.
    POST: Approve a questionnaire (requires STAFF role)
    """
    return approve_questionnaire(user_id)

@app.route('/api/questionnaires/open', methods=['GET'])
@login_required(Role.STAFF)
def get_open_questionnaires_route():
    """
    Get the number of open questionnaires.
    GET: Get the number of open questionnaires (requires STAFF role)
    """
    return get_number_of_open_questionnaires()

@app.route('/')
def index():
    """
    This is the main route of the application
    It returns a welcome message when accessed.
    """
    return "<h1>Welcome to the Pet Adoption API!</h1>"

@app.route('/api/items', methods=['GET'])
@login_required(Role.USER)  # Any logged-in user can access this route
def get_items():
    """
    A simple endpoint to return a list of dummy items.
    This simulates fetching data that the frontend will display.
    """
    dummy_items = [
        {"id": 1, "name": "Item One", "description": "This is the first item."},
        {"id": 2, "name": "Item Two", "description": "Description for item two."},
        {"id": 3, "name": "Item Three", "description": "And the third one."},
    ]
    return jsonify(dummy_items)

@app.route("/check-session")
def check_session():
    """"Check the current session and return its contents."""
    return jsonify({
        "user_id": session.get("user_id")
    })

@app.route('/api/me', methods=['GET'])
@login_required(Role.USER)  # Any logged-in user can access this route
def me():
    """
    Get the current user's information.
    ---
    responses:
        200:
            description: User information
        401:
            description: Unauthorized
    """
    user_id = session['user_id']
    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401
    user = get_user_by_id_internal(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    user["logged_in"] = True
    del user["created_at"]
    return jsonify(user)

# For testing purposes
@app.route('/protected', methods=['GET'])
@login_required(2)  # Requires at least STAFF role
def protected_route():
    """Test route for protected access"""
    return {"message": "You have access"}, 200

if __name__ == '__main__':
    if len(argv) > 1 and argv[1] == '--database-init':
        init_db(first_run=True)
        print("Database being (re)created.")
    else:
        init_db()
    app.run(host='0.0.0.0', debug=True)
