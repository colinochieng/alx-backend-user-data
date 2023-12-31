#!/usr/bin/env python3
"""
Module housing routes for user Session Authentication
"""
from api.v1.views import app_views
from flask import request, jsonify, abort
from os import getenv
from models.user import User


@app_views.route("/auth_session/login", methods=["POST"], strict_slashes=False)
def session_login() -> str:
    """
    desc: login function for sessions
        computes various responses based on user info provided
    Return: logged user if credentials are correct
    """
    email = request.form.get("email")
    passwd = request.form.get("password")

    if not email or len(email) == 0:
        return jsonify({"error": "email missing"}), 400

    if not passwd or len(passwd) == 0:
        return jsonify({"error": "password missing"}), 400

    # retrive user from db

    objs = User.search({"email": email})

    if not objs:
        return jsonify({"error": "no user found for this email"}), 404
    else:
        user = objs[0]

        if not user.is_valid_password(passwd):
            return jsonify({"error": "wrong password"}), 401
        else:
            # generate a session ID for the logged in User
            from api.v1.app import auth

            session_id = auth.create_session(user.id)

            response = jsonify(user.to_json())

            response.set_cookie(getenv("SESSION_NAME"), session_id)

            return response


@app_views.route("/auth_session/logout",
                 strict_slashes=False, methods=["DELETE"])
def session_logout() -> str:
    """
    desc: deletes users current session
        checks if user is in session and logs the user out
    return: empty dictionary
    """
    from api.v1.app import auth

    if not auth.destroy_session(request):
        abort(404)

    return jsonify({}), 200
