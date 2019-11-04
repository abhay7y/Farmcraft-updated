from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class OwnerProfile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=50)
    no_of_plots_owned = models.IntegerField()

    def __str__(self):
        return self.owner.username


class Crop(models.Model):
    cropname = models.CharField(max_length=50)
    cost = models.IntegerField(null=False)
    owner = models.ForeignKey(OwnerProfile, on_delete=models.CASCADE)

    def __str__(self):
        return "{} costs {} --> {}".format(self.cropname, self.cost, self.owner.owner.username)


class SuggestedCrops(models.Model):
    owner = models.ForeignKey(OwnerProfile, on_delete=models.CASCADE)
    crop1 = models.ForeignKey(
        Crop, related_name='crop1', on_delete=models.CASCADE)
    crop2 = models.ForeignKey(
        Crop, related_name='crop2', on_delete=models.CASCADE)
    crop3 = models.ForeignKey(
        Crop, related_name='crop3', on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.owner.owner.username)


class RentedPlots(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    owner = models.ForeignKey(OwnerProfile, on_delete=models.CASCADE)
    #crops = models.ForeignKey(SuggestedCrops, on_delete=models.CASCADE)
    crop1 = models.ForeignKey(
        Crop, related_name='selected_crop1', on_delete=models.CASCADE, blank=True, null=True)
    crop2 = models.ForeignKey(
        Crop, related_name='selected_crop2', on_delete=models.CASCADE, blank=True, null=True)
    crop3 = models.ForeignKey(
        Crop, related_name='selected_crop3', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return "{} rented {}'s plot".format(self.user.user.username, self.owner.owner.username)
