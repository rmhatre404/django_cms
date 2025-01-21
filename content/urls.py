from django.urls import path
from .views import ContentListCreateView, ContentDetailView

urlpatterns = [
    path('', ContentListCreateView.as_view(), name='content-list-create'),
    path('<int:pk>/', ContentDetailView.as_view(), name='content-detail'),
]
