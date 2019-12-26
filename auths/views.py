from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *

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
		if User.objects.filter(email=email):
			print("Same Email or phone no. already present")
			return render(request, 'auths/signup.html')
		else:
			User.objects.create_user(alcher_id, email, password)
			user = authenticate(username=alcher_id, password=password)
			if user is not None:
				auth_login(request, user)
				profUser = Profile(user=user, fullname=fullname, phone=phone, college=team_name, gender=gender)
				profUser.save()
				profUser.interests.add(*interests_int)
				profUser.save()
				CA_Detail.objects.create(user=request.user)
				return redirect('ca:questionnare')
			else:
				return render(request, 'auths/signup.html')
		return redirect('auths:register')

	else:
		name_pattern = "[A-Za-z ]*";
		team_name_pattern = "[A-Za-z0-9, ]*";
		phone_pattern = "[0-9]*";

		interests_list = Interest.objects.all()

		context = {
		'name_pattern': name_pattern,
		'team_name_pattern' : team_name_pattern,
		'phone_pattern' : phone_pattern,
		'interests_list' : interests_list,
		}

		return render(request, 'auths/ca_register.html', context)



def login(request):
	username = password = ''
	if request.POST:
		email = request.POST['ca_email']
		password = request.POST['ca_password']
		user_obj = User.objects.filter(email=email)
		if len(user_obj) > 0:
			user = authenticate(username=user_obj[0].username, password=password)
			if user is not None:
				if user.is_active:
					auth_login(request, user)

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