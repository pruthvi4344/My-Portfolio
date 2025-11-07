from django.contrib import admin
# from .models import Contact_us
from .models import Project_detail
from .models import socialmedia
from .models import skill
from .models import Aboutsec,Profile
# Register your models here.
# admin.site.register(Contact_us)
admin.site.register(Project_detail)
admin.site.register(socialmedia)
admin.site.register(skill)

admin.site.register(Profile)
admin.site.register(Aboutsec)
