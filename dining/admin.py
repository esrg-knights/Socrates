# Register your models here.
from django.contrib import admin

from .models import *

admin.site.register(DiningList)
admin.site.register(DiningParticipation)
admin.site.register(DiningStats)
