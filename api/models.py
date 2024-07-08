from django.db import models

class User(models.Model):
  email = models.EmailField(primary_key=True)
  name = models.CharField(max_length=20, )
  password = models.CharField(max_length=20)

class Business(models.Model):
  name = models.CharField(max_length=50, primary_key=True)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  description = models.TextField()

class Product(models.Model):
  business = models.ForeignKey(Business, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  price = models.FloatField()
  description = models.TextField()