import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText 

BASE_DIR = os.getcwd()

from .config import EMAIL, PASSWORD
<<<<<<< HEAD
=======

>>>>>>> d58b42b77ce160044d62c15752d1bd33a657b948
# Firebase Cursor connector
# Place cred.json in static folder at the place where manage.py is.
def my_cursor():
	try:
		firebase_admin.get_app()
	except ValueError as e:
		cred = credentials.Certificate(os.path.join(BASE_DIR, "cred.json"))
		firebase_admin.initialize_app(cred)
	
	db = firestore.client()
	return db

# Return number of available seats between src and des for train no. "train"
# There are 3 compartments in a train AC1, AC2 , AC3 with 30 seats available for covid. i.e 33%
# Actual Capactiy of each compartment os around 90
def get_available_seats(src, des, train, date):
	db = my_cursor()
	#doc_ref = db.collection("train").document(src).collection(train).document(src).collections()
	doc_ref = db.collection("trains").document("users").collection(src).document(train).collection(des).document(str(date)).collections()
	count = 0
	for compartment in doc_ref:
		for seats in compartment.stream():
			count+=1
	
	return 90 - count

# Handles Booking of tickets.
# If that src and des are not ever travelled, it make a new entry
# Return compartment number and seat number if booking is confirmed
# Else it return None.
def book_ticket(src, des, train, date, details):
	db = my_cursor()
	userId = details[0]['userId']
	#doc_ref = db.collection("train").document(src).collection(train).document(src)
	doc_ref = db.collection("trains").document("users").collection(str(src)).document(str(train)).collection(str(des)).document(str(date))
	his_ref = db.collection("history").document("userid").collection(str(userId))
	all_seats = doc_ref.get()

	if not all_seats.exists:		# Making default if not travelled.
		doc_ref.set({
			"AC1": -1,
			"AC2": -1,
			"AC3": -1
		})
	all_seats = doc_ref.get()

	seats = all_seats.to_dict() # AC1 AC2 AC3
	allotment = []
	booked_details = []
	for pass_info in details:
		for comp in seats.keys():
			fin_no = seats[comp]
			if fin_no != 89:			# Final seat will be 89 as we start of with seat number 2  and we have 30 seats.
				seat_no = fin_no + 3		# Vicinty of +-2 
				doc_ref.collection(comp).document(str(seat_no)).set(pass_info)
				pass_info['compartment'] = comp
				pass_info['seat'] = seat_no
				pass_info['date'] = date
				pass_info['src'] = src
				pass_info['des'] = des
				pass_info['train'] = train
				#his_ref.document().set(pass_info)
				booked_details.append(pass_info)
				allotment.append({
					"comp" : comp,
					"seat" : seat_no
				})
				seats[comp] = seat_no
				doc_ref.set(seats)
				break
	total_seats = len(details)
	if (total_seats>0):
		passenger = {
			'date' : date,
			'total_tickets': total_seats,
			"src": src,
			'des': des,
			'train': train
		}
		his_ref.document().set(passenger)
	else:
		pass

	send_mail(booked_details)
	return allotment

# Gives information about persorns booking history based on his/her userId.
def get_history(userid):
	history = []
	db = my_cursor()
	his_ref = db.collection("history").document("userid").collection(str(userid)).stream()
	for info in his_ref:
		history.append(info.to_dict())
	return history

def send_mail(details):
    sender = EMAIL
    receiver = details[0]['email']
    smtp = smtplib.SMTP('smtp.gmail.com', 587)
    smtp.starttls()
    smtp.login(sender, PASSWORD)
    train_name = details[0]['train']
    body  = "Thank You for choosing Safe Journey! Hope you are loving this experience.\n Your booking has been confirmed with train " + train_name + "\n Here is your passenger information.\n"
    count = 1
    for info in details:
        text = str(count) + ". Passenger Name: " + info['name'] + "\nCompartment No.: " + info['compartment'] + "\nSeat No.: " + str(info['seat']) + "\n"
        body+=text
        count+=1

    message = MIMEMultipart()
    message['Subject'] = "Booking Confirmed!"
    message['From'] = sender
    message["To"] = receiver
    message.attach(MIMEText(body, 'plain'))

<<<<<<< HEAD
    smtp.sendmail(sender,receiver,message.as_string())
=======
    smtp.sendmail(sender,receiver,message.as_string())

>>>>>>> d58b42b77ce160044d62c15752d1bd33a657b948
