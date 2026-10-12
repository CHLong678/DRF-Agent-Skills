from rest_framework.generics import ListAPIView

from .models import Order
from .serializers import OrderSerializer


class OrderListView(ListAPIView):
    serializer_class = OrderSerializer
    queryset = Order.objects.all().order_by("id")
