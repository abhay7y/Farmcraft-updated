from django.shortcuts import render, redirect
# from . import models
from .models import UserProfile
from .models import OwnerProfile
from .models import Crop
from .models import SuggestedCrops
from .models import RentedPlots
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
# Create your views here.


'''
path('admin/', admin.site.urls),
path('', views.startingpage, name="startingpage"),
path('ownerlogin/', views.owner_login, name="owner-login"),
path('usersignup/', views.user_signup, name="user-signup"),
path('userlogin/', views.user_login, name="user-login"),
path('rentplot/', views.rentplot, name="rentplot"),
path('plotdetails/', views.plotdetails, name="plotdetails"),
path('choosecrop/', views.choosecrop, name="choosecrop"),
path('userhome/', views.userhome, name='userhome'),
'''


def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('userhome')
        else:
            return redirect('user-login')
    else:
        return render(request, 'userlogin.html')


'''
o1 password?o1 anc c1 both passwords are testuser
wait
cancel server
createsuperuser
ad
one more superuser?
we deleted the old thingok
superuser created, username - ad, pwd - admin okah? ya yeet
server ples
stop and  start again?
start on cmd thats all
peacedid off


'''


def user_logout(request):
    logout(request)
    return redirect('startingpage')


def owner_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('ownerhome')

        else:
            return redirect('owner-login')
    else:
        return render(request, 'ownerlogin.html')


def owner_logout(request):
    logout(request)
    return redirect('startingpage')


def startingpage(request):
    return render(request, 'startingpage.html')


def user_signup(request):
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        password = data['password']

        # Convert password to hashed password (as Django User model - accepts hashed password)
        hashed_password = make_password(password)
        # insert the user details in the User model
        new_user = User(username=username, password=hashed_password)
        new_user.save()
        # insert the User record in the UserProfile model
        new_userprofile = UserProfile(user=new_user)
        new_userprofile.save()
        # then save it

        '''CHECK THIZ:
        https://djangobook.com/mdj2-models/'''
        return redirect('user-login')
    else:
        return render(request, 'usersignup.html')


def owner_signup(request):
    if request.method == 'POST':
        data = request.POST
        username = data['username']
        location = data['location']
        no_of_plots_owned = data['no_of_plots_owned']
        password = data['password']
        hashed_password = make_password(password)

        new_owner = User(username=username, password=hashed_password)
        new_owner.save()
        new_ownerprofile = OwnerProfile(
            owner=new_owner, location=location, no_of_plots_owned=no_of_plots_owned)
        new_ownerprofile.save()

        owner = User.objects.get(username=username)
        owner_profile = OwnerProfile.objects.get(owner=owner)
        crop1 = data['crop1']
        cost1 = data['cost1']
        crop2 = data['crop2']
        cost2 = data['cost2']
        crop3 = data['crop3']
        cost3 = data['cost3']

        # create the crop here first
        # shreyas after you finish, come to owner home ples.
        crop1_obj = Crop(owner=owner_profile, cropname=crop1, cost=cost1)
        crop2_obj = Crop(owner=owner_profile, cropname=crop2, cost=cost2)
        crop3_obj = Crop(owner=owner_profile, cropname=crop3, cost=cost3)
        crop1_obj.save()
        crop2_obj.save()
        crop3_obj.save()
        return redirect('owner-login')

    else:
        return render(request, 'ownersignup.html')


@login_required
def userhome(request):
    if request.method == 'POST':

        pass
    else:
        return render(request, 'userhome.html')


def ownerhome(request):
    if request.method == 'POST':
        data = request.POST
        owner = request.user
        owner_profile = OwnerProfile.objects.get(owner=owner)
        if 'add_crop' in data.keys():
            cropname = data['cropname']
            cost = data['cost']
            crop_obj = Crop(owner=owner_profile, cropname=cropname, cost=cost)
            crop_obj.save()
        # here create a crop object and save
        if 'edit_suggested_crop' in data.keys():
            suggested_crop1 = data['suggested-crop-1']
            suggested_crop2 = data['suggested-crop-2']
            suggested_crop3 = data['suggested-crop-3']

            crop1_obj = Crop.objects.get(
                owner=owner_profile, cropname=suggested_crop1)

            crop2_obj = Crop.objects.get(
                owner=owner_profile, cropname=suggested_crop2)

            crop3_obj = Crop.objects.get(
                owner=owner_profile, cropname=suggested_crop3)

            try:
                suggested_crop = SuggestedCrops.objects.get(
                    owner=owner_profile)
                suggested_crop.crop1 = crop1_obj
                suggested_crop.crop2 = crop2_obj
                suggested_crop.crop3 = crop3_obj
                suggested_crop.save()
            except:
                newsuggested_crop = SuggestedCrops(
                    owner=owner_profile, crop1=crop1_obj, crop2=crop2_obj, crop3=crop3_obj)
                newsuggested_crop.save()

                # no its a suggested_crop object(meaning for sugggected crop table)
        return redirect('ownerhome')
    else:
        owner = request.user
        owner_profile = OwnerProfile.objects.get(owner=owner)
        rentedplots = RentedPlots.objects.all().filter(owner=owner_profile)
        no_of_plots = owner_profile.no_of_plots_owned
        ownercrops = Crop.objects.all().filter(owner=owner_profile)
        for i in ownercrops:
            print(i.cropname)
        return render(request, 'ownerhome.html', {'rentedplots': rentedplots, 'ownercrops': ownercrops})


