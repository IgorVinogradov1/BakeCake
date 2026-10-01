import json


def main():
    with open('database.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    for order in data['orders']:
        print(
            f"{'*' * 40}\n"
            f"Номер заказа: {order["order_num"]}\n"
            f'Имя заказчика: {order["customer_name"]}\n'
            f'Номер телефона заказчика: {order["customer_phone"]}\n'
            f'Торт: {order["cake_name"]}'
        )


if __name__ == '__main__':
    main()