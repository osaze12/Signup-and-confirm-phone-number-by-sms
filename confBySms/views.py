from django.shortcuts import render, redirect

from django.contrib.auth.forms import UserCreationForm
from confBySms.form import SignupForm, ConfirmMe
from django.contrib import messages

from strgen import StringGenerator
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from confBySms.models import Profile
from twilio.rest import Client
from twilio.base.exceptions import TwilioRestException

from django.http import HttpResponse

VALID_FOR = "1 Minute"
MINUTES = 1
MY_TWILIO_NUMBER = '+12028366879' #MY TWILIO TRIAL PHONE NUMBER

phone_number = '+2348113253726'
GENERATE_TOKEN = StringGenerator("[\d\w]{5}").render()

account_sid = 'AC3482336dc717a052994f7f7a6196840c'
auth_token = 'dce3ba6224cd5abccde745811b4bfb5e'

client = Client(account_sid, auth_token)


def create_profile(request):
	if request.method == 'POST':
		if 'time_out' in request.session or 'new_user' in request.session or 're-send' in request.session:
			messages.info(request, 'You already have an account stored, please resend token')
			return redirect('confirm_token')
		else:
			form= SignupForm(request.POST)
			if form.is_valid():
				if form.cleaned_data['password'] == form.cleaned_data['password2']:

					first_name = form.cleaned_data['first_name']
					last_name = form.cleaned_data['last_name']
					username = form.cleaned_data['username']
					email = form.cleaned_data['email']
					password = form.cleaned_data['password']
					day= form.cleaned_data['day']
					month = form.cleaned_data['month']
					year = form.cleaned_data['year']
					phone_number = form.cleaned_data['phone_number']


					user_info = {
						
						'first_name'    : first_name,
						'last_name'     : last_name,
						'username'      : username,
						'email'         : email,
						'password'      : password,
						'day'           : day,
						'month'         : month,
						'year'          : year,
						'phone_number'  : phone_number,
						
					}

					request.session['user_info'] = user_info
					request.session['token'] = GENERATE_TOKEN
					request.session['new_user'] = True

					current_datetime = datetime.now()
					request.session['time'] = current_datetime.strftime('%m/%d/%Y %H:%M:%S')

					

					# CLEAN PHONE NUMBER AND SEND MESSAGE
					cleaned_phone_no = clean_phone_number(phone_number)

					#try:
					send_msg(cleaned_phone_no, request.session['token'])
					
					messages.info(request, 'token is only valid for {}'.format(VALID_FOR))
					return redirect('confirm_token')
				else:
					print(data)
					messages.info(request, 'Password Doesn\'t match')
					return redirect('/create')
			else:
				messages.info(request, 'Data is invalid')
				return redirect('/create')

	form= SignupForm()
	return render(request, 'confBySms/index.html', {'form': form})

def confirm_token(request):
	if 'time_out'in request.session or 'new_user' in request.session or 're-send' in request.session:
		form = ConfirmMe()
		return render(request, 'confBySms/tokenView.html', {'form': form})
	else:
		return redirect('create')

def process(request):
	if request.method == 'POST':
		form = ConfirmMe(request.POST)
		if form.is_valid():
			user_token_input = form.cleaned_data['token']
			if 'time' in request.session:
				time = request.session['time']
			else:
				messages.info(request, 'Token has expired, please resend', extra_tags="danger")
				return redirect('confirm_token')
			if time_has_expired(time) == False: #time has not expired
					generated_token = request.session['token']
					if generated_token == user_token_input:
						# STORE INTO THE DATABASE HERE
						user = User.objects.create(first_name= request.session.user_info.first_name,
							last_name = request.session.user_info.last_name,
							username = request.session.user_info.username,
							email = request.session.user_info.email,
							password = request.session.user_info.password
							)
						user.save(commit = False)

						profile = Profile.objects.create(user = user,
							day =  request.session.user_info.day,
							month =  request.session.user_info.month,
							year =  request.session.user_info.year,
							is_confirmed = True,
							phone_number =  request.session.user_info.phone_number
							)
						profile.save()

						del request.session['user_info']
						del request.session['token']
						del request.session['time']

						if 'new_user' in request.session:
							del request.session['new_user']

						if 're_send' in request.session:
							del request.session['re-send']

						if 'time_out' in request.session:
							del request.session['time_out']


						messages.info(request, 'Data saved successfully ')
						return redirect('login')
					else:
							messages.info(request, 'token is invalid ', extra_tags="danger")
							return redirect('confirm_token')

					return HttpResponse('<h2>Error occured</h2>')
			else: #time has expired
				request.session['time_out'] = True

				if 'new_user' in request.session:
					del request.session['new_user']

				if 're_send' in request.session:
					del request.session['re-send']

				if 'token' in request.session:
					del request.session['token']

				if 'time' in request.session:
					del request.session['time']

				messages.info(request, "sorry your token has expired, please resend", extra_tags="danger")
				return redirect('confirm_token')

def resend_token(request):
	request.session['token'] = GENERATE_TOKEN
	current_datetime = datetime.now()
	request.session['time'] = current_datetime.strftime('%m/%d/%Y %H:%M:%S')
	request.session['re-send'] = True

	if 'time_out' in request.session:
		del request.session['time_out']

	if 'new_user' in request.session:
		del request.session['new_user']

	messages.info(request, 'Token sent, vaid only valid for {}'.format(VALID_FOR))
	return redirect('confirm_token')
	

def time_has_expired(user_datetime):
	user_start_time = datetime.strptime(user_datetime, "%m/%d/%Y %H:%M:%S")
	stop_time = user_start_time + timedelta(minutes = MINUTES)
	if datetime.now() < stop_time:
		return False
	else:
		return True


def login():
	if request.method == 'POST':
		pass
	else:
		return render(request, 'confBySms/login.html')


def clean_phone_number(number):

	if '+234' in number and len(number) == 15:
		first_5 = number[0:5]
		if '0' in first_5:
			new_no = number[0:4] + number[5:]
			return new_no
		else:
			return number
	elif '+234' in number and len(number) == 14:
		return number 

	else:
		return False

def send_msg(phone_number, token):
	try:

		message = client.messages.create(
                    body='This is from Oz, This is your Token, Valid for 1 Minute {}'.format(token),
                    from_='{}'.format(MY_TWILIO_NUMBER),
                    to= phone_number
                          )

		print(message.sid)
	except Exception as e:
		print("----------------------------------")
		print(e)
		return redirect('create')