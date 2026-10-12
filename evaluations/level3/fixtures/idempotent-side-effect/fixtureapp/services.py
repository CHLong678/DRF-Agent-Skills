from .models import PaymentEffect


def process_charge(*, idempotency_key: str, amount: int) -> PaymentEffect:
    return PaymentEffect.objects.create(
        idempotency_key=idempotency_key,
        amount=amount,
    )
