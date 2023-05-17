# task 1

words_list = ['разработка', 'сокет', 'декоратор']

for word in words_list:
    print(f'{type(word)} - {word}')

words_unicode_list = ['\u0440\u0430\u0437\u0440\u0430\u0431\u043e\u0442\u043a\u0430\u000d',
                      '\u0441\u043e\u043a\u0435\u0442\u000d',
                      '\u0434\u0435\u043a\u043e\u0440\u0430\u0442\u043e\u0440']

for word in words_unicode_list:
    print(f'{type(word)} - {word}')


# task 2

words_list = [b'class', b'function', b'method']

for word in words_list:
    print(f'{type(word)} - {word} - {len(word)}')


# task 3

words_list = ['attribute', 'класс', 'функция', 'type']

for word in words_list:
    print(word.encode('utf-8'))

# or

for word in words_list:
    try:
        print(bytes(word, 'ascii'))
    except UnicodeEncodeError:
        print(f'Слово {word} нельзя представить в виде байтов')


# task 4

words_list = ['разработка', 'администрирование', 'protocol', 'standard']
words_encoded_list = []
words_decoded_list = []

for word in words_list:
    word_encoded = word.encode('utf-8')
    words_encoded_list.append(word_encoded)

print(words_encoded_list)

for word in words_encoded_list:
    word_decoded = word.decode('utf-8')
    words_decoded_list.append(word_decoded)

print(words_decoded_list)


# task 5

import subprocess
import chardet

args1 = ['ping', 'yandex.ru']
args2 = ['ping', 'youtube.com']

subproc_ping_yandex = subprocess.Popen(args1, stdout=subprocess.PIPE)
subproc_ping_youtube = subprocess.Popen(args2, stdout=subprocess.PIPE)


def decode_ping_results(subproc_ping_website):
    for line in subproc_ping_website.stdout:
        code_page = chardet.detect(line)
        line = line.decode(code_page['encoding']).encode('utf-8')
        print(line.decode('utf-8'))


decode_ping_results(subproc_ping_yandex)
decode_ping_results(subproc_ping_youtube)


# task 6

path = 'lesson1/test_file.txt'

with open(path, 'rb') as f:
    print(chardet.detect(f.read())['encoding'])

with open(path, 'rb') as f:
    for line in f:
        print(line.decode('utf-8'))
