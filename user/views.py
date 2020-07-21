from django.shortcuts import render, redirect

def home(request):
    return render(request, 'user/index.html', {'title': 'test'})
