from app import app
from flask import Flask, request,session, jsonify
from app import db
from flask_bcrypt import Bcrypt
# from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
# from flask_jwt import JWT, jwt_required, current_identity
from flask_jwt_extended import JWTManager, create_access_token
from flask_session import Session
import datetime
import uuid
import random


@app.route("/createStudent",methods=["POST"])
def insertStudent():
  token=session.get("token")
  if(token):
    name=request.json.get("name")
    std_class=request.json.get("Std_class")
    course=request.json.get("courses")
    birthdate=request.json.get("birthdate")
    contact=request.json.get("contact")
    age=request.json.get("age")
    gender=request.json.get("gender")
    email=request.json.get("email")
  

    if(name and std_class and course and birthdate and contact and age and gender): 
      cur = db.cursor()
      query = "INSERT INTO student (name,Std_class,courses, birthdate, contact, age, gender,email) VALUES (%s, %s, %s, %s, %s, %s,%s,%s)"
      values = (name,std_class, course, birthdate, contact, age, gender,email)
      cur.execute(query, values)
      db.commit()
      return jsonify({"message":"student inserted success"}),200
    else:
        return jsonify({"message":"provide all input"}),404
  else:
    return jsonify({"messsage":"Session Expires"})  

@app.route("/getAllStudent",methods=["GET"])
def studentdataAll():
  
  token=session.get("token")
  role=session.get("role")
  if(token):
    if(role=="Admin"):
      
      
        cursor = db.cursor()
      
        cursor.execute("SELECT * FROM student")

        userData = cursor.fetchall()
        print(userData)      
        return jsonify({"data":userData}),200 
    else:
       return jsonify({"messages":"You dont have admin rights"}),200 

  else:
        return jsonify({"messages":"session expire"}),200 
      


 
# to get user specific data
@app.route('/student/<int:id>', methods=['GET'])
def studentSpecificdata(id):
  cur=db.cursor()
  token=session.get("token")
  role=session.get("role")       
  email=session.get("email") 
  if(token): 
    if(role=="normal user"):
      
        sql = "SELECT * FROM user WHERE email = %s"
        cur.execute(sql, (email,))
        user=cur.fetchone()
        print(user)
        currsor=db.cursor()

        s = "SELECT * FROM student WHERE id = %s"
        
        currsor.execute(s, (id,))
        student=currsor.fetchone()
        print(student)
        if(student):
          if(user[2]==student[8]):
          
            return jsonify({"user":user}),200
          else:
            return jsonify({"message":"You dont hace access to see other user data"}),404
        else:
         return jsonify({"mess":"no student exist with this id "}),404  
    else:
    
        sql = "SELECT * FROM student WHERE id = %s"
        cur.execute(sql, (id,))
        user=cur.fetchone()
        if(user):
          return jsonify({"user":user}),200
        else:
          return jsonify({"message":"no user with this id "}),440

  else:
    return jsonify({"message":"session expire"}),440

@app.route("/updateStudent/<int:id>",methods=["PATCH"])
def updateStudent(id):
  print(" i am in update student")
  token=session.get("token")
  role=session.get("role")
  if(token):       
    if(role=="Admin"):
      print(request.get_json())
      data=request.get_json()
      qry="update student set "
      for key in data:
        qry+=f"{key}='{data[key]}',"
      qry=qry[:-1]+f" where id={id}" 
      cur=db.cursor()
      cur.execute(qry)
      db.commit()

      return jsonify({"messages":"update"}),200  
    else:
      return jsonify({"message":"Only Admin can update"}) 
  else:
     return jsonify({"message":"session time out"}),440

  
@app.route("/deleteStudent/<int:id>",methods=["DELETE"])
def deleteStudent(id):
  token=session.get("token")
  role=session.get("role")
  cur=db.cursor()
  if(token):       
    if(role=="Admin"):

        
      cur.execute("DELETE FROM student WHERE id = %s", (id,))
      db.commit()
      return jsonify({"messages":"user deleted success"}),200  
    else:
      return jsonify({"message":"Only Admin can update"}) 
  else:
     return jsonify({"message":"session time out"}),440

   
  
  