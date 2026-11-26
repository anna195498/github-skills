from decimal import Decimal

import pytest
from pydantic import ValidationError

from src.models import RefundRequest


def test_valid_refund_request():
    request = RefundRequest(
        order_id=1,
        reason="Товар пришёл с браком",
        refund_amount=Decimal("49.90"),
    )
    assert request.order_id == 1
    assert request.refund_amount == Decimal("49.90")


def test_short_reason_is_rejected():
    with pytest.raises(ValidationError) as exc_info:
        RefundRequest(order_id=1, reason="брак", refund_amount=Decimal("10"))
    assert "reason" in str(exc_info.value)


@pytest.mark.parametrize("amount", [Decimal("-5"), Decimal("0")])
def test_non_positive_amount_is_rejected(amount):
    with pytest.raises(ValidationError) as exc_info:
        RefundRequest(
            order_id=1,
            reason="Товар пришёл с браком",
            refund_amount=amount,
        )
    assert "refund_amount" in str(exc_info.value)
