from rest_framework import serializers
from api.models import User

class UserSerializers(serializers.ModelSerializer):
  image_url = serializers.ImageField(required=False)
  class Meta:
    model = User
    fields = '__all__'