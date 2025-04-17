"""Main module of the application"""
from flask import Flask, request, session, jsonify
from user import login, get_user_role, logout
from flasgger import Swagger

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
app.config.update( # credits to https://flask.palletsprojects.com/en/2.3.x/quickstart/#sessions
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE='Lax'
)

@app.route('/login', methods=['GET','POST'])
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
        return login(request.form['email'], request.form['password'])
    # **placeholder for the login page**
    return '''
        <form method="POST">
            Email: <input type="text" name="email"><br>
            Password: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
        '''

@app.route('/logout', methods=['GET'])
def logout_page():
    """
    User logout route.
    It clears the session and redirects to the login page.
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
            description: Unauthorized login

    """
    #prob will change this to a redirect instead of just a json response, it works as a mock tho
    return logout()

@app.route('/api/pets/create', methods=['GET'])
@login_required(2)  # Requires at least STAFF role
def create_pet():
    """To be implemented, just wanted to check my decorator doesn't throw an error
    ---
    parameters:
        (to be implemented)
    responses:
        201:
            description: Pet sucessfully created
        401:
            description: Pet not create
    """
    return jsonify({"message": "Pet created successfully!"}), 201

@app.route('/')
def index():
    """
    This is the main route of the application
    It returns a welcome message when accessed.
    """
    return "<h1>Welcome to the Pet Adoption API!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
