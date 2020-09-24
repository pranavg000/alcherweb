from django.contrib import admin
from .models import *

admin.site.register(Tag)
admin.site.register(PagePost)
admin.site.register(UserSharedPost)

# Register your models here.
