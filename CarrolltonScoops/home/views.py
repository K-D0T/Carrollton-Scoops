from django.shortcuts import render, redirect
from address.models import *
from .forms import * 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.urls import reverse
from django.http import HttpResponseRedirect
from .forms import RegisterForm
import smtplib, ssl
import re
from email.message import Message
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email import encoders


def home(request):
	if request.method == 'POST':
		form = MainForm(request.POST)
		addressId= Address.objects.last().id
		
		if form.is_valid():
			post = form.save(commit=False)
			post.destination_id = addressId
			post.save()
			print("successful")
		else:
			print("ERROR" )#form.errors)
	else:
		form = MainForm()

	return render(request, 'index.html', {'form': form})

def login_request(request):

	if request.method == 'POST':
		form = AuthenticationForm(request=request, data=request.POST)
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(username=username, password=password)
		
		if user is not None:
			print("authenticated")
			login(request, user)
			return HttpResponseRedirect(reverse("RequestRide"))

	else:
		print("invalid pass")

	form = AuthenticationForm()
	return render(request = request,
					template_name = "login.html",
					context={"form":form})

def signup(response):
	if response.method == "POST":
		form = RegisterForm(response.POST)
		print(form)
		if form.is_valid():
			form.save()
			
			return HttpResponseRedirect(reverse("home"))
		else:
			print(form.errors)
		
	else:
		form = RegisterForm()

	return render(response, "signup.html", {"form":form})

def SendEmail(name, email, phone, destination):
	print(name, email, phone, destination)
	
	sender_email = "jake.lake2407@gmail.com"
	receiver_email = "kaiden.thrailkill@gmail.com"
	password = "aqgwcpqamnvqyswf"


	message = """\
	Subject: Ride Request From {}

	Name: {}
	Email: {}
	Phone: {}
	Destination: {}
	""".format(name, name, email, phone, destination)


	
	
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.ehlo()
	server.starttls()
	server.login(sender_email, password)
	server.sendmail(sender_email, receiver_email, message)
	server.quit()



def RequestRide(request):
	if request.method == 'POST':
		form = MainForm(request.POST)
		addressId= Address.objects.last().id
		
		if form.is_valid():
			post = form.save(commit=False)
			post.destination_id = addressId
			post.save()
			SendEmail(post.name, post.email, post.phone_number, post.destination)
			print("successful")
		else:
			print(form.errors)
	else:
		form = MainForm()
	return render(request, 'RequestRide.html', {"form": form})

