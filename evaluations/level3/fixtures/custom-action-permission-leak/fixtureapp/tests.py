from django.test import TestCase
from rest_framework.test import APIClient

from .models import Order


class CustomActionPermissionTests(TestCase):
    def setUp(self):
        self.own = Order.objects.create(tenant_id=1, code="OWN")
        self.other = Order.objects.create(tenant_id=2, code="SECRET")

    def test_own_summary_is_visible(self):
        response = APIClient().get(
            f"/orders/{self.own.pk}/summary/",
            HTTP_X_TENANT_ID="1",
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["code"], "OWN")

    def test_other_tenant_summary_is_not_visible(self):
        response = APIClient().get(
            f"/orders/{self.other.pk}/summary/",
            HTTP_X_TENANT_ID="1",
        )
        self.assertEqual(response.status_code, 404)
