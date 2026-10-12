from django.test import TestCase

from .models import PaymentEffect
from .services import process_charge


class ChargeTests(TestCase):
    def test_duplicate_execution_creates_one_effect(self):
        first = process_charge(idempotency_key="charge-123", amount=500)
        second = process_charge(idempotency_key="charge-123", amount=500)

        self.assertEqual(PaymentEffect.objects.count(), 1)
        self.assertEqual(first.pk, second.pk)
        self.assertEqual(second.amount, 500)

    def test_different_key_creates_distinct_effect(self):
        process_charge(idempotency_key="charge-a", amount=500)
        process_charge(idempotency_key="charge-b", amount=500)

        self.assertEqual(PaymentEffect.objects.count(), 2)
