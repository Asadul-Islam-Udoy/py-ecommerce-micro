from django.urls import path
from .views import RegisterView,LoginView,UpdateView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/',LoginView.as_view(),name='login'),
    path('update/<int:user_id>',UpdateView.as_view(),name='user_update')
]