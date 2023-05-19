import csv
import re
import chardet


def get_data(*args):
    main_data = [['Изготовитель системы', 'Название ОС', 'Код продукта', 'Тип системы']]
    os_prod_list = []
    os_name_list = []
    os_code_list = []
    os_type_list = []

    os_prod_regex = r'(Изготовитель системы:)(.*)'
    os_name_regex = r'(Название ОС:)(.*)'
    os_code_regex = r'(Код продукта:)(.*)'
    os_type_regex = r'(Тип системы:)(.*)'

    for file in args:
        with open(file, 'rb') as f:
            encoding = chardet.detect(f.read())['encoding']

        with open(file, 'r', encoding=encoding) as f:
            data = f.read()
            os_prod = re.search(os_prod_regex, data)[2].split()[0]
            os_name = re.search(os_name_regex, data)[2].split()[0]
            os_code = re.search(os_code_regex, data)[2].split()[0]
            os_type = re.search(os_type_regex, data)[2].split()[0]

            os_prod_list.append(os_prod)
            os_name_list.append(os_name)
            os_code_list.append(os_code)
            os_type_list.append(os_type)

    for os_prod, os_name, os_code, os_type in zip(os_prod_list, os_name_list, os_code_list, os_type_list):
        main_data.append([os_prod, os_name, os_code, os_type])

    return main_data


def write_to_csv(file_url, *args):
    data_to_write = get_data(*args)

    with open(file_url, 'w', encoding='utf-8') as f:
        f_writer = csv.writer(f)
        for row in data_to_write:
            f_writer.writerow(row)


if __name__ == '__main__':
    write_to_csv('report.csv', *['info_1.txt', 'info_2.txt', 'info_3.txt'])
