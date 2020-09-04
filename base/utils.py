from django.core.validators import RegexValidator


class MyValidation:
    ALPHA = RegexValidator(r'^[a-zA-Z]*$', 'Enter Only Characters')
    ALPHA_SPACE = RegexValidator(r'^[a-zA-Z ]*$', 'Enter Only Characters or Space')
    ALPHA_NUM = RegexValidator(r'^[0-9a-zA-Z]*$', 'Enter Only Characters Or Number')
    NUM = RegexValidator(r'^[0-9]*$', 'Enter Only Numeric Value')
    PHONE_NO = RegexValidator(r'^\+??\d{10,15}$', "Phone number must be entered in the format: '+XX9999999999'.")


# from django.template.loader import get_template
# from django.http import HttpResponse
# from django.conf import settings
# from io import BytesIO
# import xhtml2pdf.pisa as pisa
# import os
# class Render:
#
#     @staticmethod
#     def render(path: str, params: dict):
#         template = get_template(path)
#         html = template.render(params)
#         file_name = "{0}.pdf".format(params['payment'].payment_order.receipt)
#         file_path = os.path.join(settings.MEDIA_ROOT, "invoice", file_name)
#         response = BytesIO()
#         file = open(file_path, "wb")
#         pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), file)
#         file.close()
#         if not pdf.err:
#             return HttpResponse(response.getvalue(), content_type='application/pdf')
#         else:
#             return HttpResponse("Error Rendering PDF", status=400)
#
#     @staticmethod
#     def render_to_file(path, params):
#         template = get_template(path)
#         html = template.render(params)
#         file_name = "{0}.pdf".format(params['payment'].payment_order.receipt)
#         file_path = os.path.join(settings.MEDIA_ROOT, "invoice", file_name)
#         with open(file_path, 'wb') as pdf:
#             pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf)
#         return [file_name, file_path]
#         # return HttpResponse(response.getvalue(), content_type='application/pdf')
