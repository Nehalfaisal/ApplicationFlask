from flask import Flask
import mysql.connector;

app=Flask(__name__)


# MySQL Database Configuration
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="s4smart12@A",
    database="school_management"
)

# Check database connection
if db.is_connected():
    print("Connected to the MySQL database.")
else:
    print("Failed to connect to the MySQL database.")

@app.route("/")
def home():
  return "wokring"


from controller import auth,user,student,Teacher
