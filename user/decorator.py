from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect, render
from base import const


def checkLogin(type):
    def func(function):
        def wrap(request, *args, **kwargs):
            if(not request.user.is_authenticated):
                return redirect('/user/login')

            if((type == 'user') and (request.user.user_type != const.USER)):
                # raise PermissionDenied
                return render(request, "unauthorized_access.html")
            elif((type == 'admin') and (request.user.user_type != const.ADMIN)):
                #raise PermissionDenied
                return render(request, "unauthorized_access.html")

            return function(request, *args, **kwargs)

        return wrap

    return func
