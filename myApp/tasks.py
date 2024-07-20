from celery import shared_task
from time import sleep
from django.core.mail import send_mail


@shared_task
def send_mail_task(recipient_email=None):
     # subject , description,sender email,receiver email
     send_mail("welcome in Hero coders","thank you to registration successfully and welcome to Hero coders world",
               'manikak220@gmail.com',[recipient_email],fail_silently=False)
     return None