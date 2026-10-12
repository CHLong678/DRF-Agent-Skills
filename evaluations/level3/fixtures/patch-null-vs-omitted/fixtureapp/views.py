from rest_framework.generics import RetrieveUpdateAPIView

from .models import Customer
from .serializers import CustomerSerializer


class CustomerDetailView(RetrieveUpdateAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
