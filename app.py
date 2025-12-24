from flask import Flask, jsonify
from datetime import datetime


app = Flask(__name__)

@app.route('/')
def home():
    return "Life360 Clone"

locations = {}


@app.route('/update_location/<user_id>/<lat>/<lon>')
def accept_user(user_id,lat,lon):     # Get the value from the user and store it inside dictionary locations
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")    
    locations[user_id] = {"lat":lat,"lon":lon,"Timestamp":timestamp}
    return jsonify({"message":"Successfully accepted the user"})



@app.route('/location/<user_id>')
def get_location(user_id):             # Take user_id and Check if user id is valid then return location with date, if not return error.
    if user_id in locations:
        value = locations[user_id]
        return jsonify({"user_id": user_id, "location": value}), 200   
    else:
        return jsonify({"error":"Missing user id"})
    


@app.route('/locations')
def list_users():                # Once it is called it will list everything inside the dictionary locations
    return jsonify({"Users": locations})

    

if __name__ == '__main__':
    app.run(debug=True)