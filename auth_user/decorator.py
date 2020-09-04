from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from base import const


def checkLogin(type):
    def func(function):
        def wrap(request, *args, **kwargs):
            if not request.user.is_authenticated:
                response = HttpResponse(status=302)
                response['Location'] = reverse('auth:login')
                return response
                # return redirect('auth:login')

            if (type == 'user') and (request.user.user_type != const.USER):
                # raise PermissionDenied
                return render(request, "unauthorized_access.html")
            elif (type == 'admin') and (request.user.user_type != const.ADMIN):
                # raise PermissionDenied
                return render(request, "unauthorized_access.html")
            elif (type == 'both') and (request.user.user_type not in [const.ADMIN, const.USER]):
                # admin can also access their own user side
                # raise PermissionDenied
                return render(request, "unauthorized_access.html")

            return function(request, *args, **kwargs)

        return wrap

    return func
