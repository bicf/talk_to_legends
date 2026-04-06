from django.urls import path
from .views import SessionDetailView, SessionStartView, SessionMessageView

urlpatterns = [
    path('session/', SessionStartView.as_view(), name='session-start'),
    path('session/<uuid:session_id>', SessionDetailView.as_view(), name='session-detail'),
    path('session/<uuid:session_id>/message', SessionMessageView.as_view(), name='session-message'),
]