import os
import json

DB_FILE = 'database.json'


def init_db():
    if not (os.path.exists(DB_FILE)):
        default_data = {
            "users": [],
            "orders": [],
            "cakes": [
                {"name": "Свадебный 'Нежность'", "price": 5000},
                {"name": "Торт 'Юбилей'", "price": 4500},
                {"name": "Шоколадный 'Брауни'", "price": 3200},
                {"name": "Ягодный 'Восторг'", "price": 3800},
                {"name": "Детский 'Карамелька'", "price": 2800},
                {"name": "Праздничный 'Красный бархат'", "price": 3500},
            ]
        }
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_data, f, ensure_ascii=False, indent=4)


def register_new_user(user_id, username, first_name):
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        db_users = json.load(f)
    for user in db_users['users']:
        if user['user_id'] == user_id:
            return
    new_user = {
        "user_id": user_id,
        "username": username,
        "first_name": first_name,
        "agreed_to_terms": False
    }
    db_users['users'].append(new_user)

    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(db_users, f, ensure_ascii=False, indent=4)


def has_user_agreed(user_id):
    if not os.path.exists(DB_FILE):
        return False

    with open(DB_FILE, 'r', encoding='utf-8') as f:
        db_users = json.load(f)

    for user in db_users['users']:
        if user['user_id'] == user_id:
            return user.get('agreed_to_terms', False)
    return False


def save_user_agreement(user_id, username, first_name):
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        db_users = json.load(f)

    for user in db_users['users']:
        if user['user_id'] == user_id:
            user['agreed_to_terms'] = True
            break
    else:
        new_user = {
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "agreed_to_terms": True
        }
        db_users['users'].append(new_user)

    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(db_users, f, ensure_ascii=False, indent=4)


def get_cakes():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    cakes = data['cakes']
    return cakes



def save_cake_order(user_id, cake_name, cake_price, customer_name, customer_phone, tg_username):

    with open(DB_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    order = {
        "order_num": len(data["orders"]) + 1,
        "user_id": user_id,
        "cake_name": cake_name,
        "cake_price": cake_price,
        "customer_name": customer_name,
        "customer_phone": customer_phone,
        "tg_username": tg_username,
    }
    data["orders"].append(order)

    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def update_last_order_phone(user_id, phone_number):
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for order in reversed(data["orders"]):
        if order["user_id"] == user_id:
            order["customer_phone"] = phone_number
            break

    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)