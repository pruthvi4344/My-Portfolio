from django.urls import path
from .import views

urlpatterns = [
    path('', views.home, name='home'),
    path('project/<int:project_id>/', views.project, name='project'),
    path('login', views.user_login, name='login'),
    path('adminpanel',views.adminpanel, name='adminpanel'),
    path('logout',views.user_logout, name='logout'),
    path('viewallproject', views.viewallproject, name='viewallproject'),
    path('socialmedia', views.socialmedia, name='socialmedia'),
    path('delete_project/<int:project_id>/', views.delete_project, name='delete_project'),
    path('update_project/<int:project_id>/', views.update_project, name='update_project'),
    # path('skill', views.skill, name='skill'),
    path('skill_delete/<int:skill_id>/', views.skill_delete, name='skill_delete'),
    path('update_about/<int:about_id>/', views.update_about, name='update_about'),
    path('edit/sociallinks', views.edit_sociallink, name='edit_sociallink'),
    path('edit/profile-image', views.edit_profileimg, name='edit_profileimg'),
    path('Delete/profile-image', views.delete_profileimg, name='delete_profileimg'),
]