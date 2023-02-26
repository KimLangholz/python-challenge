from flask import Blueprint, render_template, request
from helpers.template_functions import call_api
from helpers.api_functions import *

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/')
def index():
    # Call the API to get the list of users
    response = call_api("https://d16m5wbro86fg2.cloudfront.net/api/users")
    usernames = [user["username"] for user in response["Users"]]
    # Render the HTML template with the list of users
    return render_template('index.html', usernames=usernames)

@routes_bp.route('/result', methods=['POST'])
def result():
    username = request.form['username']
    button = request.form['button']

    # Call the appropriate API endpoint based on which button was clicked
    if button == 'buildable_sets':
        response = call_api(f"http://127.0.0.1:5000/api/v1.0/buildable-sets/{username}")
        print(response)
    else:
        response = call_api(f"http://127.0.0.1:5000/api/v1.0/buildable-sets-additional/{username}")

    # Render the HTML template with the JSON response from the API call
    return render_template('result.html', response=response)
