from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.utils import timezone

# Returns file direction


def upload_to(instance, filename):
    return 'images/{filename}'.format(filename=filename)

# Custom User Manager for overwritting native Django implementation.
# Reason: Create users without firstName and lastName; email as authentication
# field; image_url as extra field


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)

# Custom User with every relevant field. Objects points to UserManager for data
# management.


class User(AbstractBaseUser):
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Business(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image_url = models.ImageField(upload_to=upload_to, blank=True, null=True)
    description = models.TextField()


class Product(models.Model):
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    price = models.FloatField()
    description = models.TextField()
