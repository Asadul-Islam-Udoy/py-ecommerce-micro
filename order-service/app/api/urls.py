
from django.urls import path
from .views import OrderView, SingleOrderView
urlpatterns = [
    path('',OrderView.as_view(),name='order'),
    path("<uuid:order_id>/", SingleOrderView.as_view()),
]
