from rest_framework import pagination


class PlanPagination(pagination.PageNumberPagination):
    """."""

    page_size = 10


class PlanAmountTenurePagination(pagination.PageNumberPagination):
    """."""

    page_size = 10


class PromotionPagination(pagination.PageNumberPagination):
    """."""

    page_size = 10


class CustomerGoalPagination(pagination.PageNumberPagination):
    """."""

    page_size = 10
