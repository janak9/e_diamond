from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import get_user_model, authenticate
from user.forms import SignUpForm, ProfileForm
from user.models import User as user_model
from base.utils import send_email
from base import const
from django.utils.encoding import DjangoUnicodeDecodeError
from django.utils.encoding import force_text
from django.contrib.auth.tokens import default_token_generator as token_generator
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse
from django.forms.models import model_to_dict
from django.contrib.auth.hashers import check_password
from user.decorator import checkLogin
from decouple import config


def manage_redirect(u_type):
    if(u_type == const.USER):
        return redirect('/user')
    elif(u_type == const.ADMIN):
        return redirect('/d_admin')


def resend_verification_token(request):
    detail = ''
    if(request.method == 'POST'):
        user = user_model.objects.filter(email=request.POST.get('email'))
        if(user.exists()):
            send_email(user[0].pk)
            detail = "Link send to your mail check your mail"
        else:
            detail = 'User does not exist'
    # print(detail)
    return render(request, 'home/resend_verify.html', {'detail': detail})


def signup(request):
    msg = ""
    if(request.method == 'POST'):
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            send_email(user.pk)
            msg = "Activation mail is send to your mail please confirm your email."
    else:
        form = SignUpForm()
    u_type = {'user': const.USER}
    return render(request, "home/signup.html", {'form': form, 'u_type': u_type, 'msg': msg})


def login(request):
    if request.user.is_authenticated:
        return manage_redirect(request.user.user_type)

    errors = []
    if(request.method == 'POST'):
        email = request.POST['email']
        password = request.POST['pwd']
        user = user_model.objects.filter(email=email)
        if(user.exists()):
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
                    errors.append("not active")
            else:
                errors.append("Your Account Is " +
                              user[0].get_status_display())
        else:
            errors.append('E-mail is wrong...!')

    u_type = {'user': const.USER}
    return render(request, "home/login.html", {'u_type': u_type, 'errors': errors})


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
            config('SITE_URL') + "/user/login/'>Click Here for Login</a>"
    else:
        send_email(user.pk)
        detail = 'Link was expired. Please check your inbox again.'

    return HttpResponse(detail)


@checkLogin('user')
def profile(request):
    msg = ""
    form = None
    if(request.method == 'POST'):
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            user = form.save()
            msg = "Profile update successfully"
        else:
            msg = "Something Wrong Try Again!"

    return render(request, "home/profile.html", {'msg': msg, 'form': form})


def forgot_pwd(request):
    msg = ""
    email = request.POST.get('email')
    user = user_model.objects.filter(email=email).first()
    if request.method == 'POST':
        if user is not None:
            send_email(user.id, "forgot_password")
            msg = "Activation mail is send to your mail please confirm your email."

        else:
            msg = "This Email Does Not exist"

    return render(request, "home/forgot_password.html", {'msg': msg})


def verify_forgot_password(request, uid, token):
    msg = ''
    try:
        user_id = force_text(urlsafe_base64_decode(uid))
        user = get_user_model().objects.get(id=user_id)
    except get_user_model().DoesNotExist:
        msg = 'User does not exist'
    except DjangoUnicodeDecodeError:
        msg = 'Link was expired. Please try again to resend Password Reset link.'

    if(request.method == 'POST'):
        confirm_pwd = request.POST.get('confirm_password')
        new_pwd = request.POST.get('new_password')
        if new_pwd == confirm_pwd:
            user.set_password(new_pwd)
            user.save()
            return redirect('/user/login/')
        else:
            msg = 'Please Enter New Password and Confirm Password Must be Same!!! '

    check_token = token_generator.check_token(user, token)
    if check_token:
        return render(request, "home/reset_password.html", {'msg': msg})
    else:
        send_email(user.pk, "forgot_password")
        msg = 'Link was expired. Please check your inbox again.'

    return HttpResponse(msg)


@checkLogin('user')
def change_password(request):
    msg = ''
    user = user_model.objects.get(id=request.user.id)
    if request.method == "POST":
        if check_password(request.POST.get('current_password'), user.password):
            if check_password(request.POST.get('new_password'), user.password):
                msg = "New Password cannot be same as your current password. Please choose a different password."
            else:
                if request.POST.get('new_password') == request.POST.get('confirm_password'):
                    print(user.id)
                    print(request.POST.get('new_password'))
                    user.set_password(request.POST.get('new_password'))
                    user.save()
                    send_email(user.id, "change_password")
                    return redirect('/user/login/')
                else:
                    msg = "New password and Confirm Password Must be Same!!!"
        else:
            msg = "Current password is Wrong!!!"
    return render(request, "home/change_user_password.html", {"msg": msg})