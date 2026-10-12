from django.test import TestCase
from rest_framework.test import APIClient

from .models import Customer, Order


class OrderListTests(TestCase):
    def setUp(self):
        for index in range(5):
            customer = Customer.objects.create(name=f"Customer {index}")
            Order.objects.create(customer=customer, code=f"ORD-{index}")

    def test_list_has_bounded_query_count_and_same_payload(self):
        client = APIClient()

        with self.assertNumQueries(1):
            response = client.get("/orders/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(
            set(response.data[0]),
            {"id", "code", "customer_name"},
        )
