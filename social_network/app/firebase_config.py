import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('path/to/your/firebase/credentials.json')
firebase_admin.initialize_app(cred)

# Firestore database
db = firestore.client()
