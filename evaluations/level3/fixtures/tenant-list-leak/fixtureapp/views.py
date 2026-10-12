from rest_framework.generics import ListAPIView
from rest_framework.exceptions import ValidationError

from .models import Customer
from .serializers import CustomerSerializer


class CustomerListView(ListAPIView):
    serializer_class = CustomerSerializer

    def get_queryset(self):
        tenant_id = self.request.headers.get("X-Tenant-ID")
        if tenant_id is None:
            raise ValidationError({"tenant": "X-Tenant-ID is required"})
        return Customer.objects.all().order_by("id")
