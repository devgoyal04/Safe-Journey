import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os

BASE_DIR = os.getcwd()


# Firebase Cursor connector
# Place cred.json in static folder at the place where manage.py is.
def my_cursor():
	
	try:
		firebase_admin.get_app()
	except ValueError as e:
		cred = credentials.Certificate(os.path.join(BASE_DIR, "static", "cred.json"))
		firebase_admin.initialize_app(cred)
	
	db = firestore.client()
	return db


# Return number of available seats between src and des for train no. "train"
# There are 3 compartments in a train A1, A2 , A3 with 30 seats available for covid.
# Actual Capactiy of each compartment os around 100
def get_available_seats(src, des, train):
	db = my_cursor()
	doc_ref = db.collection("train").document(src).collection(train).document(src).collections()
	
	count = 0
	for compartment in doc_ref:
		for seats in compartment.stream():
			count+=1
	
	return 90 - count


# Handles Booking of tickets.
# If that src and des are not ever travelled, it make a new entry
# Return compartment number and seat number if booking is confirmed
# Else it return None.
def book_ticket(src, des, train, details):
	db = my_cursor()
	doc_ref = db.collection("train").document(src).collection(train).document(src)
	all_seats = doc_ref.get()
	
	if not all_seats.exists:		# Making default if not travelled.
		doc_ref.set({
			"A1": -2,
			"A2": -2,
			"A3": -2
		})
	all_seats = doc_ref.get()
	
	seats = all_seats.to_dict()
	for comp in seats.keys():
		fin_no = seats[comp]
		if fin_no != 88:				# Final seat will be 88 as we start of with seat number 1  and we have 30 seats.
			seat_no = fin_no + 3		# Vicinty of +-2 
			doc_ref.collection(comp).document(str(seat_no)).set(details)
			return comp, seat_no
	
	return None




