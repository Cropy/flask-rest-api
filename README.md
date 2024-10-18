# Flask-REST-API
 Flask REST API with JWT auth and SQLite DB

To Visualize Data Base: -> access localhost on browser

# Endpoints:
[POST] 
localhost/auth-token -> generates bearer tokens

[GET]
localhost/get-user?id={id} -> get user by id

[GET]
localhost/get-user -> gets all users

[POST]
localhost/create-user -> creates a new user

[PUT]
localhost/update-user/{id} -> updates user by id

[DELETE]
localhost/delete-user/{id} -> deletes user

# Payload Structure:
```json
{
    "name": "example",
    "email": "example@mail.com"
}
```