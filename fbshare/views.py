from django.shortcuts import render
from django.urls import reverse
from .fbshare import *
from .models import InviteAll, InviteImage
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
        print(request.FILES)
        try :
            if request.FILES is not None :
                    
                if InviteAll.objects.filter(user = request.user ).exists() :
                    data["stat"] = "Failure"
                    data["message"] = "You have already submitted an image "
                    return JsonResponse(data)
                else :
                
                    data["stat"] ="Success"
                    data["images"] =[]
                    invite = InviteAll.objects.create(user = request.user )

                    print(invite)


                    print(request.FILES.getlist("invites_image")[0])
                    # print(request.FILES.getlist("invites_image")[1])
                    print("ABove")


                    for file in request.FILES.getlist("invites_image"):
                        print(file)
                        obj = InviteImage.objects.create(image=file,invite=invite)
                        print("Are you there?")

                        print(obj)
                        print("Bkchdi")
                        data["images"].append("/media/"+str(obj.image))

                    data["message"] = "Images saved successfully"               
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
