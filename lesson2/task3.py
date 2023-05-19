import yaml

data_to_write = {
    'key 1': ['la', 'la', 'la'],
    'key 2': 5,
    'key 3': {
        'key31': '10 €'
    }
}

with open('file.yaml', 'w', encoding='utf-8') as f:
    yaml.dump(data_to_write, f, default_flow_style=False, allow_unicode=True)

with open('file.yaml', 'r', encoding='utf-8') as f:
    data = yaml.full_load(f)

    for k, v in data.items():
        print(k, ':', v)
