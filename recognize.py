# --*-- coding=utf-8 --*--
# Імпорт модулів необхідних для розпізнавання
import pytesseract
import re

# Функція розпізнавання тексту засобами Тесеракт та фільтрація
# тексту за ключовими словами (Номера маклерів)
def get_text(image, lang):
    text = pytesseract.image_to_string(image, lang)
    text__list = text.split('\n')
    result_list = []
    result = []
    tmp_str = ''
    for item in text__list:
        if item.strip() != '':
            tmp_str += ' ' + item
    phones =re.findall('\d{10}', tmp_str)
    # print(phones)

    # Розбиття розпізнаного тексту на окремі оголошення
    for item in range(0, len(phones), 2):
        if item == 0:
            start_index = 0
            end_index = tmp_str.find(phones[item]) + 10
            obj = tmp_str[start_index:end_index]
            tmp_str = tmp_str[end_index:]
        else:
            start_index = tmp_str.find(phones[item-1])+10
            end_index = tmp_str.find(phones[item]) + 10
            if end_index - start_index < 25 or tmp_str[start_index:end_index].strip() == '':
                pass
            else:
                obj = tmp_str[start_index:end_index]
                tmp_str = tmp_str[end_index:]


        result_list.append(obj)

    # Виправлення неточностей розпізнавання
    for item in result_list:
        if item.find('кімн') != -1:
            obj = item[item.find('кімн')-2:]
            obj = obj.replace('жім', 'кім')
            result.append(obj)
            print(obj)
    return result
