import firebase_admin
from firebase_admin import credentials, db

# Firebase Credentials JSON File (Download from Firebase Console)
cred = credentials.Certificate("firebase_credentials.json")

# Initialize Firebase
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smartpilldispenser-2a736-default-rtdb.firebaseio.com/'
})

# Reference to Database
firebase_ref = db.reference('/pill_dispenser')
