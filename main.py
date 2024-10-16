from flask import Flask, request, jsonify


# mock data
user_data = [
    {
        "id": "1",
        "name": "John Doe",
        "email": "john.doe1@email.com"
    },
    {
        "id": "2",
        "name": "John Doe 2",
        "email": "john.doe3@email.com"
    },
    {
        "id": "3",
        "name": "John Doe 2",
        "email": "john.doe2@email.com"
    }
]


app = Flask(__name__)


@app.route("/get-user")
def get_user_data():
    user_id = request.args.get("id") #id query string param, optional
    if user_id:
        for user in user_data:
            if user["id"] == user_id:
                return jsonify(user), 200
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(user_data), 200 




    

if __name__ == "__main__":
    app.run(debug=True)