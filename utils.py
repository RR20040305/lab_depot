from datetime import datetime, date

VALID_STATUSES = ("исправно", "в ремонте")


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d").date()
    except ValueError:
        return None


def is_future_or_today(d):
    return d >= date.today()


def validate_status(status):
    return status in VALID_STATUSES
