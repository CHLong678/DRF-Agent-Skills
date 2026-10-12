from django.core.cache import cache
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Customer


class CacheIsolationTests(TestCase):
    def setUp(self):
        cache.clear()
        Customer.objects.create(tenant_id=1, name="Tenant 1")
        Customer.objects.create(tenant_id=2, name="Tenant 2")

    def test_cache_is_tenant_scoped(self):
        client = APIClient()
        one = client.get("/customers/", HTTP_X_TENANT_ID="1")
        two = client.get("/customers/", HTTP_X_TENANT_ID="2")

        self.assertEqual([row["tenant_id"] for row in one.data], [1])
        self.assertEqual([row["tenant_id"] for row in two.data], [2])

    def test_second_request_same_tenant_can_use_cache(self):
        client = APIClient()
        first = client.get("/customers/", HTTP_X_TENANT_ID="1")
        second = client.get("/customers/", HTTP_X_TENANT_ID="1")
        self.assertEqual(first.data, second.data)
