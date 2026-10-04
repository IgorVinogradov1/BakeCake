import os
import json

DB_FILE = 'database.json'


def init_db():
    if not (os.path.exists(DB_FILE)):
        default_data = {
            "users": [],
            "orders": [],
            "cakes": [
                {
                    "name": "Свадебный 'Нежность'",
                    "price": 5000,
                    "img": "images/svadebnui.jpg",
                    "description": "Кремовая эстетика и сочная персиковая пропитка!",
                },
                {
                    "name": "Торт 'Юбилей'",
                    "price": 4500,
                    "img": "images/yubilei.jpg",
                    "description": "Стильный юбилей: сливочная нежность и свежесть ягод!",
                },
                {
                    "name": "Шоколадный 'Брауни'",
                    "price": 3200,
                    "img": "images/brauni.jpg",
                    "description": "Глубокий вкус брауни и яркость свежих ягод!",
                },
                {
                    "name": "Ягодный 'Восторг'",
                    "price": 3800,
                    "img": "images/yagodnui.jpg",
                    "description": "Ягодный восторг в каждой детали!",
                },
                {
                    "name": "Детский 'Карамелька'",
                    "price": 2800,
                    "img": "images/detskii.jpg",
                    "description": "Вкус детства: облачный крем и тягучая карамель!",
                },
                {
                    "name": "Праздничный 'Красный бархат'",
                    "price": 3500,
                    "img": "images/barhat.jpg",
                    "description": "Роскошный «Красный бархат»: классика в каждой детали!",
                },
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
        "delivery_address": None,
        "user_comment": None
    }
    data["orders"].append(order)

    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def update_last_order_data(user_id, phone_number=None, address=None, comment=None):
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for order in reversed(data["orders"]):
        if order["user_id"] == user_id:
            if phone_number is not None:
                order["customer_phone"] = phone_number
            if address is not None:
                order["delivery_address"] = address
            if comment is not None:
                order["user_comment"] = comment
            break

    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)


def cancel_last_order(user_id):
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    order_removed = False
    for order in reversed(data["orders"]):
        if order["user_id"] == user_id:
            data["orders"].remove(order)
            order_removed = True
            break

    if order_removed:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
    return False


def delete_order(user_id, order_num):
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    result = False
    for order in data["orders"]:
        if order["user_id"] == user_id and order["order_num"] == order_num:
            data["orders"].remove(order)
            result = True
            break
    if result:
        with open(DB_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    return result



def show_orders(user_id):
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)
    orders_list = []
    for order in data["orders"]:
        if order["user_id"] == user_id:
            order_text = (
            f'{"*" * 40}\n\n'
            f'Номер заказа: {order["order_num"]}\n\n'
            f'Имя заказчика: {order["customer_name"]}\n'
            f'Номер телефона заказчика: {order["customer_phone"]}\n'
            f'ТГ аккаунт: {order["tg_username"]}\n'
            f'Торт: {order["cake_name"]}\n'
            f'Сумма заказа: {order["cake_price"]}\n'
            f'Адрес доставки: {order["delivery_address"]}\n'
            f'Комментарий: {order["user_comment"]}\n'
            f'{"*" * 40}\n\n'
            )
            orders_list.append(order_text)
    return orders_list