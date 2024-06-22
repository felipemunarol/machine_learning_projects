import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'second_project.settings')

import django
django.setup()

# Fake pop script
import random
from second_app.models import AcessosRecord, Webpage, Topic, WebsiteUser
from faker import Faker

fakegen = Faker()
topics = ['Search', 'Social', 'Marketplace', 'News', 'Games']

def add_topic():
    t = Topic.objects.get_or_create(top_name=random.choice(topics))[0]
    t.save()
    return t

def populate(N=5):

    for entry in range(N):

        # Ger the topic for the entry
        top = add_topic()

        fake_url = fakegen.url()
        fake_date = fakegen.date()
        fake_name = fakegen.company()
        fake_user_first_name = fakegen.name()
        fake_user_second_name = fakegen.last_name()
        fake_email = fakegen.email()


        # Create the new webpage entry
        webpg = Webpage.objects.get_or_create(topic=top, url=fake_url, name=fake_name)[0]

        # Create a fake access record for that webpage
        acc_rcd = AcessosRecord.objects.get_or_create(name=webpg, date=fake_date)[0]

        # Create a fake user to that webpage
        user =  WebsiteUser.objects.get_or_create(
            first_name=fake_user_first_name,
            last_name=fake_user_second_name,
            email=fake_email
        )[0]
        user.save()

if __name__ == '__main__':
    print("Populating the database")
    populate()
    print("Finished Populating")