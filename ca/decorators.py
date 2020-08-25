from django.shortcuts import redirect

def profile_required(func):
    def wrapper_function(request, *args, **kwargs):
        ca_dets = request.user.ca_details
        if ca_dets.ca_profile_complete and not ca_dets.ca_approval :
            return redirect('ca:pending')
        if not ca_dets.ca_profile_complete :
            return redirect('ca:questionnare')
        return func(request, *args, **kwargs)

    return wrapper_function