@login_required
def rentplot(request):
    if request.method == 'POST':
        data = request.POST
        owner_name = data['Owner']
        # get the owner User record
        # get the owner Profile
        # owner.no_of_plots -= 1
        # owner.save()
        # everytime a customer rents a plot then the owners - number of plots needs to change by -1
        user = request.user
        user_id = user.id
        user_object = User.objects.get(id=user_id)
        user_profile = UserProfile.objects.get(user=user_object)
        owner = User.objects.get(username=owner_name)
        owner_profile = OwnerProfile.objects.get(owner=owner)
        owner_profile.no_of_plots_owned -= 1
        owner_profile.save()

        if 'crop1' in data.keys():
            crop1_name = data['crop1']
            crop1 = Crop.objects.get(owner=owner_profile, cropname=crop1_name)
        else:
            crop1 = ""
        if 'crop2' in data.keys():
            crop2_name = data['crop2']
            crop2 = Crop.objects.get(owner=owner_profile, cropname=crop2_name)
        else:
            crop2 = ""
        if 'crop3' in data.keys():
            crop3_name = data['crop3']
            crop3 = Crop.objects.get(owner=owner_profile, cropname=crop3_name)
        else:
            crop3 = ""

        # ...
        if crop1 == "" and crop2 == "" and crop3 == "":
            return render(request, 'rentplot.html', {'Error': 'no crops selected >> Please choose atleast 1 crop'})
        else:
            if crop1 == '' and crop2 == '':
                rentplot = RentedPlots(
                    user=user_profile, owner=owner_profile, crop3=crop3)
            elif crop2 == '' and crop3 == '':
                rentplot = RentedPlots(
                    user=user_profile, owner=owner_profile, crop1=crop1)
            elif crop1 == '' and crop3 == '':
                rentplot = RentedPlots(
                    user=user_profile, owner=owner_profile, crop2=crop2)
            elif crop1 == '':
                rentplot = RentedPlots(
                    user=user_profile, owner=owner_profile, crop2=crop2, crop3=crop3)
            elif crop2 == '':
                rentplot = RentedPlots(
                    user=user_profile, owner=owner_profile, crop1=crop1, crop2=crop2)
            elif crop3 == '':
                rentplot = RentedPlots(
                    user=user_profile, owner=owner_profile, crop1=crop1, crop2=crop2)
            elif crop1 != '' and crop2 != '' and crop3 != '':
                rentplot = RentedPlots(
                    user=user_profile, owner=owner_profile, crop1=crop1, crop2=crop2, crop3=crop3)
            else:
                pass

        rentplot.save()
        return redirect('userhome')

    else:
        owners = OwnerProfile.objects.all()
        suggested_crops = SuggestedCrops.objects.all()
        info = {}

        for owner in owners:
            for crop_set in suggested_crops:
                if crop_set.owner == owner:
                    if owner.no_of_plots_owned > 0:
                        info[owner] = crop_set
        print(info)
        return render(request, 'rentplot.html', {'info': info})


@login_required
def plotdetails(request):
    user = request.user
    user_profile = UserProfile.objects.get(user=user)
    rented_plots = RentedPlots.objects.all().filter(user=user_profile)
    for i in rented_plots:
        print(i.owner.owner.username)
    return render(request, 'plotdetails.html', {'rented_plots': rented_plots})


@login_required
def choosecrop(request):
    if request.method == 'POST':
        pass
    else:
        return render(request, 'choosecrop.html')

# used when you want to get data from table (one record)
# models.SOMETABLE.objects.get()

# to get all
# models.SOMETABLE.objects.all()

# to put a filter
# models.SOMETABLE.objects.all().filter(the filter is here)


# example : RentedPlot.objects.all().filter(owner=some_owner)


'''
# TODO :
- owner can add suggested crops thru temp>>>>>>temp?
- owner can edit suggested crops thru ownerhome
- owner can add mulitple crops thru ownerhome
'''
