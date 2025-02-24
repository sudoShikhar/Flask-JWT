# JWT Auth Assignment

1. For the purpose of this assignment, users and tokens are stored in code directly in an array. Those could be stored in a DB instead.
1. Instead of curl commands, a Postman JSON is provided in the repo itself.
1. We'll create virtual enviroment<br>
    `python -m venv venv`
1. Activate venv<br>
    `.\venv\Scripts\activate.bat`
1. Install dependencies<br>
    `pip install -r requirements.txt`
1. Then run command <br>
    `flask --app JWT run`
1. `GET` All Users `/allusers`
    1. Helper API. It retrieves all users signed up, and their tokens, both access and refresh.
1. `POST` Sign Up `/signup`
    1. Pass body like `{"email" : "shikhar@test", "password" : "123456789"}`
    1. Creates a user entry.
    1. Does not login the user.
1. `POST` Login `/login`
    1. Pass body the same way as signup.
    1. Logs in the user. Creates an access token and a refresh token.
    1. Returns both the tokens.
1. `GET` Check Token `/checktoken`
    1. Pass access token in Auth header as a Bearer Token.
    1. Returns the email of the token passed, and the expiry time.
1. `GET` Refresh Token `/refreshtoken`
    1. Can be called with refresh token.
    1. Pass refresh token just like in check token.
    1. Returns the new access token for the user.
1. `GET` Revoke Token `/revoketoken`
    1. For the purpose of this assignment, any token passed in is revoked. Ideally this should be an admin utility and token could be passed in the body instead.
    1. Pass token just like in check token.
    1. Revokes the token, the said token can then not be used for any endpoint.
