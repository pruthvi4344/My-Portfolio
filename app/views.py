from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from django.db import connection

from django.contrib.auth.decorators import login_required
# from .models import Contact_us
from django.core.mail import send_mail
from .models import Project_detail
from .models import Aboutsec
from .models import socialmedia
from .models import skill,Profile
# from django.contrib.auth import authenticate
def update_about(request, about_id):
    updateabout = get_object_or_404(Aboutsec, id=about_id)
    if not request.session.get('user_id'):
        messages.error(request, "You need to log in to access this page.")
        return redirect('login')
    if request.method == 'POST':
        content= request.POST.get('content')
        if not content:
            messages.error(request, 'all fields are required')
        else:
            updateabout.content = content
            updateabout.save()
            messages.success(request, 'you information is updated')
            return redirect('adminpanel')
    return render(request,'update_about.html',{'updateabout':updateabout})

#skill delete function
def skill_delete(request, skill_id):
    if not request.session.get('user_id'):
        messages.error(request, "You need to log in to access this page.")
        return redirect('login')
    
    skilldelete = skill.objects.get(id=skill_id)
    # print(f"Attempting to delete skill: {skill.skill} (ID: {skill.id})")
    skilldelete.delete()
    messages.success(request, 'Successfully Deleted')
    return redirect('adminpanel')
def update_project(request, project_id):
    project = get_object_or_404(Project_detail, id=project_id)
    if not request.session.get('user_id'):
        messages.error(request, "You need to log in to access this page.")
        return redirect('login')
    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        tech = request.POST.get('tech')
        url = request.POST.get('url')

        if not name or not desc or not tech or not url:
            messages.error(request,'All fields are required')
        else:
            project.name = name
            project.desc = desc
            project.tech = tech
            project.url = url
            project.save()

            messages.success(request, 'Project information updated successfully')
            return redirect('adminpanel')


    return render(request, 'update_project.html', {'project':project})


def delete_project(request, project_id):
    if not request.session.get('user_id'):
        messages.error(request, "You need to log in to access this page.")
        return redirect('login')
    try:
        # Fetch the project by ID
        project = Project_detail.objects.get(id=project_id)
        
        # Log project details for debugging (optional)
        print(f"Attempting to delete project: {project.name} (ID: {project.id})")
        
        # Delete the project from the database
        project.delete()

        # Optionally reset the ID counter (not recommended for production)
        # reset_project_ids()  # Reset the auto-increment ID counter (for SQLite)

        # Provide a success message and redirect back to the admin panel
        messages.success(request, 'Project deleted successfully.')
    except Project_detail.DoesNotExist:
        # Handle case where project does not exist
        messages.error(request, 'Project not found.')

    # Redirect back to admin panel
    return redirect('adminpanel')       


def adminpanel(request):
    sociallinks = socialmedia.objects.first()
    profileimgdetails = Profile.objects.first()
    # print("Session Data:", request.session)
    if request.method =='POST':
        form_type = request.POST.get('form_type')
        if form_type == 'socialmedia':
            if sociallinks:
                messages.error(request, 'social links are already inserted you can only delete or edit them.')
                return redirect('adminpanel')
            else:
             linkedin = request.POST.get('linkedin')
             twitter = request.POST.get('twitter')
             github = request.POST.get('github')
             youtube = request.POST.get('youtube')
            # print(f"links: {linkedin}")
             socialmedia.objects.create(linkedin=linkedin, twitter=twitter, github=github, youtube=youtube)
             messages.success(request, 'Links saved successfully')
             return redirect('adminpanel')

            
        elif form_type == 'projectdetail':
         name = request.POST.get('name')
         desc = request.POST.get('desc')
         tech = request.POST.get('tech')
         url = request.POST.get('url')
         # print(f"Form data: Name: {name}, Desc: {desc}, Tech: {tech}, URL: {url}")

         # Validate that all fields are filled
         if not name or not desc or not tech or not url:
            messages.error(request, "All fields are required.")
            return redirect('adminpanel')

         # Create a new project record
         Project_detail.objects.create(name=name, desc=desc, tech=tech, url=url)
         messages.success(request, 'Project saved successfully!')

         # Redirect to the same page after saving the project
         return redirect('adminpanel')     

        elif form_type =='skill':
            skill_name = request.POST.get('skill')
            logo = request.FILES.get('logo')

            if skill and logo:
              skill.objects.create(skill=skill_name, logo=logo)
              messages.success(request, 'Skill Added')
              return redirect('adminpanel')
            else:
                messages.error(request, 'All fields are required')
                return render(request, 'adminpanel.html')
        
        elif form_type =='profileimg':
            
            profileimg = request.FILES.get('profileimg')
            resume = request.FILES.get('resume')

            if profileimgdetails:
              messages.error(request, 'Profile image Exist. You can only edit or delete')
              return redirect('adminpanel')
            Profile.objects.create(profileimg=profileimg,resume=resume)
            messages.success(request, 'Uploaded Successfully')
            return render(request,'adminpanel.html')

        elif form_type == 'about':
            aboutdata = request.POST.get('content')
            aboutdatas = Aboutsec.objects.all()
    # Prevent duplicate entries
            if Aboutsec.objects.exists():
             messages.error(request, "You can only submit information once.")
             return render(request, 'adminpanel.html', {
            'error_message': "You can only submit 'About Me' information once.",
            'aboutdatas': aboutdatas,  # Pass existing data to the template
            'skills': skill.objects.all(),
            'projects': Project_detail.objects.all(),
        })
            if aboutdata:
                Aboutsec.objects.create(content=aboutdata)
                messages.success(request, 'Information saved successfully')
                return redirect('adminpanel')
            else:
                messages.error(request, 'all fields are required')
                return render(request, 'adminpanel.html')
        

    
        

    if not request.session.get('user_id'):
        messages.error(request, "You need to log in to access this page.")
        return render(request, 'login.html')
        # Check if user is authenticated via session data
    
    


    if 'user_id' in request.session and 'username' in request.session:
        # Retrieve user info from session
        user_id = request.session['user_id']
        username = request.session['username']
        # Get the user from the database
        user = User.objects.get(id=user_id)
        skills = skill.objects.all()
        projects = Project_detail.objects.all()
        # print(aboutus.objects.all())
        aboutdatas = Aboutsec.objects.all()
        return render(request, 'adminpanel.html', {'user': user, 'projects': projects, 'skills':skills, 'aboutdatas':aboutdatas,
                                                   'sociallinks':sociallinks,'profileimgdetails':profileimgdetails})
    else:
        return redirect('login')  # Redirect to login page if not authenticated
    # return render(request, 'adminpanel.html', {'user': request.user})

