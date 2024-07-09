from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailBackend(ModelBackend):
  def authenticate(self, request, username=None, password=None, **kwargs):
    usermodel = get_user_model()
    print(username + " " + password)
    try:
      user = usermodel.objects.get(email=username)
    except usermodel.DoesNotExist:
      print("doesnt exist")
      return None

    if user.check_password(password):
      return user
    
    print("check_password didnt work")

  def get_user(self, user_id):
    usermodel = get_user_model()
    try:
      return usermodel.objects.get(pk=user_id)
    except usermodel.DoesNotExist:
      return None