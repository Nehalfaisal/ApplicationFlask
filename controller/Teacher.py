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


@app.route("/createTeacher",methods=["POST"])
def insertTeahcer():
  token=session.get("token")
  role=session.get("role")
  if(token):
    if(role=="Admin" or role=="teacher user"):  
      name=request.json.get("name")
      teaching_course=request.json.get("teaching_course")
      section=request.json.get("section")
      age=request.json.get("age")
      gender=request.json.get("gender")
      joining_date=request.json.get("joining_date")
      email=request.json.get("email")
      print(name,teaching_course,section,age,gender,joining_date,email)
      
      if(name and teaching_course and section and age and gender and joining_date and email):
        cur = db.cursor()
        sql = "SELECT * FROM teacher WHERE email = %s"
        cur.execute(sql, (email,))
        teacher = cur.fetchone()
        if(teacher):
          return jsonify({"message":"the email is already exist with other teacher"})
        else:
          cur = db.cursor()
          query = "INSERT INTO teacher (name,teaching_course,section, age, gender,joining_date,email) VALUES (%s, %s, %s, %s, %s, %s,%s)"
          values = (name,teaching_course, section, age, gender,joining_date,email)
          cur.execute(query, values)
          db.commit()
          return jsonify({"message":"teacher inserted success"}),200
      else:
          return jsonify({"message":"provide all input"}),404
    else:
       return jsonify({"messsage":"Only admin and teaches have access"})  
      
  else:
      return jsonify({"messsage":"Session Expires"})  
    
  

@app.route("/getAllTeacher",methods=["GET"])
def TeacherdataAll():
  
  token=session.get("token")
  role=session.get("role")
  if(token):
    if(role=="Admin"):
      
      
        cursor = db.cursor()
      
        cursor.execute("SELECT * FROM teacher")

        userData = cursor.fetchall()
      
        return jsonify({"data":userData}),200 
    else:
       return jsonify({"messages":"You dont have admin rights"}),200 

  else:
        return jsonify({"messages":"session expire"}),200 
      


 
# to get Teacher specific data

@app.route('/teacher/<int:id>', methods=['GET'])
def teacherSpecificdata(id):
  cur=db.cursor()
  token=session.get("token")
  role=session.get("role")       
  email=session.get("email") 
  if(token): 
    if(role=="teacher user"):
      
        sql = "SELECT * FROM user WHERE email = %s"
        cur.execute(sql, (email,))
        user=cur.fetchone()
        print(user)
        currsor=db.cursor()

        s = "SELECT * FROM teacher WHERE id = %s"
        
        currsor.execute(s, (id,))
        teacher=currsor.fetchone()
      
        if(teacher):
          if(user[2]==teacher[7]):
          
            return jsonify({"user":user}),200
          else:
            return jsonify({"message":"You dont hace access to see other user data"}),404
        else:
         return jsonify({"mess":"no student exist with this id "}),404  
    else:
    
        sql = "SELECT * FROM teacher WHERE id = %s"
        cur.execute(sql, (id,))
        user=cur.fetchone()
        if(user):
          return jsonify({"Teacher":user}),200
        else:
          return jsonify({"message":"no Teacher with this id "}),440

  else:
    return jsonify({"message":"session expire"}),440

@app.route("/updateTeacher/<int:id>",methods=["PATCH"])
def updateTeacher(id):
  
  token=session.get("token")
  role=session.get("role")
  if(token):       
    if(role=="Admin"):
      print(request.get_json())
      data=request.get_json()
      qry="update teacher set "
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

  
@app.route("/deleteTeacher/<int:id>",methods=["DELETE"])
def deleteTeacher(id):
  print("sadas")
  token=session.get("token")
  role=session.get("role")
  cur=db.cursor()
  if(token):       
    if(role=="Admin"):

        
      cur.execute("DELETE FROM teacher WHERE id = %s", (id,))
      db.commit()
      return jsonify({"messages":"teacher deleted success"}),200  
    else:
      return jsonify({"message":"Only Admin can update"}) 
  else:
     return jsonify({"message":"session time out"}),440

   
  
  