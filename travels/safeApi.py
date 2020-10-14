import firebase_admin
from firebase-admin import credentials
from firebase_admin import firestore

def my_cursor():
	cred = credentials.Certificate("cred.json")
	firebase_admin.initialize_app(cred)

	db = firestore.client()
	return db

