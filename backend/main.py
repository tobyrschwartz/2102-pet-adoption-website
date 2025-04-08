from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    """
    This is the main route of the application
    It returns a welcome message when accessed.
    """
    return "<h1>Welcome to the Pet Adoption API!</h1>"

if __name__ == '__main__':
    app.run(debug=True)
