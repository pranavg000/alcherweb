from django.shortcuts import render
from django.urls import reverse
from .fbshare import *
from .models import *
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.decorators import login_required
from ca.decorators import profile_required
# Create your views here.


def fb(request) :
    get_page_posts()
    get_user_posts() 

    return HttpResponse("run successful") 



@login_required
@profile_required
def invite_all(request) :
    if request.method == "POST" :
        data = {}
        try :
          if request.FILES["invites_image"] is not None :
             if InviteAll.objects.filter(user = request.user ).exists() :
                 data["stat"] = "Failure"
                 data["message"] = "You have already submitted an image "
                 return JsonResponse(data)
             else :
                
                data["stat"] ="Success"
                
                invites = InviteAll.objects.create(user = request.user ,image =request.FILES["invites_image"])
                
                data["image"] = "/media/"+str(invites.image)

                data["message"] = "Image saved successfully"               
                
                 
          else :

             data["message"] = "No file uploaded,Please add a valid file"
             data["stat"] = "Failure"
          return JsonResponse(data)

        except :
            data["message"] = "Try reducing the file size or make sure you have submitted a image"
            data["stat"] = "Failure"
            return JsonResponse(data)
 
    else :
       submissions  = InviteAll.objects.filter(user = request.user).order_by('-pk')
       
       context = {
               'invites' : submissions,
               'invite_active' : True
               }

       return render(request,'ca/invites.html',context)

