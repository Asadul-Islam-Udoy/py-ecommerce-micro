from api.models import Order, OrderItem
from django.db import transaction
import uuid
from django.core.paginator import Paginator

class OrderService:
    
    
    @staticmethod
    def get_orders(filters, page=1, limit=10):

        queryset = Order.objects.prefetch_related("items").order_by("-created_at")
        user_id = filters.get("user_id")
        status = filters.get("status")

        if user_id:
            queryset = queryset.filter(user_id=user_id)

        if status:
            queryset = queryset.filter(status=status)

        paginator = Paginator(queryset, limit)
        page_obj = paginator.get_page(page)

        return {
            "data": page_obj.object_list,
            "meta": {
                "total": paginator.count,
                "page": page,
                "limit": limit,
                "total_pages": paginator.num_pages
            }
        }
        
    @staticmethod
    def get_order_by_id(order_id):

        try:
            order = (
                Order.objects
                .prefetch_related("items")  # ✅ optimization
                .get(id=order_id)
            )
            return order

        except Order.DoesNotExist:
            return None   
         
    @staticmethod
    @transaction.atomic
    def create_order(user_id, items):
        
        order = Order.objects.create(
            user_id = user_id,
            subtotal = 0,
            total_price = 0,
        )
        
        order_items = []
        total = 0
        
        for item in items:
            item_total = item["price"] * item["quentity"]
            
            order_items.append(
                OrderItem(
                    order=order,
                    product_id=item["product_id"],
                    product_name=item["product_name"],
                    quantity=item["quantity"],
                    price=item["price"],
                    total_price=item_total
                    
                )
            )
            
            total += item_total
            
        
        OrderItem.objects.bulk_create(order_items)

        order.subtotal = total
        order.total_price = total
        order.save()

        return order