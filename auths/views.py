from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from .tokens import account_activation_token
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.validators import EmailValidator, RegexValidator
from .utilities import generateAlcherId






def register(request):

	if request.method == 'POST':
		print(request.POST, "$$$$$$$$$$$$$$$$$$$$$")
		password = request.POST['password']
		fullname = request.POST['fullname']
		gender = request.POST.get('gender')
		team_name = request.POST['team_name']
		email = request.POST['email']
		phone = request.POST['phone']
		interests = request.POST.getlist('interests[]')
		interests_int = [int(x) for x in interests]
		data = {}
		name_validator = RegexValidator('^[A-Za-z ]+$')
		if fullname == '':
			data['fullname_error'] = "Please enter your Full Name"
		else:
			try:
				name_validator(fullname)
			except Exception as e:
				data['fullname_error'] = "Only letters and white spaces"


		if email == '':
			data['email_error'] = "Please enter a valid Email ID"
		else:
			try:
				email_validator = EmailValidator()
				email_validator(email)
			except Exception as e:
				data['email_error'] = "Invalid email format"


		if phone == '':
			data['phone_error'] = "Please enter a valid Phone No"
		else:
			try:
				phone_number_validator = RegexValidator('^[0-9]{10}$')
				phone_number_validator(phone)
			except Exception as e:
				data['phone_error'] = "Must have 10 digits and only digits from 0 to 9 allowed"





		if gender == None:
			data['gender_error'] = "Gender is mandatory"

		if team_name == '':
			data['team_name_error'] = "Please enter your Team Name"
		else:
			try:
				name_validator(team_name)
			except Exception as e:
				data['team_name_error'] = "Only letters and white spaces"

		if password == '':
			data['password_error'] = "Password is required"
		else:
			if len(password) < 8:
				data['password_error'] = "Minimum 8 characters"

		if len(interests_int) == 0:
			data['interests_error'] = "Please select one or more interests"

		if data:
			print(data, "$$$$$$$$$$$$$$$$$$$$$")
			return render(request, 'auths/ca_register.html', data)


		alcher_id = generateAlcherId(fullname)
		if User.objects.filter(email=email).filter(profile__emailVerified=True):
			print("Same Email or phone no. already present")
			return redirect('auths:register')
		else:
			User.objects.create_user(alcher_id, email, password)
			user = authenticate(username=alcher_id, password=password)
			if user is not None:
				user.is_active=False
				user.save()
				profUser = Profile(user=user, alcher_id=alcher_id, fullname=fullname, phone=phone, college=team_name, gender=gender)
				profUser.save()
				profUser.interests.add(*interests_int)
				profUser.save()
				current_site = get_current_site(request)
				subject = 'Activate Your Alcheringa CA Account'
				message = render_to_string('auths/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
				user.email_user(subject, message)
				return redirect('auths:account_activation_sent')
			else:
				print("user is none")
				return redirect('auths:register')

	else:
		name_pattern = "[A-Za-z ]*"
		team_name_pattern = "[A-Za-z0-9, ]*"
		phone_pattern = "[0-9]{10}"
		interests_list = Interest.objects.all()
		context = {
		'name_pattern': name_pattern,
		'team_name_pattern' : team_name_pattern,
		'phone_pattern' : phone_pattern,
		'interests_list' : interests_list,
		}
		return render(request, 'auths/ca_register.html', context)


def register_oauth(request):

	if request.method == 'POST':
		print(request.POST, "$$$$$$$$$$$$$$$$$$$$$")
		gender = request.POST.get('gender')
		team_name = request.POST['team_name']
		phone = request.POST['phone']
		interests = request.POST.getlist('interests[]')
		interests_int = [int(x) for x in interests]
		data = {}
		name_validator = RegexValidator('^[A-Za-z ]+$')


		if phone == '':
			data['phone_error'] = "Please enter a valid Phone No"
		else:
			try:
				phone_number_validator = RegexValidator('^[0-9]{10}$')
				phone_number_validator(phone)
			except Exception as e:
				data['phone_error'] = "Must have 10 digits and only digits from 0 to 9 allowed"





		if gender == None:
			data['gender_error'] = "Gender is mandatory"

		if team_name == '':
			data['team_name_error'] = "Please enter your Team Name"
		else:
			try:
				name_validator(team_name)
			except Exception as e:
				data['team_name_error'] = "Only letters and white spaces"


		if len(interests_int) == 0:
			data['interests_error'] = "Please select one or more interests"

		if data:
			print(data, "$$$$$$$$$$$$$$$$$$$$$")
			return render(request, 'auths/ca_oauth_register.html', data)

		if Profile.objects.filter(phone=phone):
			print("Same Phone no. already present")
			return redirect('auths:register_oauth')

		fullname = request.user.first_name + " " + request.user.last_name
		alcher_id = generateAlcherId(fullname)
		CA_Detail.objects.create(user = request.user)
		profUser = Profile(user=request.user, alcher_id=alcher_id, fullname=fullname, phone=phone, college=team_name, gender=gender)
		profUser.save()
		profUser.interests.add(*interests_int)
		profUser.save()
		return redirect('ca:home')
		

	else:
		name_pattern = "[A-Za-z ]*"
		team_name_pattern = "[A-Za-z0-9, ]*"
		phone_pattern = "[0-9]{10}"
		interests_list = Interest.objects.all()
		context = {
		'name_pattern': name_pattern,
		'team_name_pattern' : team_name_pattern,
		'phone_pattern' : phone_pattern,
		'interests_list' : interests_list,
		}
		return render(request, 'auths/ca_oauth_register.html', context)


def activate(request, uidb64, token, backend= 'django.contrib.auth.backends.ModelBackend'):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.profile.emailVerified = True
        user.save()
        user.profile.save()
        auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        CA_Detail.objects.create(user=request.user)
        return redirect('ca:questionnare')
    else:
    	return render(request, 'auths/account_activation_invalid.html')




def account_activation_sent(request):
	return render(request, 'auths/account_activation_sent.html')






def login(request):
	username = password = ''
	if request.POST:
		email = request.POST['ca_email']
		password = request.POST['ca_password']

		data = {}
		try:
			email_validator = EmailValidator()
			email_validator(email)
		except Exception as e:
			data['email_error'] = "Please enter a valid Email ID"

		if password == '':
			data['password_error'] = "Password is required"

		if data:
			return render(request, 'auths/ca_login.html', data)

		user_obj = User.objects.filter(email=email)
		if len(user_obj) == 0:
			print("No user with this email exists!")
			data['login_error'] = "Sorry! Invalid credentials. Try again."
			return render(request, 'auths/ca_login.html', data)
		else:
			user = authenticate(username=user_obj[0].username, password=password)
			if user is None:
				print("Please enter the correct password for your account.")
				data['login_error'] = "Sorry! Invalid credentials. Try again."
				return render(request, 'auths/ca_login.html', data)


			user_obj = user_obj.filter(profile__emailVerified=True)

			if len(user_obj) == 0:
				print("Email not verified yet!")
				return redirect('auths:verifyEmail')
			
			
			auth_login(request, user)
			print(user.username)

			ca_detail = CA_Detail.objects.filter(user = request.user);
			if len(ca_detail) == 0:
				CA_Detail.objects.create(user=request.user)
				ca_detail = CA_Detail.objects.filter(user = request.user);
			if ca_detail[0].ca_approval :
				return redirect('ca:home')
			elif ca_detail[0].ca_profile_complete :
				return redirect('ca:pending')
			else :
				return redirect('ca:questionnare')
	return render(request, 'auths/ca_login.html')


def verifyEmail(request):
	return render(request, 'auths/verify_your_email.html')


def resendMail(request):
	if request.method=='POST':
		email=request.POST['emailField']
		user_obj = User.objects.filter(email=email).filter(profile__emailVerified=True)
		if len(user_obj)!=0 :
			messages.info(request, ('Email already verified! Please proceed to login.'))
			return redirect('auths:login')
		user_obj = User.objects.filter(email=email)
		if len(user_obj) ==0:
			messages.info(request, 'Email is not registered yet, please signup!')
			return redirect('auths:register')
		if len(user_obj)>0:
			user = user_obj[0]
			current_site = get_current_site(request)
			subject = 'Activate Your Alcheringa CA Account'
			message = render_to_string('auths/account_activation_email.html', {
        	'user': user,
        	'domain': current_site.domain,
        	'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        	'token': account_activation_token.make_token(user),
        })
			user.email_user(subject, message)
			return redirect('auths:account_activation_sent')
	return render(request, 'auths/verify_your_email.html')


def logout_(request):
	if request.user:
		logout(request)
	# messages.success(request, 'Logged out successfully!!')
	return redirect('auths:login')