from rest_framework.generics import ListAPIView
from drf_spectacular.utils import extend_schema
from .models import Legend
from .serializers import LegendSerializer


class LegendListView(ListAPIView):
    queryset = Legend.objects.all()
    serializer_class = LegendSerializer
    pagination_class = None

    @extend_schema(
        operation_id="listLegends",
        description="Get a list of all available historical legends."
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)