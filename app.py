# # from flask import Flask, request, jsonify, render_template
# # from transformers import pipeline

# # app = Flask(__name__)

# # # Load Hugging Face model
# # model_name = "sathwik-kom/fake-review-detection_1"
# # classifier = pipeline("text-classification", model=model_name)

# # @app.route("/")
# # def home():
# #     return render_template("input.html")  # Make sure input.html is in the "templates" folder

# # @app.route("/analyze", methods=["POST"])
# # def analyze():
# #     data = request.get_json()
# #     text = data.get("text", "")

# #     if not text:
# #         return jsonify({"error": "No text provided"}), 400

# #     result = classifier(text)[0]
# #     label = "Fake Review" if result["label"] == "LABEL_1" else "Genuine"
    
# #     return jsonify({"label": label, "score": result["score"]})

# # if __name__ == "__main__":
# #     app.run(debug=True)


# from flask import Flask, request, jsonify, render_template
# from transformers import pipeline
# from huggingface_hub import interpreter_login

# # Login to Hugging Face Hub
# #interpreter_login()

# app = Flask(__name__)

# # Load Hugging Face model
# model_name = "sathwik-kom/fake-review-detection_1"
# classifier = pipeline("text-classification", model=model_name)

# @app.route("/home")
# def home():
#     return render_template("input.html")  # Ensure input.html exists in the "templates" folder
# from flask import render_template

# @app.route('/')
# def login_page():
#     return render_template('form.html')


# @app.route("/analyze", methods=["POST"])
# def analyze():
#     data = request.get_json()
#     text = data.get("text", "")

#     if not text:
#         return jsonify({"error": "No text provided"}), 400

#     result = classifier(text)[0]
#     label = "Fake Review" if result["label"] == "LABEL_1" else "Genuine"
    
#     return jsonify({"label": label, "score": result["score"]})

# if __name__ == "__main__":
#     app.run(debug=True)










# from flask import Flask, request, jsonify, render_template, session, redirect, url_for
# from flask_pymongo import PyMongo
# from werkzeug.security import generate_password_hash, check_password_hash
# from transformers import pipeline
# import secrets

# app = Flask(__name__)
# app.secret_key = secrets.token_hex(16)  # Replace with a secure key

# # MongoDB Configuration
# app.config["MONGO_URI"] = "mongodb+srv://sathudemon37:sathudemon37@cluster0.rbhqi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0/users"
# mongo = PyMongo(app)

# # Load Hugging Face Model
# model_name = "sathwik-kom/fake-review-detection_1"
# classifier = pipeline("text-classification", model=model_name)

# # Login Page
# @app.route("/")
# def login_page():
#     return render_template("form.html")

# # Signup Route

# @app.route("/signup", methods=["POST"])
# def signup():
#     data = request.get_json()
#     email = data.get("email")
#     password = data.get("password")

#     if not email or not password:
#         return jsonify({"error": "Email and password are required"}), 400

#     users = mongo.db.users

#     # Check if user already exists
#     if users.find_one({"email": email}):
#         return jsonify({"error": "User already exists"}), 409

#     # Hash password before storing
#     hashed_password = generate_password_hash(password)

#     # Insert user into MongoDB
#     new_user = users.insert_one({"email": email, "password": hashed_password})

#     # Store user in session
#     session["user"] = str(new_user.inserted_id)  # Convert ObjectId to string

#     return jsonify({"message": "Signup successful", "userId": session["user"]}), 201


# # Login Route

# @app.route("/login", methods=["POST"])
# def login():
#     data = request.get_json()
#     email = data.get("email")
#     password = data.get("password")

#     user = mongo.db.users.find_one({"email": email})
#     if user and check_password_hash(user["password"], password):
#         session["user"] = email  # Store user in session
#         return redirect(url_for("home"))

#     return jsonify({"error": "Invalid credentials"}), 401


# # Protected Home Page
# @app.route("/home")
# def home():
#     if "user" not in session:
#         return redirect(url_for("login_page"))  # Redirect to login if not authenticated
#     return render_template("input.html")

# # Logout Route
# @app.route("/logout")
# def logout():
#     session.pop("user", None)  # Remove user from session
#     return redirect(url_for("login_page"))

# # Analyze Review Route
# @app.route("/analyze", methods=["POST"])
# def analyze():
#     if "user" not in session:
#         return jsonify({"error": "Unauthorized access"}), 401  # Restrict to logged-in users only

#     data = request.get_json()
#     text = data.get("text", "")

#     if not text:
#         return jsonify({"error": "No text provided"}), 400

#     result = classifier(text)[0]
#     label = "Fake Review" if result["label"] == "LABEL_1" else "Genuine"

#     return jsonify({"label": label, "score": result["score"]})

# if __name__ == "__main__":
#     app.run(debug=True)









from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash
import os
from dotenv import load_dotenv
from flask import redirect, url_for
from flask import session
from transformers import pipeline

import secrets


app = Flask(__name__)

CORS(app)

# MongoDB Configuration
load_dotenv()
app.config["MONGO_URI"] = "mongodb+srv://sathudemon37:sathudemon37@cluster0.rbhqi.mongodb.net/test?retryWrites=true&w=majority&appName=Cluster0"

mongo = PyMongo(app)
db = mongo.db

model_name = "sathwik-kom/fake-review-detection_1"  # Your model repo name
classifier = pipeline("text-classification", model=model_name)


print(db.list_collection_names())  
user_count = db.users.count_documents({})
print(f"User count: {user_count}")

app.secret_key = secrets.token_hex(16)  # Generates a secure random key

@app.route('/test-db')
def test_db():
    users = db.users.find()  # Get all users
    users_list = list(users)  # Convert to list
    return jsonify({"users": users_list if users_list else "No users found"})

# Serve form.html (Login/Signup Page)
@app.route('/')
def serve_main():
    return render_template("form.html")  # Correctly loads form.html from templates

# Serve input.html (Review Analysis Page)
@app.route('/input')
def serve_input():
    return render_template("input.html")  # Correctly loads input.html from templates

# Sign-up Route
@app.route('/signup', methods=['POST'])
def signup():
    data = request.json
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    existing_user = db.users.find_one({"email": email})
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    hashed_password = generate_password_hash(password)
    db.users.insert_one({"email": email, "password": hashed_password})
    return jsonify({"message": "User registered successfully"}), 201

# Login Route
import json

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    print("Received login data:", json.dumps(data, indent=2))  # Debugging

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = db.users.find_one({"email": email})
    if not user:
        return jsonify({"error": "User not found"}), 400

    if not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid password"}), 400

    return jsonify({"message": "Login successful", "userId": str(user["_id"])}), 200



@app.route('/analyze', methods=['POST'])
def analyze_text():
    data = request.json
    review_text = data.get("reviewText", "")

    if not review_text:
        return jsonify({"error": "No text provided"}), 400

    result = classifier(review_text)[0]
    label = "Fake Review" if result["label"] == "LABEL_1" else "Genuine"

    return jsonify({"label": label, "score": result["score"]})

# Logout Route
@app.route('/logout', methods=['POST'])
def logout():
    session.pop("user", None)  # Clear user session
    return jsonify({"message": "Logged out successfully", "redirect": url_for("serve_main")})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5000)), debug=True)

