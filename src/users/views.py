from django.contrib.auth.models import AnonymousUser
from rest_framework import views, viewsets, status
from django.shortcuts import get_object_or_404
from rest_framework.response import Response

from promotions.permissions import IsAdmin, IsPartner, IsCustomer
from users.models import CustomUser
from users.serializers import CustomUserSerializer


class LogOutView(views.APIView):
    """."""

    permission_classes = [IsAdmin | IsPartner | IsCustomer]

    def delete(self, request, *args, **kwargs):
        """."""

        if isinstance(request.user, AnonymousUser):
            return Response({"detail": "You cannot log out."}, status=status.HTTP_400_BAD_REQUEST)
        request.auth.delete()
        return Response({"detail": "You have logged out successfully"}, status=status.HTTP_204_NO_CONTENT)


class UserViewSet(viewsets.ModelViewSet):
    """."""

    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    http_method_names = ["post", "delete"]

    def perform_create(self, serializer):
        """."""

        return CustomUser.objects.create_user(**dict(serializer.validated_data))

    def destroy(self, request, *args, **kwargs):
        """."""

        if self.get_object() != request.user:
            return Response({"detail": "You can only delete your account"}, status=status.HTTP_400_BAD_REQUEST)
        return super(UserViewSet, self).destroy(request, *args, **kwargs)

    def perform_destroy(self, user):
        user.is_active = False
        user.save()


class ActivationStatusView(views.APIView):
    """."""

    permission_classes = [IsAdmin]

    def post(self, request, *args, **kwargs):
        """."""

        user = get_object_or_404(CustomUser, pk=kwargs.get('pk'))
        user.is_active = not user.is_active
        user.save()
        user_status = "activated" if user.is_active else "deactivated"
        return Response({"detail": f"user {user_status} successfully"})


class UserDetailsView(views.APIView):
    """."""

    permission_classes = [IsAdmin | IsPartner | IsCustomer]

    def get(self, request, *args, **kwargs):
        """."""

        user = CustomUserSerializer(request.user)
        return Response({"user": user.data})
