from django.shortcuts import render, redirect
from django.http import HttpResponse
import datetime
import time
import calendar
import pytz
import pyrebase
from .forms import LoginForm


# Create your views here.

config = {
'apiKey': "AIzaSyCZuko6X66AylGmp4E7_rmuie_Z_WOW4oo",
'authDomain': "messenger-71bd3.firebaseapp.com",
'databaseURL': "https://messenger-71bd3.firebaseio.com",
'projectId': "messenger-71bd3",
'storageBucket': "messenger-71bd3.appspot.com",
'messagingSenderId': "799254915773"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
database=firebase.database()
chats_list = []
email = "test@test.uk"

def login(request):
	global chats_list
	if request.method == "POST":
		form = LoginForm()
		email = request.POST['email']
		password = request.POST['password']
		try:
			user = auth.sign_in_with_email_and_password(email, password)
			session_id = user['idToken']
			uid = user['localId']
			request.session['uid'] = str(session_id)

			chats = database.child("User").get()
			chats_list = []
			for chat in chats.each():
				chats_list.append(chat.key())
			return redirect('/base')
			#return render(request, 'website/base.html', {'chats_list': chats_list})
		except:
			print("CANT LOGIN")
			error = 'login error'
			return render(request, 'website/login.html', {'form': form, 'error': error })
		print("norm")

	form = LoginForm()
	return render(request, 'website/login.html', {'form': form})

def base(request):
	global chats_list
	email = "test@test.uk"
	password = "test14"
	user = auth.sign_in_with_email_and_password(email, password)
	session_id = user['idToken']
	uid = user['localId']
	request.session['uid'] = str(session_id)

	chats = database.child("User").get()
	chats_list = []
	for chat in chats.each():
		chats_list.append(chat.key())
	return render(request, 'website/base.html', {'chats_list': chats_list})

def chat(request, name):
	if request.method == "POST":
		timee = int(round(time.time() * 1000))
		message = request.POST['text_input']
		data = {'autor': email , 'textMessage': message, 'timeMessage': timee}
		database.child("User").child(name).child("Messages").push(data)
		print("POST : ", name, timee, message)
	d = database.child("User").child(name).child("Messages").get()
	messages_list = []
	for i in d.each():
		message_dict = i.val()
		data = str(datetime.datetime.fromtimestamp(message_dict['timeMessage'] / 1e3))
		message_dict['timeMessage'] = data[0:19]
		messages_list.append(message_dict)
	return render(request, 'website/chat.html', {'vv': name, 'chats_list': chats_list, 'messages_list': messages_list})

def show_chat(request):
	return render(request, 'website/show_chat.html')
# def stream_handler(message):
#     print(message)

# my_stream = database.child("User").child("test").child("Messages").stream(stream_handler)

