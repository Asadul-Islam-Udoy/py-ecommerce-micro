from django.urls import path
from .views import RegisterView,LoginView,UpdateView

urlpatterns = [
    path('', RegisterView.as_view(), name='user-list'),
    path('login/',LoginView.as_view(),name='login'),
    path('update/<int:user_id>',UpdateView.as_view(),name='user_update')
]