from django.shortcuts import render
from django.http import HttpResponse
from second_app.models import Topic, Webpage, AcessosRecord, WebsiteUser
# Create your views here.

def index(request):
    webpages_list = AcessosRecord.objects.order_by('date')
    date_dict = {'access_records': webpages_list}
    return render(request, 'second_app/list.html', context=date_dict)

def help(request):
    my_dict = {'insert_me':"This page is builded to help you with any question that you can have"}
    return render(request, "second_app/help.html", context=my_dict)

def users(request):
    users_dict = {'users_list': WebsiteUser.objects.all()}
    return render(request, "second_app/users_list.html", context=users_dict)