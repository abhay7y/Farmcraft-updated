from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.OwnerProfile)
admin.site.register(models.UserProfile)
admin.site.register(models.Crop)
admin.site.register(models.SuggestedCrops)
admin.site.register(models.RentedPlots)
