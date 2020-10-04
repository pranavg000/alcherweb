from django.shortcuts import redirect
from auths.models import CA_Detail, Profile
from auths.views import register_oauth

def profile_required(func):
    def wrapper_function(request, *args, **kwargs):
        try:
            ca_dets = request.user.ca_details
        except:
            # The user is logging in for the first time
            return redirect('auths:register_oauth')
        if ca_dets.ca_profile_complete and not ca_dets.ca_approval :
            return redirect('ca:pending')
        if not ca_dets.ca_profile_complete :
            return redirect('ca:questionnare')
        return func(request, *args, **kwargs)

    return wrapper_function
