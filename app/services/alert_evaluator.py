from decimal import Decimal

from app.enums import AlertCondition
from app.models import Alert


def should_trigger(
        alert: Alert,
        current_price: Decimal,
        previous_price: Decimal | None = None
) -> bool:

    match alert.condition:

        case AlertCondition.ABOVE:
            # trigger whenever price is above the target
            return current_price > alert.target_price

        case AlertCondition.BELOW:
            # trigger whenever price is below the target
            return current_price < alert.target_price

        case AlertCondition.CROSSES_ABOVE:
            # trigger only when price crosses from below to above
            if previous_price is None:
                return False
            was_below_or_at = previous_price <= alert.target_price
            now_above = current_price > alert.target_price

            return was_below_or_at and now_above

        case AlertCondition.CROSSES_BELOW:
            # trigger only when price crosses from above to below
            if previous_price is None:
                return False

            was_above_or_at = previous_price >= alert.target_price
            now_below = current_price < alert.target_price

            return was_above_or_at and now_below

        case _:
            return False