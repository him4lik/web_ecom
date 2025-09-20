from lib.base_classes import BaseModel
from django.db import models
import datetime
from django.forms.models import model_to_dict


class CompanyINFO(BaseModel):
	name = models.CharField(max_length=50)
	tagline = models.CharField(max_length=100)
	logo = models.FileField()
	phone = models.CharField(max_length=10)
	email = models.CharField(max_length=50)
	linkedin = models.CharField(max_length=50)
	twitter = models.CharField(max_length=50)
	instagram = models.CharField(max_length=50)
	address = models.CharField(max_length=200, default='')

	def __str__(self):
		return self.name
