from django.contrib import admin
from  django.contrib.auth.models import User

from .models import Appointment
class AppointmentModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'time']
    list_display_links = ['name']
    list_filter = ['name', 'time']
    search_fields = ['name', 'message']

    class Meta:
        model = Appointment

class UserModelAdmin(admin.ModelAdmin):
    list_display = ['username','email','pk']
    class Meta:
        model=User
admin.site.register(Appointment, AppointmentModelAdmin)
# admin.site.register(User,UserModelAdmin)
