from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def index(request):
    my_dict = {'insert_me': "Now I am comming from fist_app/index.html!"}
    return render(request, 'second_app/index.html', context=my_dict)

def help(request):
    my_dict = {'insert_me':"This page is builded to help you with any question that you can have"}
    return render(request, "second_app/help.html", context=my_dict)