from flask import Flask
import mysql.connector
# from flask_cors import CORS
from flask_mysqldb import MySQL

app=Flask(__name__)
# CORS(app)  # Enable CORS for all routes


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 's4smart12@A'
app.config['MYSQL_DB'] = 'school_management'

db = MySQL(app)
print(db)

# MySQL Database Configuration
# db = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="s4smart12@A",
#     database="school_management",


# )

# # Check database connection
# if db.is_connected():
#     print("Connected to the MySQL database.")
# else:
#     print("Failed to connect to the MySQL database.")

@app.route("/app")
def home():
  return "Api is working "


from controller import auth,user,student,Teacher
if __name__ == '__main__':
    app.run()
