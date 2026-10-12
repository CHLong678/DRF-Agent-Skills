from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Order
from .serializers import OrderSerializer


class OrderViewSet(ReadOnlyModelViewSet):
    serializer_class = OrderSerializer

    def get_queryset(self):
        tenant_id = int(self.request.headers["X-Tenant-ID"])
        return Order.objects.filter(tenant_id=tenant_id)

    @action(detail=True, methods=["get"])
    def summary(self, request, pk=None):
        order = Order.objects.get(pk=pk)
        return Response({"id": order.id, "code": order.code})
