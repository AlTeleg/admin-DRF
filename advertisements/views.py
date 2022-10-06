from django.db.models import Q
from django.http import request
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet
from advertisements.filters import AdvertisementFilter
from advertisements.models import Advertisement
from advertisements.permissions import IsAdvOwnerOrAdmin
from advertisements.serializers import AdvertisementSerializer


class AdvertisementViewSet(ModelViewSet):
    """ViewSet для объявлений."""

    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = AdvertisementFilter
    permission_classes = [IsAuthenticated, IsAdvOwnerOrAdmin]

    def get_permissions(self):
        """Получение прав для действий."""
        if self.action == "create":
            return [IsAuthenticated()]
        elif self.action in ["update", "partial_update", "delete"]:
            return [IsAdvOwnerOrAdmin()]
        else:
            return []

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Advertisement.objects.filter(
                Q(status="DRAFT", creator=self.request.user) | (Q(status="OPEN") | Q(status="CLOSED"))
            )
        else:
            return Advertisement.objects.filter(
                (Q(status="OPEN") | Q(status="CLOSED"))
            )




