from django.test import TestCase
from rest_framework.test import APIClient

from .models import Customer


class PatchTests(TestCase):
    def setUp(self):
        self.customer = Customer.objects.create(name="Old", note="keep me")

    def test_omitted_note_is_preserved(self):
        response = APIClient().patch(
            f"/customers/{self.customer.pk}/",
            {"name": "New"},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.customer.refresh_from_db()
        self.assertEqual(self.customer.name, "New")
        self.assertEqual(self.customer.note, "keep me")

    def test_explicit_null_clears_note(self):
        response = APIClient().patch(
            f"/customers/{self.customer.pk}/",
            {"note": None},
            format="json",
        )
        self.assertEqual(response.status_code, 200)
        self.customer.refresh_from_db()
        self.assertIsNone(self.customer.note)
