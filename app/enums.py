from enum import StrEnum

class UserRole(StrEnum):
    ADMIN = "admin"
    STAFF = "staff"
    CUSTOMER = "customer"


# class StockSymbol(StrEnum):
    # AAPL = "AAPL"
    # AMZN = "AMZN"
    # TSLA = "TSLA"
    ...


class AlertCondition(StrEnum):
    ABOVE = "above"  # price > target
    BELOW = "below"  # price < target
    CROSSES_ABOVE = "crosses_above"  # crosses from below to above
    CROSSES_BELOW = "crosses_below"  # crosses from above to below

class TokenType(StrEnum):
    BEARER = "Bearer"