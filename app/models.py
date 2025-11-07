from django.db import models
# from django.contrib.auth.models import User



# class Contact_us(models.Model):

#     name = models.CharField(max_length=50)
#     email = models.EmailField()
#     message = models.CharField(max_length=200)

class Project_detail(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=300)
    tech = models.CharField(max_length=100)
    url = models.CharField(max_length=50)

class socialmedia(models.Model):
    linkedin = models.CharField(max_length=500)
    twitter = models.CharField(max_length=500)
    github = models.CharField(max_length=500)
    youtube = models.CharField(max_length=500)

class skill(models.Model):
    skill=models.CharField(max_length=20)
    logo=models.ImageField(upload_to='skill/')

class Aboutsec(models.Model):
    content= models.CharField(max_length=500)

class Profile(models.Model):
    profileimg = models.ImageField(upload_to='Profileimg/',blank=True, null=True)
    resume = models.FileField(upload_to='Resumes/',blank=True, null=True)