def home(request):
    
    projects = Project_detail.objects.all()[:3]
    skills = skill.objects.all()
    aboutdata = Aboutsec.objects.first()
    sociallinks = socialmedia.objects.first()
    profileimgdetails = Profile.objects.first()

   
   
    if request.method== 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
       

        subject = "New Contact Form Submission"
        email_message = f"Name: {name}\n\nEmail: {email}\n\nMessage: {message}"
        from_email = 'hurrymargen@gmail.com'
        recipient_list = ['hurrymargen@gmail.com']  # Replace with your email
        
        try:
            send_mail(subject, email_message, from_email, recipient_list)
            messages.success(request, 'I will get back to you soon.')
        except Exception as e:
            messages.error(request, f"Failed to send email, Try again later: {e}")


        return redirect('home')
            

    return render(request, 'index.html',{'projects':projects, 'skills':skills, 'aboutdata':aboutdata, 'sociallinks':sociallinks,'profileimgdetails':profileimgdetails})

def project(request, project_id):

    project = Project_detail.objects.get(id=project_id)
    technologies = [tech.strip() for tech in project.tech.split(",")]
    return render(request, 'project.html',{'project': project, 'technologies' : technologies })

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            # Fetch user from database
            user = User.objects.get(username=username)
            # user = authenticate(request, username=username, password=password)

            # Check if the provided password matches the hashed password
            if check_password(password, user.password):
                # Store user information in session
                request.session['user_id'] = user.id
                request.session['username'] = user.username
                # print(request.user)
                # Redirect to admin panel
                return redirect('adminpanel')
            else:
                messages.error(request, "Incorrect password.")
        except User.DoesNotExist:
            messages.error(request, "User does not exist.")

        # Redirect back to login page on failure
        return redirect('login')

    return render(request, 'login.html')

def user_logout(request):
    # Clear session data
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect('login')

def viewallproject(request):
    projects = Project_detail.objects.all()

    # Retrieve username from session (if logged in)
    # user_username = request.session.get('username', None)
    return render(request, 'viewallproject.html',{'projects' : projects})

def edit_sociallink(request):
    sociallinks = socialmedia.objects.first()

    if request.method == "POST":
        linkedin = request.POST.get('linkedin')
        twitter = request.POST.get('twitter')
        github = request.POST.get('github')
        youtube = request.POST.get('youtube')

        sociallinks.linkedin = linkedin
        sociallinks.twitter = twitter
        sociallinks.github = github
        sociallinks.youtube = youtube

        sociallinks.save()

        messages.success(request, 'Links Are Updated')
        return redirect('adminpanel')
    
    return render(request, 'edit_sociallinks.html', {'sociallinks':sociallinks})

def edit_profileimg(request):
    profileimgdetails = Profile.objects.first()

    if profileimgdetails:
        if request.method == 'POST':
            if 'profileimg' in request.FILES:
             profileimgdetails.profileimg = request.FILES.get('profileimg')
            if 'resume' in request.FILES:
             profileimgdetails.resume = request.FILES.get('resume') 
            profileimgdetails.save()
            messages.success(request,'Updated successfully') 
            return redirect('adminpanel')
    else:
        messages.error(request, 'First Upload Information Afterwards you can edit it')    
        return redirect('adminpanel')
    return render(request, 'edit_profileimg.html',{'profileimgdetails':profileimgdetails})

def delete_profileimg(request):
    profileimgdetails = Profile.objects.first()
    if profileimgdetails:
     profileimgdetails.delete()
     messages.success(request, 'Profile Image Removed Succefully.')
     return redirect('adminpanel')
    else:
        messages.error(request, 'No Image Found to delete')    
        return redirect('adminpanel')
