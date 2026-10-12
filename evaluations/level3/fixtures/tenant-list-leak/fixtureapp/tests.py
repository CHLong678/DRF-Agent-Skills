from django.test import TestCase
from rest_framework.test import APIClient

from .models import Customer


class CustomerListTests(TestCase):
    def setUp(self):
        Customer.objects.create(tenant_id=1, name="Tenant 1 - A")
        Customer.objects.create(tenant_id=1, name="Tenant 1 - B")
        Customer.objects.create(tenant_id=2, name="Tenant 2 - Secret")

    def test_list_is_scoped_to_tenant(self):
        response = APIClient().get("/customers/", HTTP_X_TENANT_ID="1")

        self.assertEqual(response.status_code, 200)
        self.assertEqual([row["tenant_id"] for row in response.data], [1, 1])
        self.assertNotIn("Tenant 2 - Secret", [row["name"] for row in response.data])

    def test_tenant_header_is_required(self):
        response = APIClient().get("/customers/")
        self.assertEqual(response.status_code, 400)
