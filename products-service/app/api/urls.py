from django.urls import path
from .views import ProductCreateView,ProductDetailView

urlpatterns = [
    path('', ProductCreateView.as_view(), name='product-create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
]