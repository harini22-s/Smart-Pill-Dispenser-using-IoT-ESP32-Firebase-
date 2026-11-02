from flask import Flask, render_template, request, jsonify
import pyrebase

app = Flask(__name__)

# Firebase configuration
firebaseConfig = {
    "apiKey": "AIzaSyAVhaMyKE65KmD2ArWbew36wTEBr6h9r_o",
    "authDomain": "smartpilldispenser-2a736.firebaseapp.com",
    "databaseURL": "https://smartpilldispenser-2a736-default-rtdb.firebaseio.com",
    "projectId": "smartpilldispenser-2a736",
    "storageBucket": "smartpilldispenser-2a736.firebasestorage.app",
    "messagingSenderId": "680607789018",
    "appId": "1:680607789018:web:0b944fcfeffd70b41b1ae3",
    "measurementId": "G-3HV7D49855"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()

@app.route("/")
def index():
    data = db.child("pill_dispenser").get().val() or {"dispense_status": {}, "alerts": {"missed_doses": []}}
    return render_template("index.html", data=data)

@app.route("/set_schedule", methods=["POST"])
def set_schedule():
    new_schedule = request.json

    formatted_schedule = {}
    for key, time_str in new_schedule.items():
        if time_str:
            formatted_schedule[key] = {
                "time": time_str,  # Store actual time
                "dispensed": False,
                "taken": False
            }

    db.child("pill_dispenser").child("dispense_status").set(formatted_schedule)
    return jsonify({"success": True, "message": "Schedule updated successfully"}), 200

@app.route("/get_schedule")
def get_schedule():
    data = db.child("pill_dispenser").get().val() or {"dispense_status": {}, "alerts": {"missed_doses": []}}
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)
