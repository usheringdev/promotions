from django.utils import timezone

from rest_framework import serializers

from users.models import UserRoleChoices
from .models import Plan, BenefitType, Promotion, PromotionType, CustomerGoal, Benefit


class PlanSerializer(serializers.ModelSerializer):
    """."""

    benefit_type = serializers.ChoiceField(choices=BenefitType.choices)
    end_date = serializers.DateTimeField(required=False)

    class Meta:
        """."""

        model = Plan
        fields = (
            "id",
            "name",
            "active",
            "benefit_percentage",
            "benefit_type",
            "amount",
            "start_date",
            "end_date",
        )


class PromotionSerializer(serializers.ModelSerializer):
    """."""

    type = serializers.ChoiceField(choices=PromotionType.choices)
    end_date = serializers.DateTimeField(required=False)
    active = serializers.BooleanField(required=False)
    num = serializers.IntegerField(required=False)

    def validate(self, attrs):
        """."""

        type = attrs.get("type")
        start_date = attrs.get("start_date")
        end_date = attrs.get("end_date")
        num = attrs.get("num")
        if start_date < timezone.now().astimezone():
            raise serializers.ValidationError(detail={"start_date": "Start date cannot be in past"})
        if type == PromotionType.NUMBER.value and not num:
            raise serializers.ValidationError("You must provide number of promotions for a promotion of type number")
        if type == PromotionType.NUMBER.value and end_date:
            raise serializers.ValidationError("You cannot have an end date for promotion of type number")
        if type == PromotionType.TIME.value and not end_date:
            raise serializers.ValidationError("You must have an end date for promotion of type time")
        if type == PromotionType.TIME.value and num:
            raise serializers.ValidationError("You cannot provide num to a promotion with end date")
        if end_date:
            if end_date < timezone.now().astimezone():
                raise serializers.ValidationError("End must cannot be past time")
            if end_date < start_date:
                raise serializers.ValidationError("End date must be greater than start date")
        return attrs

    class Meta:
        """."""

        model = Promotion
        fields = (
            "type",
            "id",
            "name",
            "active",
            "start_date",
            "end_date",
            "benefit",
            "num",
        )


class BenefitSerializer(serializers.ModelSerializer):
    """."""

    class Meta:
        """."""

        model = Benefit
        fields = (
            "token",
            "active",
            "expiry_date",
            "amount"
        )


class CustomerGoalSerializer(serializers.ModelSerializer):
    """."""

    active = serializers.BooleanField(required=False)
    benefit = BenefitSerializer(read_only=True)

    def validate(self, attrs):
        """."""

        plan = attrs.get("plan")
        user = attrs.get("user")
        deposited_amount = attrs.get("deposited_amount")
        started_date = attrs.get("started_date")
        promotion = attrs.get("promotion")

        if not plan.active:
            raise serializers.ValidationError("Plan is not active")
        if plan.end_date is not None and plan.end_date < timezone.now().astimezone():
            raise serializers.ValidationError("Plan has expired")
        if plan.start_date > timezone.now().astimezone():
            raise serializers.ValidationError("Plan has not started yet.")
        if deposited_amount <= 0:
            raise serializers.ValidationError("Deposited amount must be greater than zero")
        if started_date < timezone.now().astimezone():
            raise serializers.ValidationError("Start time must not be in the past")
        if not promotion.active:
            raise serializers.ValidationError("Promotion is not active")
        if promotion.start_date > timezone.now().astimezone():
            raise serializers.ValidationError("Promotion has not started yet.")
        if user.role != UserRoleChoices.CUSTOMER.value:
            raise serializers.ValidationError("Goals can only be created for a customer")
        request = self.context.get("request")
        if request.user != user:
            raise serializers.ValidationError("You can create only your own customer goals")
        promotions = [c_goal.promotion for c_goal in user.customer_goals.all()]
        if promotion in promotions:
            raise serializers.ValidationError("You have already used this promotion")
        return attrs

    def create(self, validated_data):
        """."""

        plan = validated_data.get("plan")
        user = validated_data.get("user")
        promotion = validated_data.get("promotion")
        CustomerGoal.objects.filter(plan=plan, user=user).update(active=False)
        amount = (plan.benefit_percentage + promotion.benefit) * plan.amount / 100
        benefit = Benefit.objects.create(amount=amount, expiry_date=timezone.now().astimezone() + timezone.timedelta(days=60))
        validated_data.update({"benefit": benefit})
        return super(CustomerGoalSerializer, self).create(validated_data)

    class Meta:
        """."""

        model = CustomerGoal
        fields = (
            "id",
            "plan",
            "user",
            "deposited_amount",
            "started_date",
            "promotion",
            "active",
            "benefit",
        )
