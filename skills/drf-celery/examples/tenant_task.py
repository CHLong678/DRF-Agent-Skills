"""Scoped Celery task pattern.

Baseline: Django 3.2+ and Celery 5.0+.
Replace the example model/service imports with project-specific code.
"""

from celery import shared_task
from django.db import transaction

from myapp.models import Customer
from myapp.services import synchronize_customer


def schedule_customer_sync(tenant_id, customer_id):
    """Call after request-layer authorization has been verified."""
    transaction.on_commit(
        lambda: sync_customer.delay(tenant_id, customer_id)
    )


@shared_task(
    bind=True,
    autoretry_for=(ConnectionError,),
    retry_backoff=True,
    max_retries=5,
)
def sync_customer(self, tenant_id, customer_id):
    customer = Customer.objects.get(
        pk=customer_id,
        tenant_id=tenant_id,
    )

    # The external side effect should be idempotent or use a durable
    # idempotency key when duplicate execution is possible.
    synchronize_customer(customer)
