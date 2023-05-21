import json
from datetime import datetime


def write_order_to_json(item, quantity, price, buyer, date):
    with open('orders.json', 'r', encoding='utf-8') as f_r:
        data = json.load(f_r)

    with open('orders.json', 'w', encoding='utf-8') as f_w:
        data['orders'].append({'item': item,
                               'quantity': quantity,
                               'price': price,
                               'buyer': buyer,
                               'date': date})
        json.dump(data, f_w, indent=4)


if __name__ == '__main__':
    write_order_to_json('Платье 35967', '1', '7500', 'Ксения Молчанова', '17-05-2023')
