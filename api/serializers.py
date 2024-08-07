from rest_framework import serializers
from api.models import User, Business

# The Serializers transform models into native Python datatypes for easy
# convertion into JSON.
# Create method is necessary for managing our custom User model.


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'image_url', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            **self.validated_data
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class BusinessSerializer(serializers.ModelSerializer):

    user = UserSerializers(read_only=True)

    class Meta:
        model = Business
        fields = "__all__"


class BusinessOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = "__all__"
