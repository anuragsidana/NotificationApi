from __future__ import absolute_import

from celery import shared_task



import arrow



# Uses credentials from the TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN
# environment variables
from django.conf import settings

import sendgrid
import os
from sendgrid.helpers.mail import *


# Mail Settings
def build_mail_settings():
    """Build mail settings mock."""
    mail_settings = MailSettings()
    mail_settings.bypass_list_management = BypassListManagement(True)
    mail_settings.footer_settings = FooterSettings(True, "Footer Text",
                                                   ("<html><body><b>Regards</b> <br> "
                                                    "JNU-Support <br>Phone: +91 (22) 2572 2545 </body></html>"))
    mail_settings.sandbox_mode = SandBoxMode(False)
    mail_settings.spam_check = SpamCheck(True, 1,
                                         "https://spamcatcher.sendgrid.com")
    return mail_settings

def get(emails,mssg):
    import sendgrid
    import os








    sg = sendgrid.SendGridAPIClient(apikey="YOUR_API_KEY")
    data = {
        "personalizations": [
            {
                "to": emails
            ,
                "subject": "Sending with SendGrid is Fun"
            }
        ],
        "from": {
            "email": "test@example.com"
        },
        "content": [
            {
                "type": "text/plain",
                "value": mssg
            }
        ]
    }

    # print("mails are "+str(emails))
    response = sg.client.mail.send.post(request_body=data)
    print(response.status_code)
    print(response.body)
    print(response.headers)


@shared_task
def send_sms_reminder(appointment_id):
    print("xuxxxx1")
    # to prevent recursive import
    from .models import Appointment

    """Send a reminder to a phone using Twilio SMS"""
    # Get our appointment from the database
    try:
        print("pk is        "+str(appointment_id))
        appointment = Appointment.objects.get(pk=appointment_id)
    except Appointment.DoesNotExist:
        print("inside")
        # The appointment we were trying to remind someone about
        # has been deleted, so we don't need to do anything
        return

    appointment_time = appointment.time
    body = 'Hi {0}. You have an appointment coming up at {1}.'.format(
        appointment.name,
        appointment_time.format('h:mm a')
    )
    # print("xuxxxx    " +time+"mddg "+mssg)
    emails=[]
    ids=appointment.user_id.all()
    for id in ids:
        mail = {"email": id.email}
        emails.append(mail)

    import json
    json.dumps({'to': emails}, indent=4)
    print("mails are " + str(emails))

    get(emails,appointment.message)

    #response = sg.client.mail.send.post(request_body=mail.get())
    # print(response.status_code)
    # print(response.body)
    # print(response.headers)

    # message = client.messages.create(
    #     body=body,
    #     to=appointment.phone_number,
    #     from_=settings.TWILIO_NUMBER,
    # )
