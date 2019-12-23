from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User

def register(request):

	if request.method == 'POST':
		
		username = request.POST['username']
		password = request.POST['password']
		email = request.POST['email']
		User.objects.create_user(username, email, password)
		user = authenticate(username=username, password=password)
		if user is not None:
			login(request, user)
		else:
			return render(request, 'auths/signup.html')
		
		return redirect('auths:login')
	else:
		venues = Venue.objects.filter(user=request.user).order_by('-pk')
		name_pattern = "A-Za-z ";
		team_name_pattern = "A-Za-z0-9, ";
		phone_pattern = "0-9";
		return render(request, 'auths/signup.html')



# def login(request):
# 	username = password = ''
# 	if request.POST:
# 		username = request.POST['username']
# 		password = request.POST['password']

# 		user = authenticate(username=username, password=password)
# 		if user is not None:
# 			if user.is_active:
# 				login(request, user)
# 				ca_detail = CA_Detail.objects.get(user = request.user);
# 				if ca_detail.ca_approval :
# 					return redirect('ca:home')
# 				elif ca_detail.ca_profile_complete :
# 					return redirect('ca:pending')
# 				else :
# 					return redirect('ca:questionnare')

# 	return render(request, 'auths/login.html')