from django.core.management.base import BaseCommand
import random
import datetime
from django.contrib.auth.models import User
from django.core.files import File
from home.models import CompanyINFO


class Command(BaseCommand):
    help = "This command populates db with test data"

    def handle(self, *args, **kwargs):
        CompanyINFO.objects.all().delete()

        with open('media/Logo-Test_t1Pqphm.png', 'rb') as f:
            company_logo = File(f)
            test_company = CompanyINFO.objects.create(
                name='Test Company',
                tagline='Test Tagline',
                email='him4lik@gmail.com',
                logo=company_logo,
                phone='7982117280',
                linkedin='https://www.linkedin.com/',
                twitter='https://www.x.com',
                instagram='https://instagram.com',
                address='test_address, city, state, 111111',
                )
        

        print("Test company created successfully!")

