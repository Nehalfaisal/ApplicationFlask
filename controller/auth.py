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




bcrypt = Bcrypt(app)

jwt = JWTManager(app)


def generate_hex(length):
    hex_digits = "0123456789abcdef"
    hex_string = ""
    for _ in range(length):
        hex_string += random.choice(hex_digits)
    return hex_string

secret_key = generate_hex(16)

print(secret_key)

app.config['JWT_SECRET_KEY'] = f'{secret_key}' 
app.secret_key = f'{secret_key}'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(seconds=9800)




@app.route("/signUp", methods=['POST'])
def singUp():
    name = request.json.get('name')
    email=request.json.get("email")
    password = request.json.get('password')
    role=request.json.get("role")
    if(role!="Admin" or role!="admin"):
      if(name and email and password):
        cur=db.cursor()
        with db.cursor() as cursor:
            
              sql = "SELECT * FROM user WHERE email = %s"
              cursor.execute(sql, (email,))
              user = cursor.fetchone()
              
              if user:
                  return jsonify({'message': 'User with that email already exists.'}), 409
                
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        print(name,email,hashed_password,role)
        # cur=db.cursor()
        cur.execute("INSERT INTO user (name, email, password, role) VALUES (%s, %s, %s, %s)", (name, email, hashed_password,role ))
        # cur.execute("select * from user")
        # result=cur.fetchall()
        # print(result)
        db.commit()
        return jsonify({'message': 'User signed up successfully.'}), 201
      else:
        return jsonify({'message': 'kindly give all user unput'}), 201
    else:
      return jsonify({"message":"one admin already exist not allowed"})



@app.route("/login",methods=["POST"])
def login():
  email=request.json.get("email")
  password=request.json.get("password")
  print(email,password)
  if(email and password):
      cur=db.cursor()
      with db.cursor() as cursor:
          
            sql = "SELECT * FROM user WHERE email = %s"
            cursor.execute(sql, (email,))
            user = cursor.fetchone()
          
          
            if user!=None:
                
                p= bcrypt.check_password_hash(user[3], password)
                
                if(p):
                  
                  access_token = create_access_token(identity=user[0])
                
                  session['token'] = access_token
                  session['role']=user[4]
                  session['email']=user[2]
                  session['name']=user[1]
                  session.permanent = True 
                

                  
                  if(access_token and p):
                  
                    return jsonify("login success")
                  else:
                      return jsonify({"message":"login failed"}),409
                else:
                  return jsonify({"message":"password incorrect"}),401
            else:
                
                return jsonify({"message":"User does not exist"}),404


  else:   
     return jsonify({"message":"kindly provide all user input"})




# @app.route("/updateUser",methods=["PATCH"])
# def protected():
#   print("protected")
#   token=session.get("token")
#   print(token)
#   return jsonify({"messages":"protected"}),200    
  
  