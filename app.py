from flask import Flask, request, jsonify
from models import db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.before_first_request
def create_tables():
    db.create_all()


@app.route("/get-user", methods=["GET"])
def get_user_data():
    user_id = request.args.get("id") #id query string param, optional
    if user_id:
        user = User.query.filter_by(id = user_id).first()
        if user:
            return jsonify({"id": user.id, "name": user.name, "email": user.email}), 200
        return jsonify({"error": "User not found"}), 404
    users = User.query.all()
    return jsonify([{"id": user.id, "name": user.name, "email": user.email} for user in users]), 200


@app.route("/create-user", methods=["POST"])
def create_user_data():
    payload = request.get_json()
    new_user = User(name = payload['name'], email = payload['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User Created"}), 201


@app.route("/update-user/<user_id>", methods=["PUT"])
def update_user_data(user_id):
    payload = request.get_json()
    user = User.query.filter_by(id = user_id).first()
    if user:
        user.name = payload["name"]
        user.email = payload["email"]
        db.session.commit()
        return jsonify({"message": "User Updated"}), 200
    return jsonify({"error": "User not found"}), 


@app.route("/delete-user/<user_id>", methods=["DELETE"])
def delete_user_data(user_id):
    user = User.query.filter_by(id = user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User Deleted"}), 200
    return jsonify({"error": "User not found"}), 404


if __name__ == "__main__":
    app.run(debug = True)