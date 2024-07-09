from .serializers import UserSerializers, BusinessSerializer, BusinessOwnerSerializer
from django.contrib.auth import authenticate
from .models import Business

# rest_framework must be included on settings.INSTALLED_APPS
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly

# rest_framework.auth must be included on settings.INSTALLED_APPS
from rest_framework.authtoken.models import Token

# Default authentication setted for TokenAuthentication on settings. This       
# configuration is made to allow Authentication by Token when using authenticate
#
# REST_FRAMEWORK = {
#   'DEFAULT_AUTHENTICATION_CLASSES': [
#       'rest_framework.authentication.TokenAuthentication',
#   ]
# }


# Registration View: gets a request with email, username, password and image,
# validates fields with serializer and registers the new user if valid. Finally
# responds with a message deppending on result.
class RegistrationView(APIView):
  parser_classes = (MultiPartParser, FormParser)
  serializer_class = UserSerializers
  
  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid():
      serializer.save()
      return Response({'msg': 'Successful registration'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Login View: gets a request with email and password, if any credential is 
# missing an error is thrown. After this tries to authenticate the user, 
# returning None if fails. If successful, returns an auth token.
class LoginView(APIView):
  def post(self, request):
    if 'email' not in request.data or 'password' not in request.data:
      return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
    email = request.POST['email']
    password = request.POST['password']
    
    user = authenticate(request, username=email, password=password)

    if user is not None:
      token, _ = Token.objects.get_or_create(user=user)
      return Response({'msg': 'Login Success', 'token': token.key}, status=status.HTTP_200_OK)
    return Response({'msg': 'Invalid Credentials', 'credentials': [email, password]}, status=status.HTTP_401_UNAUTHORIZED)

# Logout: requires the user to be authenticated and asks for the token on the
# request header (Authorization: Token XXXX).
class LogoutView(APIView):
  permission_classes = [IsAuthenticated]
  def post(self, request):
    request.auth.delete()
    
    return Response({'msg': 'logged out'}, status=status.HTTP_200_OK)
  
class SessionView(APIView):
  permission_classes = [IsAuthenticated]
  serializer_class = UserSerializers

  def get(self, request):
    user = request.user
    return Response({
      'username': user.username, 
      'email': user.email,
      'image_url': user.image_url.url if user.image_url else ""
      }, status=status.HTTP_201_CREATED)


# Business related Views
class BusinessView(APIView):
  permission_classes = [IsAuthenticatedOrReadOnly]
  serializer_class = BusinessSerializer
  
  def get(self, request):
    serializer = BusinessOwnerSerializer(Business.objects.all(), many=True)
    return Response({'businesses': serializer.data}, status=status.HTTP_202_ACCEPTED);
  
  def post(self, request):
    if 'name' not in request.data or 'description' not in request.data:
      return Response({'msg': 'Credentials missing'}, status=status.HTTP_400_BAD_REQUEST)
    name = request.POST['name']
    description = request.POST['description']

    data = {
      "name": name,
      "description": description,
      "user": request.user.id
    }
    serializer = self.serializer_class(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response({'msg': 'Successful business registration'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)