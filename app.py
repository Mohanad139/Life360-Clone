from flask import Flask, jsonify
from datetime import datetime
from database import init_db, insert_location, gets_location,get_all_locations,delete_location

init_db() # Initilize the database when the app start


app = Flask(__name__)

@app.route('/')
def home():
    return "Life360 Clone"



@app.route('/update_location/<user_id>/<lat>/<lon>')
def accept_user(user_id,lat,lon):     
    # Get the value from the user and store it inside dictionary locations
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")   
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
                
    
    insert_location(user_id,lat,lon,timestamp)
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


if __name__ == '__main__':
    app.run(debug=True)