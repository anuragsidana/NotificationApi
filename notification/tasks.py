from __future__ import absolute_import

from celery import shared_task



import arrow



# Uses credentials from the TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN
# environment variables
from django.conf import settings

@shared_task
def send_sms_reminder(appointment_id,mssg,user):
    # to prevent recursive import
    from .models import Appointment

    """Send a reminder to a phone using Twilio SMS"""
    # Get our appointment from the database
    try:
        appointment = Appointment.objects.get(pk=appointment_id)
    except Appointment.DoesNotExist:
        # The appointment we were trying to remind someone about
        # has been deleted, so we don't need to do anything
        return

    appointment_time = appointment.time
    # body = 'Hi {0}. You have an appointment coming up at {1}.'.format(
    #     appointment.name,
    #     appointment_time.format('h:mm a')
    # )
    print("xuxxxx")


    # message = client.messages.create(
    #     body=body,
    #     to=appointment.phone_number,
    #     from_=settings.TWILIO_NUMBER,
    # )
