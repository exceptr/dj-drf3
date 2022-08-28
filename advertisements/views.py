from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from advertisements.models import Advertisement
from advertisements.permissions import IsOwner
from advertisements.serializers import AdvertisementSerializer


class AdvertisementCreatorSearchFilter(SearchFilter):
    search_param = 'creator'


class AdvertisementFilter(filters.FilterSet):
    created_at = filters.DateFromToRangeFilter()
    status = filters.Filter()

    class Meta:
        model = Advertisement
        fields = ['created_at', 'status']


class AdvertisementViewSet(ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    filter_backends = [AdvertisementCreatorSearchFilter, DjangoFilterBackend, SearchFilter]
    search_fields = ['creator__id']
    filterset_class = AdvertisementFilter

    def get_permissions(self):
        """Получение прав для действий."""
        if self.request.method in ['POST', 'DELETE', 'PATCH']:
            return [IsOwner()]
        return []