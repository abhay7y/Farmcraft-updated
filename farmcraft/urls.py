"""farmcraft URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.startingpage, name="startingpage"),
    path('ownerlogin/', views.owner_login, name="owner-login"),
    path('usersignup/', views.user_signup, name="user-signup"),
    path('ownersignup/', views.owner_signup, name="owner-signup"),
    path('userlogin/', views.user_login, name="user-login"),
    path('userlogout/', views.user_logout, name="user-logout"),
    path('rentplot/', views.rentplot, name="rentplot"),
    path('plotdetails/', views.plotdetails, name="plotdetails"),
    path('choosecrop/', views.choosecrop, name="choosecrop"),
    path('userhome/', views.userhome, name='userhome'),
    path('ownerhome/', views.ownerhome, name='ownerhome'),

]
