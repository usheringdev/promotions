import uuid

from django.db import models

from users.models import CustomUser


class BenefitType(models.TextChoices):
    """."""

    CASHBACK = 'cashback', 'Cashback'
    VOUCHER = 'voucher', 'Voucher'


class Benefit(models.Model):
    """."""

    token = models.UUIDField(editable=False, default=uuid.uuid4, db_index=True)
    active = models.BooleanField(default=True)
    expiry_date = models.DateTimeField()
    amount = models.DecimalField(decimal_places=2, max_digits=8)


class Plan(models.Model):
    """."""

    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    benefit_percentage = models.IntegerField()
    benefit_type = models.CharField(choices=BenefitType.choices, max_length=255)
    amount = models.DecimalField(decimal_places=2, max_digits=8)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        """."""

        ordering = ["-created_at"]


class PromotionType(models.TextChoices):
    """."""

    NUMBER = 'number', 'Number'
    TIME = 'time', 'Time'


class Promotion(models.Model):
    """."""

    name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    type = models.CharField(choices=PromotionType.choices, max_length=15)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField(null=True)
    num = models.IntegerField(null=True)
    benefit = models.DecimalField(decimal_places=2, max_digits=4)


class CustomerGoal(models.Model):
    """."""

    plan = models.ForeignKey('Plan', on_delete=models.PROTECT, related_name='customer_goals')
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='customer_goals')
    deposited_amount = models.DecimalField(decimal_places=2, max_digits=8)
    started_date = models.DateTimeField()
    promotion = models.ForeignKey('Promotion', on_delete=models.PROTECT, related_name='customer_goals')
    active = models.BooleanField(default=True)
    benefit = models.ForeignKey('Benefit', on_delete=models.PROTECT, related_name='customer_goals')