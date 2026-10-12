from django.db import transaction

from .models import Order


DISPATCHED: list[int] = []


def dispatch_order(order_id: int) -> None:
    DISPATCHED.append(order_id)


def create_order(*, code: str, fail_after_dispatch: bool = False) -> Order:
    with transaction.atomic():
        order = Order.objects.create(code=code)
        dispatch_order(order.id)
        if fail_after_dispatch:
            raise RuntimeError("simulate rollback")
        return order
