from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode
from threading import Thread
from decouple import config
from main_admin.models import AboutUs
import logging

admins_logger = logging.getLogger('admins')


def send_email(user, email_type='activation', *args, **kwargs):
    # this start thread there for user don't need to wait until mail send
    t = Thread(target=email_thread, args=(user, email_type, *args), kwargs=kwargs)
    t.start()


# def send_email_with_attachment(file: list):
#     r = requests.post(
#         "https://api.mailgun.net/v3/######/messages",
#         auth=("api", "key-########################################"),
#         files=[("attachment", (file[0], open(file[1], "rb").read()))],
#         data={"from": "No Reply <no-reply@##########>",
#               "to": "me@########",
#               "subject": "Sales Report",
#               "text": "Requested Sales Report",
#               "html": "<html>Requested Sales Report</html>"})


def email_thread(user, email_type, *args, **kwargs):
    try:
        about_us = AboutUs.objects.first()
        emails = []
        data = {
            'user': user,
            'app_name': config('APP_NAME'),
            'base_url': settings.SITE_URL,
            'about_us': about_us
        }

        if email_type == 'forgot_password':
            email_template = get_template('mail/forgot_password.html')
            subject = 'Forgot Password'
            data['token'] = token_generator.make_token(user)
            data['uid'] = force_text(urlsafe_base64_encode(force_bytes(user.pk)))
            emails.append(user.email)
        elif email_type == 'contact':
            email_template = get_template('mail/contact.html')
            subject = 'Request for ' + kwargs['contact'].get_contact_type_display()
            data['contact'] = kwargs['contact']
            for u in user: emails.append(u.email)
        elif email_type == 'contact_reply':
            email_template = get_template('mail/contact_reply.html')
            subject = 'Reply of ' + kwargs['contact'].get_contact_type_display()
            data['contact'] = kwargs['contact']
            data['reply'] = kwargs['reply']
            emails.append(kwargs['contact'].email)
        elif email_type == 'change_password':
            email_template = get_template('mail/change_password.html')
            subject = 'Change Password'
            emails.append(user.email)
        elif email_type == 'order_user':
            email_template = get_template('mail/order_user.html')
            subject = 'Your ' + data['app_name'] + ' order #' + kwargs['payment_order'].receipt
            data['payment_order'] = kwargs['payment_order']
            emails.append(user.email)
        elif email_type == 'order_admin':
            email_template = get_template('mail/order_admin.html')
            subject = 'You got new order #' + kwargs['payment_order'].receipt
            data['payment_order'] = kwargs['payment_order']
            for u in user: emails.append(u.email)
        else:
            email_template = get_template('mail/verification.html')
            subject = 'Activate Your Account'
            data['token'] = token_generator.make_token(user)
            data['uid'] = force_text(urlsafe_base64_encode(force_bytes(user.pk)))
            emails.append(user.email)

        # if email_type == 'inform':
        #     email_template = get_template('mail/inform.html')
        #     subject = 'E-diamond Updates'
        #     data['message'] = message
        #     from_user = get_user_model().objects.get(pk=from_pk)
        #     data['from_user'] = from_user

        # if email_type == 'requestPayment':
        #     email_template = get_template('mail/reqPayment.html')
        #     subject = 'E-diamond Updates'
        #     data['message'] = message
        #     from_user = get_user_model().objects.get(pk=from_pk)
        #     data['from_user'] = from_user

        msg = EmailMultiAlternatives(
            subject, '', settings.EMAIL_FROM, emails)
        msg.attach_alternative(email_template.render(data), "text/html")
        msg.send()
    except Exception as e:
        admins_logger.exception(e)
        print(e)
