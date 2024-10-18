from flask import Flask, request, jsonify
from models import db, User
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import datetime


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = "troll_key"


db.init_app(app)
jwt = JWTManager(app)

def create_tables():
    db.drop_all()
    db.create_all()
    if not User.query.filter_by(email = "admin@example.com").first():
        initial_user = User(name = "Admin", email = "admin@example.com") # creates an initial user, used to generate tokens
        db.session.add(initial_user)
        db.session.commit()


@app.route("/auth-token", methods=["POST"])
def generate_token():
    payload = request.get_json()
    user = User.query.filter_by(email = payload["email"]).first()
    if user and user.name == payload['name']: 
        access_token = create_access_token(identity = user.id, expires_delta = datetime.timedelta(minutes = 10))
        return jsonify(access_token = access_token), 200
    return jsonify({"error": "Invalid credentials"}), 


@app.route("/get-user", methods=["GET"])
@jwt_required()
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
@jwt_required()
def create_user_data():
    payload = request.get_json()
    new_user = User(name = payload["name"], email = payload["email"])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User Created"}), 201


@app.route("/update-user/<user_id>", methods=["PUT"])
@jwt_required()
def update_user_data(user_id):
    payload = request.get_json()
    user = User.query.filter_by(id = user_id).first()
    if user:
        user.name = payload["name"]
        user.email = payload["email"]
        db.session.commit()
        return jsonify({"message": "User Updated"}), 200
    return jsonify({"error": "User not found"}), 404 


@app.route("/delete-user/<user_id>", methods=["DELETE"])
@jwt_required()
def delete_user_data(user_id):
    user = User.query.filter_by(id = user_id).first()
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User Deleted"}), 200
    return jsonify({"error": "User not found"}), 404


if __name__ == "__main__":
    with app.app_context():
        create_tables()
    app.run(debug = True)