from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('hello-viewset', views.HelloViewSet, basename='hello-viewset')
router.register('profile', views.UserProfileViewSet)
router.register('login', views.LoginViewSet, basename='login')
router.register('feed', views.UserProfileFeedViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('hello-view/', views.HelloView.as_view()),
    path('home', views.home),

]