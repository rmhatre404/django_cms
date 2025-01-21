from django.urls import path
from users.views import AuthorRegistrationView, LoginView

urlpatterns = [
    path('register/', AuthorRegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
]


