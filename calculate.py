from datetime import datetime


def check_urgent_delivery(delivery_dte_str):
    try:
        delivery_date = datetime.strptime(delivery_dte_str, '%d.%m.%Y').date()
        today = datetime.now().date()

        days_for_order = (delivery_date - today).days

        if 0 <= days_for_order <= 1:
            return  True

        return False
    except ValueError:
        return False

