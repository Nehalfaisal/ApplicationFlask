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
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(seconds=60)



@app.route("/getAll",methods=["GET"])
def userdata():
  
  token=session.get("token")
  role=session.get("role")
  if(role=="Admin"):
      if(role=="Admin" and token):
      
        cursor = db.cursor()
      
        cursor.execute("SELECT * FROM user")

        userData = cursor.fetchall()
        print(userData)      
        return jsonify({"data":userData}),200 
      else:
          return jsonify({"messages":"you have dont have  access"}),200 
  else:
    return jsonify({"Alert":"You dont have admin rights"}),401      


 
# to get user specific data
@app.route('/user/<int:id>', methods=['GET'])
def userSpecificdata(id):
  cur=db.cursor()
  token=session.get("token")
  role=session.get("role")       
  email=session.get("email") 
  print(role)
  if(role=="normal user"):
    print("i normal User")
    if(token):
      sql = "SELECT * FROM user WHERE email = %s"
      cur.execute(sql, (email,))
      user=cur.fetchone()
      print("user is ")
      print(user)
      if(user[0]==id):
        
        return jsonify({"user":user}),200
      else:
        return jsonify({"message":"You dont hace access to see other user data"}),404
    else:
        return jsonify({"message":"session time out"}),440
  else:
    if(token):
      sql = "SELECT * FROM user WHERE id = %s"
      cur.execute(sql, (id,))
      user=cur.fetchone()
      if(user):
        return jsonify({"user":user}),200
      else:
         return jsonify({"message":"no user with this id "}),440

    else:
       return jsonify({"message":"session time out"}),440

@app.route("/updateUser/<int:id>",methods=["PATCH"])
def update(id):
  
  token=session.get("token")
  role=session.get("role")
  if(token):       
    if(role=="Admin"):
      print(request.get_json())
      data=request.get_json()
      qry="update user set "
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

  
@app.route("/deleteUser/<int:id>",methods=["DELETE"])
def delete(id):
  token=session.get("token")
  role=session.get("role")
  cur=db.cursor()
  if(token):       
    if(role=="Admin"):

        
      cur.execute("DELETE FROM user WHERE id = %s", (id,))
      db.commit()
      return jsonify({"messages":"user deleted success"}),200  
    else:
      return jsonify({"message":"Only Admin can update"}) 
  else:
     return jsonify({"message":"session time out"}),440

   
  
  