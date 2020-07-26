from django.template.loader import get_template
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import get_user_model
from django.conf import settings
from threading import Thread
import logging
from django.core.validators import RegexValidator

admins_logger = logging.getLogger('admins')


def send_email(user_pk, email_type='activation', message=None, from_pk=None):
    # this start thread there for user don't need to wait until mail send
    t = Thread(target=email_thread, args=(user_pk, email_type, message, from_pk))
    t.start()


def email_thread(user_pk, email_type, message, from_pk):
    try:
        tpl = get_template('mail/verification_email.html')
        subject = 'Activate Your Account'

        user = get_user_model().objects.get(pk=user_pk)

        if email_type == 'forgot_password':
            tpl = get_template('mail/forgot_password_email.html')
            subject = 'Forgot Password'

        if email_type == 'change_password':
            print("change password in util")
            tpl = get_template('mail/change_password.html')
            subject = 'Change Password'

        data = {
            'user': user,
            'token': token_generator.make_token(user),
            'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
            'base_url': settings.SITE_URL
        }

        # if email_type == 'invitation_email':
        #     tpl = get_template('mail/invitation_email.html')
        #     subject = 'Invitation'
        if email_type == 'inform':
            tpl = get_template('mail/inform.html')
            subject = 'E-diamond Updates'
            data['message'] = message
            from_user = get_user_model().objects.get(pk=from_pk)
            data['from_user'] = from_user

        if email_type == 'requestPayment':
            tpl = get_template('mail/reqPayment.html')
            subject = 'E-diamond Updates'
            data['message'] = message
            from_user = get_user_model().objects.get(pk=from_pk)
            data['from_user'] = from_user

        msg = EmailMultiAlternatives(
            subject, '', settings.EMAIL_FROM, [user.email])
        msg.attach_alternative(tpl.render(data), "text/html")
        msg.send()
    except Exception as e:
        admins_logger.exception(e)
        print(e)


class MyValidation():
    ALPHA = RegexValidator(r'^[a-zA-Z]*$', 'Enter Only Characters')
    ALPHA_SPACE = RegexValidator(r'^[a-zA-Z ]*$', 'Enter Only Characters or Space')
    ALPHA_NUM = RegexValidator(r'^[0-9a-zA-Z]*$', 'Enter Only Characters Or Number')
    NUM = RegexValidator(r'^[0-9]*$', 'Enter Only Numeric Value')
    PHONE_NO = RegexValidator(r'^\+??\d{10,15}$', "Phone number must be entered in the format: '+XX9999999999'.")
