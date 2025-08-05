from flask import Flask, jsonify, request
from flask_cors import CORS

from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity

# import sentry_sdk

# sentry_sdk.init(
#     dsn="https://c1d68e7c34f50b0bbc77b08ad74c1f5d@o491346.ingest.us.sentry.io/4509707544625152",
#     # Add data like request headers and IP for users,
#     # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
#     send_default_pii=True,
# )

app = Flask(__name__)

CORS(app)

app.config["JWT_SECRET_KEY"] = "MyKey@123"
# app.config["TESTING"] = True 

jwt = JWTManager(app)

products_list = []
users=[{"email" : "admin@mail.com", "password":"12345"}]

@app.route("/")
def hello():
    res = {"Flask-API NGROK Login": "1.0"}
    return jsonify(res), 200

@app.route("/register", methods=["POST"])
def register():
    data = dict(request.get_json())
    users.append(data)
    return jsonify(data), 201

@app.route("/login", methods=["POST"])
def login():
    data = dict(request.get_json())
    for user in users:
        if user["email"] == data["email"] and user["password"] == data["password"]:
            # Create a token and return to the user
            token = create_access_token(identity=user["email"])
            return jsonify({"message": "Login Success", "token" : token}), 200
        else:
            pass
    return jsonify({"message": "Invalid Credentials"}), 401

@app.route("/api/products", methods=["GET", "POST"])
@jwt_required()
def products():

    email = get_jwt_identity()
    print("Email------", email)

    if request.method == "GET":
        #Return a list of products as JSON
        return jsonify(products_list), 200
    elif request.method == "POST":
        #Data will be recived here as JSON so we convert to Dictionary
        data = dict(request.get_json())
        if "name" not in data.keys() or "bp" not in data.keys() or "sp" not in data.keys():
            error = {"error" : "invalid keys"}
            return jsonify(error), 403
        elif data["name"] == "" or data["bp"] == "" or data["sp"] == "":
            error = {"error" : "ensure all values are set"}
            return jsonify(error), 403
        else:
            products_list.append(data)
            return jsonify(data), 201
    else:
        #A diferent request method was sent
        error = {"error" : "Method not allowed"}
        return jsonify(error), 405

if __name__ == "__main__":
    app.run(debug=True)
