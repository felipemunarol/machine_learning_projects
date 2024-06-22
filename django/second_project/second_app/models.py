from django.db import models
from datetime import date

# Create your models here.

class Topic(models.Model):
    top_name = models.CharField(max_length=264, unique=True)    # Its good to have a leght for the charfield, othewise the costumer can put a long text

    def __str__(self):
        return self.top_name

class Webpage(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    name = models.CharField(max_length=264, unique=True)
    url = models.URLField(unique=True)

    def __str__(self):
        return self.name
    
class AcessosRecord(models.Model):
    name=models.ForeignKey(Webpage, on_delete=models.CASCADE)
    date=models.DateField(default=date.today, blank=True)

    def __str__(self):
        return str(self.date)
    
class WebsiteUser(models.Model):
    first_name=models.CharField(max_length=264, unique=True)
    last_name=models.CharField(max_length=264, unique=True)
    email = models.CharField(max_length=264, unique=True)
    
    def __str__(self):
        return str(self.first_name)