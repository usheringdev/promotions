from rest_framework import viewsets, views, status
from rest_framework.response import Response

from promotions.permissions import IsCustomer, IsPartner
from .filters import PlanFilterSet, PromotionFilterSet
from .models import Plan, Promotion, CustomerGoal, Benefit
from .pagination import (
    PlanPagination,
    PromotionPagination,
    CustomerGoalPagination
)
from .serializers import (
    PlanSerializer,
    PromotionSerializer,
    CustomerGoalSerializer
)


class PlanViewSet(viewsets.ModelViewSet):
    """."""

    permission_classes = [IsPartner]
    
    http_method_names = ["get", "post", "delete"]
    serializer_class = PlanSerializer
    queryset = Plan.objects.all()
    pagination_class = PlanPagination
    filterset_class = PlanFilterSet

    def perform_destroy(self, plan):
        plan.active = False
        plan.save()
        plan.amounts_and_tenures.all().update(active=False)


class PromotionViewSet(viewsets.ModelViewSet):
    """."""

    permission_classes = [IsPartner]

    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    http_method_names = ["get", "post", "delete"]
    pagination_class = PromotionPagination
    filterset_class = PromotionFilterSet

    def perform_destroy(self, promotion):
        promotion.active = False
        promotion.save()


class CustomerGoalViewSet(viewsets.ModelViewSet):
    """."""

    permission_classes = [IsCustomer]

    queryset = CustomerGoal.objects.all()
    serializer_class = CustomerGoalSerializer
    http_method_names = ["get", "post", "delete"]
    pagination_class = CustomerGoalPagination

    def perform_destroy(self, customer_goal):
        customer_goal.active = False
        customer_goal.save()


class RedeemBenefitView(views.APIView):
    """."""

    permission_classes = [IsCustomer]

    def delete(self, request, *args, **kwargs):
        """."""

        token = kwargs.get("token")
        user_tokens = [cg.benefit.token for cg in request.user.customer_goals.all()]
        if token not in user_tokens:
            return Response({"detail": "Yuo do not own this token"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            benefit = Benefit.objects.get(token=token)
        except Benefit.DoesNotExist:
            return Response({"detail": "This token does not exist"}, status=status.HTTP_400_BAD_REQUEST)
        if not benefit.active:
            return Response({"detail": "This token has already been used"}, status=status.HTTP_400_BAD_REQUEST)
        benefit.active = False
        benefit.save()
        return Response({"detail": "You have redeemed the token successfully."})
