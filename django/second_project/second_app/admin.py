from django.contrib import admin
from second_app.models import AcessosRecord, Topic, Webpage, WebsiteUser

# Register your models here.
admin.site.register(AcessosRecord)
admin.site.register(Topic)
admin.site.register(Webpage)
admin.site.register(WebsiteUser)

