from django.contrib import admin
from .models import Fillup,LoggedIn,Link
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


# Register your models here.
admin.site.register(Fillup)
admin.site.register(LoggedIn)
admin.site.register(Link)
admin.site.unregister(User)
admin.site.unregister(Group)