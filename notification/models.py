from __future__ import unicode_literals




from django.conf import settings
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
import datetime

import arrow



class Appointment(models.Model):
    name = models.CharField(max_length=150)
    # phone_number = models.CharField(max_length=15)

    user_id = models.ManyToManyField('auth.User')
    message=models.CharField(max_length=250)
    date=models.CharField(max_length=20)
    time = models.CharField(max_length=20)


    owner = models.ForeignKey('auth.User', related_name='nots', on_delete=models.CASCADE)


    # Additional fields not visible to users

    task_id = models.CharField(unique=False,max_length=50, blank=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'Appointment #{0} - {1}'.format(self.pk, self.name)

    def get_absolute_url(self):
        return reverse('view_appointment', args=[str(self.id)])

    def clean(self):
        """Checks that appointments are not scheduled in the past"""

        time=datetime.datetime.strptime((self.date+" "+self.time), "%Y-%m-%d %H:%M:%S")
        appointment_time = arrow.get(time, settings.TIME_ZONE)

        if appointment_time < arrow.utcnow():
            raise ValidationError('You cannot schedule an appointment for the past. Please check your time and time_zone')



    def schedule_reminder(self):
        try:
            user_id = self.user_id
        except Exception:
            print("Error haiiiii")
        # emails=[]
        #
        # ids=self.pk
        # ids = self.user_id.all()

        # for id in ids:
        #     mail = { "email": id.email}
        #     emails.append(mail)

        # import  json
        # json.dumps({'to':emails},indent=4)

        """Schedules a Celery task to send a reminder about this appointment"""
        time = datetime.datetime.strptime((self.date + " "+self.time), "%Y-%m-%d %H:%M:%S")
        # Calculate the correct time to send this reminder
        appointment_time = arrow.get(time, settings.TIME_ZONE)
        # reminder_time = appointment_time.replace(minutes=-settings.REMINDER_TIME)

        # Schedule the Celery task
        from .tasks import send_sms_reminder
        result = send_sms_reminder.apply_async((self.pk,), eta=appointment_time)

        return result.id



    def save(self, *args, **kwargs):
        # from Nots.settings import celery_app
        from  Nots.celery import app as celery_app
        """Custom save method which also schedules a reminder"""
        # ids=self.user_id.all()

        print("key iss       "+str(self.pk))
        # Check if we have scheduled a reminder for this appointment before
        if self.task_id:
            # Revoke that task in case its time has changed
            celery_app.control.revoke(self.task_id)

        # Save our appointment, which populates self.pk,
        # which is used in schedule_reminder
        super(Appointment, self).save(*args, **kwargs)

        # Schedule a new reminder task for this appointment
        self.task_id = self.schedule_reminder()

        # Save our appointment again, with the new task_id
        # super(Appointment, self).save(*args, **kwargs)

        # print("iddddddddddd          "+str(self.pk))
