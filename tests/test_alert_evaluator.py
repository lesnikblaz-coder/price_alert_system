from decimal import Decimal
from unittest.mock import MagicMock

from app.enums import AlertCondition
from app.models import Alert
from app.services.alert_evaluator import should_trigger

def create_alert(condition: AlertCondition, target: str) -> Alert:
    alert = MagicMock(spec=Alert)
    alert.condition = condition
    alert.target_price = Decimal(target)

    return alert

def test_above_when_price_above_target():
    alert = create_alert(AlertCondition.ABOVE, "50000")

    assert should_trigger(alert, Decimal("60000")) is True

def test_above_when_price_below_target():
    alert = create_alert(AlertCondition.ABOVE, "50000")

    assert should_trigger(alert, Decimal("40000")) is False

def test_crosses_above_triggers_only_at_moment_of_crossing():
    alert = create_alert(AlertCondition.CROSSES_ABOVE, "50000")

    assert should_trigger(alert, Decimal("51000"), Decimal("49000")) is True

    assert should_trigger(alert, Decimal("51000"), Decimal("50500")) is False

def test_crosses_above_returns_false_without_previous_price():
    alert = create_alert(AlertCondition.CROSSES_ABOVE, "50000")
    
    assert should_trigger(alert, Decimal("51000"), None) is False

def test_crosses_below_triggers_only_at_moment_of_crossing():
    alert = create_alert(AlertCondition.CROSSES_BELOW, "50000")

    assert should_trigger(alert, Decimal("49000"), Decimal("51000")) is True

    assert should_trigger(alert, Decimal("49000"), Decimal("49500")) is False