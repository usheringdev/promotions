from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PlanViewSet, PromotionViewSet, CustomerGoalViewSet, RedeemBenefitView

router = DefaultRouter()
router.register('plans', PlanViewSet, basename='plans')
router.register('promotions', PromotionViewSet, basename='promotions')
router.register('customer_goals', CustomerGoalViewSet, basename='customer_goals')

urlpatterns = [
    path('redeem/<uuid:token>/', RedeemBenefitView.as_view(), name='redeem-token')
] + router.urls
