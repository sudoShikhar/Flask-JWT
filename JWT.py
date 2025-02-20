from flask import Flask
from flask import jsonify
from flask import request

from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token
from flask_jwt_extended import create_refresh_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import get_jwt

from datetime import datetime, timedelta
app = Flask(__name__)
app.config["JWT_SECRET_KEY"] = "ShikharJWT"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(seconds = 300)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days = 30)
jwt = JWTManager(app)

"""
Could be later switched to a DB or redis etc...
Password could be hashed with bcrypt for better security...
"""
users = {
    # "email" : "password"
}
users["shikhar@test"] = "123456789" #TODO: delete
tokens = {
    # "email" : {"access": "token1", "refresh": "token2"}
}
expired_tokens_identifiers = set()

@app.post("/signup")
def sign_up():
    email = request.json.get("email")
    password = request.json.get("password")

    # TODO: check if user already exists

    users[email] = password

    return jsonify(success = True), 200


@app.post("/login")
def login():
    email = request.json.get("email")
    password = request.json.get("password")

    # TODO: check if user does not exist
    if password == users[email]:
        access_token = create_access_token(identity = email)
        refresh_token = create_refresh_token(identity = email)
        tokens[email] = {
            "access": access_token,
            "refresh": refresh_token,
        }
        return jsonify(
            access_token = access_token,
            refresh_token = refresh_token,
            ), 200
    else:
        return jsonify(success = False), 401
    
@app.get("/checktoken")
@jwt_required()
def check_token():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(
        logged_in_as = current_user,
        expires = datetime.fromtimestamp(get_jwt()["exp"])
    ), 200

@app.get("/refreshtoken")
@jwt_required(refresh = True)
def refresh_token():
    email = get_jwt_identity()
    access_token = create_access_token(identity = email)
    tokens[email]["access"] = access_token
    return jsonify(access_token = access_token)

@jwt.token_in_blocklist_loader
def check_if_token_is_revoked(jwt_header, jwt_payload: dict):
    jwt_identifier = jwt_payload["jti"]
    return jwt_identifier in expired_tokens_identifiers

@app.get("/revoketoken")
@jwt_required()
def revoke_token():
    """
        For now lets just revoke the token of the user who called,
        this can rather be an admin power and accept token in body...   
    """
    expired_tokens_identifiers.add(get_jwt()["jti"])
    print(expired_tokens_identifiers)
    return jsonify(success = True), 200


@app.get("/allusers")
def all_users():
    return jsonify({ 
        email: { 
            "password": users[email], 
            "token": tokens.get(email, None),
        } for email in users
    }), 200
