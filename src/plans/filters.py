from django_filters import rest_framework as filters

from plans.models import Plan, Promotion, BenefitType, CustomerGoal


class PlanFilterSet(filters.FilterSet):
    """."""

    benefit_type = filters.ChoiceFilter(choices=BenefitType.choices)
    active = filters.BooleanFilter()

    class Meta:
        """."""

        model = Plan
        fields = {
            "name": ["icontains"],
            "benefit_percentage": ["lte", "gte"],
        }


class PromotionFilterSet(filters.FilterSet):
    """."""

    class Meta:
        """."""

        model = Promotion
        fields = {
            "name": ["icontains"],
        }
