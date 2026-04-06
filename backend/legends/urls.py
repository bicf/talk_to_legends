from django.urls import path
from .views import LegendListView

urlpatterns = [
    path('legends', LegendListView.as_view(), name='legend-list'),
]