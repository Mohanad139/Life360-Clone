from flask import Flask, jsonify, request
from datetime import datetime,timedelta
from database import init_db, insert_location, gets_location,get_all_locations,delete_location,get_user_history,create_users_table,insert_users_table,get_user
from flask_cors import CORS
import bcrypt
import jwt
import secrets
import base64





init_db() # Initilize the database when the app start
create_users_table()

app = Flask(__name__)
CORS(app)

secret_key = secrets.token_hex(16)


@app.route('/')
def home():
    return "Life360 Clone"





@app.route('/update_location/<user_id>/<lat>/<lon>')
def accept_user(user_id,lat,lon):     
    # Get the value from the user and store it inside the database.
    if user_id == '':
        return jsonify({"error": "User ID must contain a character"}), 400

    try:
        lat = float(lat)
        lon = float(lon)
    except ValueError:
        return jsonify({"error": "Latitude and longitude must be valid numbers"}), 400
    if not(lat <= 90 and lat>= -90):
        return jsonify({"error": "Latitude must be in range of -90,90"}), 400
    if not(lon <= 180 and lon >= -180):
        return jsonify({"error": "Longitude must be in range of -180,180"}), 400
                


    insert_location(user_id,lat,lon)
    return jsonify({"message":"Successfully accepted the user"})
    



@app.route('/location/<user_id>')
def get_location(user_id):             
    # Take user_id and Check if user id is valid then return location with date, if not return error.
    result = gets_location(user_id)
    if result is not None:
        return jsonify({"user_id": user_id, "location": result}), 200   
    else:
        return jsonify({"error":"Missing user id"})
    


@app.route('/locations')
def list_users():
    # Once it is called it will list everything inside the dictionary locations
    rows = get_all_locations()
    users = {}
    for row in rows:
        users[row[0]]={
            "Latitude" : row[1],
            "Longitude" : row[2],
            "Timestamp" : row[3],
        }

    return jsonify({"Users": users})

@app.route('/location/<user_id>', methods=['DELETE'])
def delete(user_id):
    result = gets_location(user_id)
    if result is None:
        return jsonify({"error":"User does not exist"}),404
    delete_location(user_id)
    return jsonify({"message": f"The location of this user id {user_id} has been deleted."})  


@app.route('/history/<user_id>')
def history(user_id):
    isthere = gets_location(user_id)
    if isthere is None:
        return jsonify({"error":"No history found for this user."}),404
    result = get_user_history(user_id)
    history = []
    for row in result:
        history.append({
            "ID" : row[0],
            "Latitude" : row[2],
            "Longitude" : row[3],
            "Timestamp" : row[4]
        })
    
    return jsonify({"User ID": user_id, "History": history })



@app.route("/register",methods = ["POST"])
def register():
    username = request.form.get('username')
    if username == "":
        return jsonify({"error":"Username can't be empty"}),400
    
    user = get_user(username)
    # Check if username is not None using user[1] since user[0] is id.
    if user is not None:
        return jsonify({"error": "Invalid username or password"}),400

    password = request.form.get('password')
    if len(password) < 8:
        return jsonify({"error":"Password must contain 8 or more charachters"}),400

    password_hash = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt(rounds=12))
    insert_users_table(username,password_hash)

    return jsonify({'message':f"User {username} has been successfully registered"})

@app.route("/login",methods = ["POST"])
def login():
    username = request.form.get('username')
    password = request.form.get('password')

    user = get_user(username)
    if user is None:
        return jsonify({"error": "Invalid username or password"}),400
    
    #Get the hashed password using user[2]
    hashed = user[2]


    if hashed is None:
        return jsonify({"error": "Invalid username or password"}), 400

    if bcrypt.checkpw(password.encode('utf-8'),hashed):
        payload = {
            "sub" : username,
            "exp" : datetime.utcnow() + timedelta(hours=24),
            "iat" : datetime.utcnow()
        }



        final_jwt = jwt.encode(payload,secret_key,algorithm='HS256')


        return jsonify({'token':final_jwt}),200
    else:
        return jsonify({"error": "Invalid username or password"}),400

if __name__ == '__main__':
    app.run(debug=True)

