from flask import Flask, jsonify
from datetime import datetime


app = Flask(__name__)

@app.route('/')
def home():
    return "Life360 Clone"

locations = {}


@app.route('/update_location/<user_id>/<lat>/<lon>')
def accept_user(user_id,lat,lon):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")    
    locations[user_id] = {"lat":lat,"lon":lon,"Date":timestamp}
    return jsonify({"message":"Successfully accepted the user"})



@app.route('/location/<user_id>')
def get_location(user_id):
    if user_id in locations:
        value = locations[user_id]
        return jsonify({"user_id": user_id, "location": value}), 200   
    else:
        return jsonify({"error":"Missing user id"})
    
    

if __name__ == '__main__':
    app.run(debug=True)