from flask import Flask
import mysql.connector;
# from flask_cors import CORS


app=Flask(__name__)
# CORS(app)  # Enable CORS for all routes



# MySQL Database Configuration
db = mysql.connector.connect(
    host="127.0.0.1",
    user="appuser",
    password="s4smart12",
    database="school_management",


)

# Check database connection
if db.is_connected():
    print("Connected to the MySQL database.")
else:
    print("Failed to connect to the MySQL database.")

@app.route("/app")
def home():
  return "Api is working "


from controller import auth,user,student,Teacher
