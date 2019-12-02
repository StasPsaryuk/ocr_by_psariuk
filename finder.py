# --*-- coding=utf-8 --*--
# Імпорт модулів необхідних для запису файлів формату xls
import re
import xlrd

# Функція фільтрації розпізнаного тексту за ключовими словами
def sort_list(ls:list):
    result = [[], [], []]
    for item in ls:
        if item.startswith('1-кімн.'):
            result[0].append(item)
        if item.startswith('2-кімн.'):
            result[1].append(item)
        if item.startswith('3-кімн.'):
            result[2].append(item)
    return result

# Функція отримання бази номерів маклерів
def get_tel_rieltors(file:object):
    rielt_list =[]
    index = 1
    wb = xlrd.open_workbook(file)
    sheet = wb.sheet_by_name('Ріелтори')
    vals = [sheet.row_values(rownum) for rownum in range(sheet.nrows)][1:]
    return vals


# Функція пошуку в тексті телефонних номерів
def search(ls:str):
    tel = re.findall('\d{10}', ls)
    if tel:
        return tel
