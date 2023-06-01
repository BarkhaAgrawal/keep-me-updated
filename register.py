import os
import json
from flask import Flask, render_template, request, redirect

app = Flask(__name__, template_folder='/Users/barkha/HackSharks-devpost')



# Define the file path for storing user data
DATA_FILE = 'user_data.json'

def load_user_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            data = json.load(file)
        return data
    else:
        return []

def save_user_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the user's registration details from the form
        username = request.form['username']
        email = request.form['email']
        interests = request.form.getlist('interests')

        # Load existing user data
        user_data = load_user_data()

        # Create a new user object
        new_user = {
            'username' : username,
            'email': email,
            'interests': interests
        }

#         # Store the user's interests in the user_data dictionary
#         user_data[username] = {
#             'email': email,
#             'interests': interests
#         }
        # Add the new user to the user data
        user_data.append(new_user)

        # Write the updated user data to the JSON file
        save_user_data(user_data)

        # Redirect the user to their profile page
        return redirect('/profile/' + username)
    else:
        return render_template('index.html')

@app.route('/profile/<username>')
def profile(username):
    # Load the user data
    user_data = load_user_data()
    
    # Find the user based on email
    for user in user_data:
        if user['username'] == username:
            break
#     # Retrieve the user's details from the user_data dictionary
#     user = user_data.get(username)

    if user:
        email = user['email']
        interests = user['interests']
    else:
        email = ''
        interests = []

    return render_template('profile.html', username=username, email=email, interests=interests)

@app.route('/update/<username>', methods=['GET', 'POST'])
def update(username):
    # Load the user data
    user_data = load_user_data()
    # Find the user based on email
    for user in user_data:
        if user['username'] == username:
            # Update the user's interests
            user['interests'] = interests
            break

    if user:
        email = user['email']
        interests = user['interests']
    else:
        return redirect('/profile/' + username)

    if request.method == 'POST':
        # Get the updated interests from the form
        updated_interests = request.form.getlist('interests')

        # Update the user's interests
        user['interests'] = updated_interests

        # Save the updated user data
        save_user_data(user_data)

        # Redirect the user to their profile page
        return redirect('/profile/' + username)
    else:
        return render_template('update.html', username=username, email=email, interests=interests)

if __name__ == '__main__':
    app.run(debug=True)
