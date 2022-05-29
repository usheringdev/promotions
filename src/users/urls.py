from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import DefaultRouter

from users.views import UserViewSet, ActivationStatusView, LogOutView, UserDetailsView

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')

urlpatterns = [
    path('login/', obtain_auth_token, name="log_in"),
    path('logout/', LogOutView.as_view(), name="log_out"),
    path('change_activation/<int:pk>/', ActivationStatusView.as_view(), name="activation-status"),
    path('details/', UserDetailsView.as_view(), name="user-details"),
] + router.urls
