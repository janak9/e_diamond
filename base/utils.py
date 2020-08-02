from django.template.loader import get_template
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.core.validators import RegexValidator
from django.core.mail import EmailMultiAlternatives
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from threading import Thread
from io import BytesIO
from random import randint
import xhtml2pdf.pisa as pisa
import logging
import os

admins_logger = logging.getLogger('admins')


def send_email(user_pk, email_type='activation', message=None, from_pk=None):
    # this start thread there for user don't need to wait until mail send
    t = Thread(target=email_thread, args=(user_pk, email_type, message, from_pk))
    t.start()

def send_email_with_attachment(file: list):
    r = requests.post(
        "https://api.mailgun.net/v3/######/messages",
        auth=("api", "key-########################################"),
        files=[("attachment", (file[0], open(file[1], "rb").read()))],
        data={"from": "No Reply <no-reply@##########>",
              "to": "me@########",
              "subject": "Sales Report",
              "text": "Requested Sales Report",
              "html": "<html>Requested Sales Report</html>"})

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

from django.http import HttpResponse
class Render:

    @staticmethod
    def render(path: str, params: dict):
        template = get_template(path)
        html = template.render(params)
        file_name = "{0}.pdf".format(params['payment'].payment_order.receipt)
        file_path = os.path.join(settings.MEDIA_ROOT, "invoice", file_name)
        response = BytesIO()
        file = open(file_path, "wb")
        pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), file)
        file.close()
        if not pdf.err:
            return HttpResponse(response.getvalue(), content_type='application/pdf')
        else:
            return HttpResponse("Error Rendering PDF", status=400)

    @staticmethod
    def render_to_file(path, params):
        template = get_template(path)
        html = template.render(params)
        file_name = "{0}.pdf".format(params['payment'].payment_order.receipt)
        file_path = os.path.join(settings.MEDIA_ROOT, "invoice", file_name)
        with open(file_path, 'wb') as pdf:
            pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf)
        return [file_name, file_path]
        # return HttpResponse(response.getvalue(), content_type='application/pdf')
