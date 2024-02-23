from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.http import Http404, HttpResponseServerError
from .models import CustomUser, GeneratedLeadStatus, Recruiter, RecruiterLeadDetails
from django.contrib.auth import get_user_model
from django.utils.crypto import get_random_string
from django_rest_passwordreset.signals import reset_password_token_created
from django.urls import reverse
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import send_mail
from django.core import mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.sites.models import Site
from django.db import transaction
from django.core.exceptions import SuspiciousOperation
from rest_framework.exceptions import ValidationError
# Generate uid from the user's primary key

token_generator = PasswordResetTokenGenerator()


from rest_framework.response import Response
from rest_framework import status

User = get_user_model()
class EmailSendingError(Exception):
    pass
@receiver(pre_save, sender=GeneratedLeadStatus)
def user_created(sender, instance, **kwargs):
    if instance.status == 'accepted':
            email=instance.lead.email
            username = instance.lead.name 
            is_recriuter = True
            password = get_random_string(length=12)
            with transaction.atomic():
                queryset = User.objects.filter(email=email)
                if queryset.exists():
                     raise ValidationError({"details":"Account for this email address already exits!"})
                else:
                      
                    user = User.objects.create_user(email=email, username = username, is_recriuter=is_recriuter, password=password)
                    Recruiter.objects.create(user = user)
                    # Generate token for a user
                    token = token_generator.make_token(user)
                    uid = urlsafe_base64_encode(force_bytes(user.pk))
                    reset_password_link = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})

                    # Get the current site
                    #The code below should be used in production 
                    #current_site = Site.objects.get_current() 

                    # Construct the reset password link with the actual domain
                    #reset_password_link = f"https://{current_site.domain}{reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})}"

                    
                    #For developement
                    reset_password_link = reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token})

                    # Construct the absolute URL using the domain
                    absolute_reset_password_link = f'http://127.0.0.1:8000{reset_password_link}'

                    # Construct the email message
                    email_subject = 'Reset Your Password'
                    email_message = f'Please follow this link to reset your password: {absolute_reset_password_link}'

                    try:
                            connection = mail.get_connection()
                            connection.open()
                            send_mail(
                                email_subject,
                                email_message,
                                'hiregurkha@gmail.com',  # Replace with your 'from' email
                                [user.email],  
                                fail_silently=False
                            )

                            return True  # Indicate successful email sending
                    except:
                         raise EmailSendingError
            

    if instance.status == 'rejected':
          recruiter_lead = RecruiterLeadDetails.objects.get(id=instance.lead.id)
          recruiter_lead.delete()
          raise Http404
    


# @receiver(reset_password_token_created)
# def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
#     """
#     Handles password reset tokens
#     When a token is created, an e-mail needs to be sent to the user
#     :param sender: View Class that sent the signal
#     :param instance: View Instance that sent the signal
#     :param reset_password_token: Token Model Object
#     :param args:
#     :param kwargs:
#     :return:
#     """
#     # send an e-mail to the user
#     context = {
#         'current_user': reset_password_token.user,
#         'username': reset_password_token.user.username,
#         'email': reset_password_token.user.email,
#         'reset_password_url': "{}?token={}".format(
#             instance.request.build_absolute_uri(reverse('password_reset:reset-password-confirm')),
#             reset_password_token.key)
#     }

#     # render email text
#     email_html_message = render_to_string('email/user_reset_password.html', context)
#     email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

#     msg = EmailMultiAlternatives(
#         # title:
#         "Password Reset for {title}".format(title="Some website title"),
#         # message:
#         email_plaintext_message,
#         # from:
#         "noreply@somehost.local",
#         # to:
#         [reset_password_token.user.email]
#     )
#     msg.attach_alternative(email_html_message, "text/html")
#     msg.send()