from django.contrib.auth import authenticate
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

name_pattern = "[A-Za-z ]*"
team_name_pattern = "[A-Za-z0-9, ]*"
phone_pattern = "[0-9]*"
interests_list = Interest.objects.all()

def generateAlcherId(fullname):
	latUserID = User.objects.latest('id').id
	newUserID=latUserID+1
	fullname_trim = fullname.replace(" ","")
	fullname_trim = fullname_trim.replace("'","")
	fullname_trim = fullname_trim[:3].upper()
	alcher_id= "ALC-"+fullname_trim+"-"+str(newUserID)
	return alcher_id


def register(request):

	if request.method == 'POST':
		
		password = request.POST['password']
		fullname = request.POST['fullname']
		gender = request.POST['gender']
		team_name = request.POST['team_name']
		email = request.POST['email']
		phone = request.POST['phone']
		interests = request.POST.getlist('interests[]')
		interests_int = [int(x) for x in interests]
		alcher_id = generateAlcherId(fullname)
		print(alcher_id)
		if User.objects.filter(email=email).filter(profile__emailVerified=True):
			print("Same Email or phone no. already present")
			context = {
			'name_pattern': name_pattern,
			'team_name_pattern' : team_name_pattern,
			'phone_pattern' : phone_pattern,
			'interests_list' : interests_list,
		}

			return render(request, 'auths/ca_register.html',context)
		else:
			User.objects.create_user(alcher_id, email, password)
			user = authenticate(username=alcher_id, password=password)
			if user is not None:
				user.is_active=False
				user.save()
				profUser = Profile(user=user, fullname=fullname, phone=phone, college=team_name, gender=gender)
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
				context = {
			'name_pattern': name_pattern,
			'team_name_pattern' : team_name_pattern,
			'phone_pattern' : phone_pattern,
			'interests_list' : interests_list,
			}
			return render(request, 'auths/ca_register.html', context)

	else:
		context = {
		'name_pattern': name_pattern,
		'team_name_pattern' : team_name_pattern,
		'phone_pattern' : phone_pattern,
		'interests_list' : interests_list,
		}
		return render(request, 'auths/ca_register.html', context)


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
		user_obj = User.objects.filter(email=email)
		if len(user_obj) == 0:
			print("No user with this email exists!")
			return render(request,'auths/ca_login.html')
		else:
			user_obj = User.objects.filter(email=email).filter(profile__emailVerified=True)
			if len(user_obj) == 0:
				print("Email not verified yet!")
				return render(request, 'auths/verify_your_email.html')
			else:
				user = authenticate(username=user_obj[0].username, password=password)
				if user is None:
					print("Please enter the correct password for your account.")
					return render(request, 'auths/ca_login.html')
				else:
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