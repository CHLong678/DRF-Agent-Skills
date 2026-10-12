from django.test import TestCase

from .models import Order
from .services import DISPATCHED, create_order


class CommitBoundaryTests(TestCase):
    def setUp(self):
        DISPATCHED.clear()

    def test_dispatch_happens_after_successful_commit(self):
        with self.captureOnCommitCallbacks(execute=True):
            order = create_order(code="A")

        self.assertEqual(DISPATCHED, [order.id])
        self.assertEqual(Order.objects.count(), 1)

    def test_rollback_does_not_dispatch(self):
        with self.assertRaises(RuntimeError):
            with self.captureOnCommitCallbacks(execute=True):
                create_order(code="B", fail_after_dispatch=True)

        self.assertEqual(DISPATCHED, [])
        self.assertEqual(Order.objects.count(), 0)
