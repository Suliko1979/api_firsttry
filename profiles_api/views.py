from django.shortcuts import render
from rest_framework.views import APIView, status
from rest_framework.response import Response
from rest_framework import viewsets
from . import serializers
from . import models
from . import permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
import requests

def home(request):
    response = requests.get('http://127.0.0.1:8000/api/profile/').json()
    return render(request, 'home.html', {'response': response})


class HelloView(APIView):
    """test API view"""

    serializer_class = serializers.Hello_serializer

    def get(self, request, format=None):
        an_apiview = [
            'Uses HTTP method as funstion',
            'It is similar to a traditional Django view'
            'Gives you most control'
        ]

        return Response({'message': 'Hello', 'an_apiview': an_apiview})

    def post(self, request):
        """create hello message with our name"""

        serializer = serializers.Hello_serializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)
            return Response({'message': message})
        else:
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        """Updating the object"""
        return Response({'method': 'put'})

    def path(self, request, pn=None):
        """partial update"""
        return Response({'method': 'patch'})

    def delete(self, request, pk=None):
        return Response({'method': 'delete'})

class HelloViewSet(viewsets.ViewSet):
    """test API viewset"""

    serializer_class = serializers.Hello_serializer


    def list(self, request):

        a_viewset = [
            "Uses actions such as CRUD",
            'It automatically maps to URLS',
            'more functionaluty with less codes'
        ]
        return Response({'message': 'Hello', 'a-viewset': a_viewset})

    def create(self, request):
        """Create a new hello message"""

        serializer = serializers.Hello_serializer(data=request.data)

        if serializer.is_valid():
            name = serializer.data.get('name')
            message = 'Hello {0}'.format(name)

            return Response({'message': message})
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        """Getting an object by its ID"""

        return Response({'http_method': 'GET'})

    def update(self, request, pk=None):
        return Response({'http_method': 'PUT'})

    def partial_update(self, request, pk=None):
        return Response({'http_method': 'PATCH'})

    def delete(self, request, pk=None):
        return Response({'http_method': 'DELETE'})

class UserProfileViewSet(viewsets.ModelViewSet):
    """handles creating, updating and deleting profiles"""
    serializer_class = serializers.UserProfileSerializer
    queryset = models.UserProfile.objects.all()
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class LoginViewSet(viewsets.ViewSet):
    """check email and let log in"""
    serializer_class = AuthTokenSerializer

    def create(self, request):
        return ObtainAuthToken().as_view()(request=request._request)


class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles reading, creating and updating profile feed items"""

    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()

    def perform_create(self, serializer):
        """Sets the user profile to the logged in user"""
        serializer.save(user_profile=self.request.user)

