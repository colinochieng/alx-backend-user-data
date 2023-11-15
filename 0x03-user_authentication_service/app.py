#!/usr/bin/env python3
'''
Basic Flask app's Module
'''
from flask import Flask, Response, jsonify, url_for
from flask import abort, request, redirect
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', strict_slashes=False)
def home_route() -> Response:
    '''
    desc: route for home page
    return: a JSON payload
    '''
    return jsonify({"message": "Bienvenue"})


@app.route('/users', strict_slashes=False, methods=['POST'])
def users():
    '''
    desc: the end-point to register a user
    '''
    email = request.form.get('email')
    password = request.form.get('password')


    try:
        AUTH.register_user(email, password)

        # if no error: user created
        return jsonify(
                    {"email": email, "message": "user created"}
                    )
    except ValueError as e:
        return jsonify({"message": "email already registered"}
                    ), 400

@app.route('/sessions', strict_slashes=False, methods=['POST'])
def login():
    '''
    desc: function to login user
        create a user session and saves to db if
        login is successful
    '''
    data = request.form.to_dict()
    email, password = data.get('email'), data.get('password')

    if data and email:
        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)

            response = jsonify({"email": email, "message": "logged in"})
            response.set_cookie('session_id', session_id)

            return response
        else:
            abort(401)
    else:
        abort(401)

@app.route('/sessions', strict_slashes=False, methods=['DELETE'])
def logout():
    '''
    desc: logs the current user out
        Find the user with the requested session ID
         If the user exists destroy the session
         and redirect the user to GET /
    '''
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect(url_for('home_route'))


@app.route('/profile', strict_slashes=False)
def profile():
    '''
    desc: return user data
    NOTE: request is expected to contain a session_id cookie
    '''
    session_id = request.cookies.get('session_id')

    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)

    return jsonify({'email': user.email})


@app.route('/reset_password', strict_slashes=False, methods=['POST'])
def get_reset_password_token():
    '''
    function to respond to reset password post
    request is expected to contain form
        data with the "email" field
    '''
    email = request.form.get('email')

    if not email:
        abort(403)
    # get token
    try:
        token = AUTH.get_reset_password_token(email)
        return jsonify(
                {"email": email, "reset_token": token}
                )
    except ValueError:
        abort(403)


@app.route('/reset_password', strict_slashes=False, methods=['PUT'])
def update_password():
    '''
    desc: function to update password
    return: message
    NOTE: request is expected to contain form data
    with fields "email", "reset_token" and "new_password"
    '''
    data = request.form.to_dict()
    email = data.get('reset_token')
    reset_token = data.get('reset_token')
    new_password = data.get('new_password')

    if email and reset_token and new_password:
        try:
            AUTH.update_password(reset_token, new_password)

            return jsonify({"email": email, "message": "Password updated"})
        except ValueError as e:
            abort(403)
    else:
        abort(403)




if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="5000")
