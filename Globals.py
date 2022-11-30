import codecs
TOKEN = "5834579102:AAFOF5J9TerzUp3WmIu0YR9ggGzjpzWWaPo"
CHOICES1 = ('Шифрование', 'Дешифрование с ключом', 'Дешифрование без ключа')
CHOICES2 = ('Метод Цезаря', 'Метод Виженера', 'Метод Вернама')
LANGUAGES = ('RU', 'EN')
HELPTEXT = ''
with codecs.open('helper.txt', encoding='utf-8') as f:
    for value in f:
        HELPTEXT += value