from rest_framework import serializers

from plans.serializers import CustomerGoalSerializer
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """."""

    customer_goals = CustomerGoalSerializer(many=True, read_only=True)

    class Meta:
        """."""

        model = CustomUser
        fields = (
            "username",
            "role",
            "id",
            "password",
            "customer_goals",
        )
        extra_kwargs = {
            "password": {
                "write_only": True
            },
        }
