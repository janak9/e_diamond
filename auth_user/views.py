from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.contrib.auth.hashers import check_password
from django.utils.encoding import DjangoUnicodeDecodeError
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.urls import reverse
from django.http import HttpResponse
from auth_user.forms import SignUpForm, ProfileForm
from auth_user.models import User as user_model
from auth_user.decorator import checkLogin
from base import const
from base.mail import send_email
from decouple import config
from user.views import get_common_context


def manage_redirect(u_type):
    if u_type == const.USER:
        return redirect('/')
    elif u_type == const.ADMIN:
        return redirect('/main_admin')


def resend_verification_token(request):
    detail = ''
    if request.method == 'POST':
        user = user_model.objects.filter(email=request.POST.get('email')).first()
        if user.exists():
            send_email(user, 'activation')
            detail = "Link send to your mail check your mail"
        else:
            detail = 'User does not exist'
    # print(detail)
    return render(request, 'user/resend_verify.html', {'detail': detail})


def signup(request):
    msg = ""
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_email(user, 'activation')
            msg = "Activation mail is send to your mail please confirm your email."
    else:
        form = SignUpForm()
    u_type = {'user': const.USER}
    return render(request, "user/signup.html", {'form': form, 'u_type': u_type, 'msg': msg})


def login(request):
    if request.user.is_authenticated:
        return manage_redirect(request.user.user_type)

    errors = []
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['pwd']
        user = user_model.objects.filter(email=email)
        if user.exists():
            if user[0].status == const.ACTIVE:
                if user[0].is_active:
                    user = authenticate(
                        request, username=email, password=password)
                    if user is not None:
                        auth_login(request, user)
                        return manage_redirect(user.user_type)
                    else:
                        errors.append('Password is wrong...!')
                else:
                    errors.append("email is not activated. please check your mail and confirm your email. if you don't get mail then <a href=" + reverse('auth:resend-verify') + ">click here<a> to resend mail")
            else:
                errors.append("Your Account Is " + user[0].get_status_display())
        else:
            errors.append('E-mail is wrong...!')

    u_type = {'user': const.USER}
    return render(request, "user/login.html", {'u_type': u_type, 'errors': errors})


def logout(request):
    auth_logout(request)
    return redirect('/')


def verify_account(request, uid, token):
    try:
        user_id = force_text(urlsafe_base64_decode(uid))
        user = get_user_model().objects.get(id=user_id)
    except get_user_model().DoesNotExist:
        detail = 'User does not exist'
    except DjangoUnicodeDecodeError:
        detail = 'Link was expired. Please try to login to resend email verification link.'

    check_token = token_generator.check_token(user, token)

    if check_token:
        user = user
        user.is_active = True
        user.save()
        detail = "your account is activated successfully<br><a href='" + \
                 config('SITE_URL') + reverse('auth:login') + "'>Click Here for Login</a>"
    else:
        send_email(user, 'activation')
        detail = 'Link was expired. Please check your inbox again.'

    return HttpResponse(detail)


@checkLogin('both')
def profile(request):
    context = {'active': 'my_account'}
    get_common_context(request, context)
    context['msg'] = ""
    context['form'] = None
    if request.method == 'POST':
        context['form'] = ProfileForm(request.POST, request.FILES, instance=request.user)
        if context['form'].is_valid():
            context['form'].save()
            context['msg'] = "Profile update successfully"
        else:
            context['msg'] = "Something Wrong Try Again!"

    return render(request, "user/profile.html", context)


def forgot_pwd(request):
    msg = ""
    email = request.POST.get('email')
    user = user_model.objects.filter(email=email).first()
    if request.method == 'POST':
        if user is not None:
            send_email(user, "forgot_password")
            msg = "Forgot Password Link is send to your email, please check you email."

        else:
            msg = "This Email Does Not exist"

    return render(request, "user/forgot_password.html", {'msg': msg})


def verify_forgot_password(request, uid, token):
    msg = ''
    try:
        user_id = force_text(urlsafe_base64_decode(uid))
        user = get_user_model().objects.get(id=user_id)
    except get_user_model().DoesNotExist:
        msg = 'User does not exist'
    except DjangoUnicodeDecodeError:
        msg = 'Link was expired. Please try again by generating new link.'

    if request.method == 'POST':
        confirm_pwd = request.POST.get('confirm_password')
        new_pwd = request.POST.get('new_password')
        if new_pwd == confirm_pwd:
            user.set_password(new_pwd)
            user.save()
            return redirect('auth:login')
        else:
            msg = 'New Password and Confirm Password Must be Same!!! '

    check_token = token_generator.check_token(user, token)
    if check_token:
        return render(request, "user/reset_password.html", {'msg': msg})
    else:
        send_email(user, "forgot_password")
        msg = 'Link was expired. Please check your inbox again.'

    return HttpResponse(msg)


@checkLogin('both')
def change_password(request):
    context = {'active': 'my_account'}
    get_common_context(request, context)
    context['msg'] = ""
    user = user_model.objects.get(id=request.user.id)
    if request.method == "POST":
        if check_password(request.POST.get('current_password'), user.password):
            if check_password(request.POST.get('new_password'), user.password):
                context[
                    'msg'] = "New Password cannot be same as your current password. Please choose a different password."
            else:
                if request.POST.get('new_password') == request.POST.get('confirm_password'):
                    user.set_password(request.POST.get('new_password'))
                    user.save()
                    send_email(user, "change_password")
                    return redirect('auth:login')
                else:
                    context['msg'] = "New Password and Confirm Password Must be Same!!!"
        else:
            context['msg'] = "Current password is Wrong!!!"
    return render(request, "user/change_user_password.html", context)
