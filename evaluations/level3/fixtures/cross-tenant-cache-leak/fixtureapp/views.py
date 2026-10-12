from django.core.cache import cache
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Customer


class CustomerListView(APIView):
    def get(self, request):
        tenant_id = int(request.headers["X-Tenant-ID"])
        cache_key = "customer-list"
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached)

        payload = list(
            Customer.objects.filter(tenant_id=tenant_id)
            .order_by("id")
            .values("id", "tenant_id", "name")
        )
        cache.set(cache_key, payload, 60)
        return Response(payload)
