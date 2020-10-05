from auths.models import Profile
from social_core.backends.facebook import FacebookOAuth2, FacebookAppOAuth2
from urllib.request import urlopen
from django.template.defaultfilters import slugify


from django.core.files.base import ContentFile

def save_profile(backend, details, response, uid,user, *args, **kwargs):
    
      if backend.__class__ == FacebookOAuth2:
        url = response['picture']['data']['url']
        avatar = urlopen(url)
        print(user,url)
        profile,_ = Profile.objects.get_or_create(user =user)
        profile.profile_image.save(slugify(user.username + " social") + '.jpg',
        ContentFile(avatar.read()))
        profile.save()
