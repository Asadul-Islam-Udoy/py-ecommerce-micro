from django.urls import path
from .views import RegisterView,LoginView

urlpatterns = [
    path('', RegisterView.as_view(), name='user-list'),
    path('login/',LoginView.as_view(),name='login')
]