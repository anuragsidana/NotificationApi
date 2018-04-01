from django.contrib import admin


from .models import Appointment
class AppointmentModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'time']
    list_display_links = ['name']
    list_filter = ['name', 'time']
    search_fields = ['name', 'message']

    class Meta:
        model = Appointment


admin.site.register(Appointment, AppointmentModelAdmin)
