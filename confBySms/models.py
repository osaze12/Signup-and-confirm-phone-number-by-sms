from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
	
	token = models.CharField(max_length=5, null=True, blank = True)
	is_confirmed = models.BooleanField(default=False)
	day = models.IntegerField( null = True, blank = True)
	month = models.CharField(max_length = 50, null = True, blank = True)
	year = models.IntegerField( null = True, blank = True)
	phone_number = models.IntegerField()
	user = models.OneToOneField(User, on_delete=models.CASCADE)
