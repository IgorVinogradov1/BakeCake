import json


def main():
    with open('database.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for order in data['orders']:
        print(
            f'{"*" * 40}\n\n'
            f'Номер заказа: {order["order_num"]}\n\n'
            f'ID заказчика: {order["user_id"]}\n'
            f'Имя заказчика: {order["customer_name"]}\n'
            f'Номер телефона заказчика: {order["customer_phone"]}\n'
            f'Торт: {order["cake_name"]}\n'
            f'Сумма заказа: {order["cake_price"]}'
        )


if __name__ == '__main__':
    main()