from Cesar import cesar
from CesarDeCrypt import cesarDeCrypt
from Viegener import viegener
from Vernam import vernam
from Globals import CHOICES1, CHOICES2


def shifr(stroka, language, value1, value2, key):
    if CHOICES1[0] == value1:
        if CHOICES2[0] == value2:
            key = int(key)
            return ['Зашифрованный текст:', cesar(stroka, key, language)]
        elif CHOICES2[1] == value2:
            return ['Зашифрованный текст:', viegener(stroka, key, language, 1)]
        else:
            stroka, key = vernam(stroka, language, 1)
            return ['Зашифрованный текст:', stroka, 'Ваш ключ:', key]
    elif CHOICES1[1] == value1:
        if CHOICES2[0] == value2:
            key = int(key)
            return ['Дешифрованный текст:', cesar(stroka, -key, language)]
        elif CHOICES2[1] == value2:
            return ['Дешифрованный текст:', viegener(stroka, key, language, -1)]
        else:
            return ['Дешифрованный текст:', vernam(stroka, language, -1, key)]
    else:
        if CHOICES2[0] == value2:
            return ['Дешифрованный текст:', cesarDeCrypt(stroka, language)]
        else:
            return ['Метод дешифрования без ключа работает только для метода Цезаря!']
