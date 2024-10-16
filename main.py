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


@app.route("/get-user", methods=["GET"])
def get_user_data():
    user_id = request.args.get("id") #id query string param, optional
    if user_id:
        for user in user_data:
            if user["id"] == user_id:
                return jsonify(user), 200
        return jsonify({"error": "User not found"}), 404
    
    return jsonify(user_data), 200 


@app.route("/create-user", methods=["POST"])
def create_user_data():
    payload = request.get_json()
    user_data.append(payload)
    return jsonify({"message": "User Updated"}), 201


@app.route("/update-user/<user_id>", methods=["PUT"])
def create_user_data(user_id):
    payload = request.get_json()
    for user in user_data:
            if user["id"] == user_id:
                index = user_data.index(user)
                user_data[index] = payload
                return jsonify({"message": "User Updated"}), 200
                
    return jsonify({"error": "User not found"}), 404



    

if __name__ == "__main__":
    app.run(debug=True)