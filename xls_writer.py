# --*-- coding=utf-8 --*--
# Імпорт модулів необхідних для запису файлів формату xls
import xlwt
from uuid import uuid4

# Функція збереження відфільтрованого тексту в файл
def writer(ls:list, count_room:int):
    file_neme = str(uuid4().hex)+ '_output.xls'
    wb  =xlwt.Workbook()
    ws = wb.add_sheet(str(count_room)+'кімн.')
    for item in range(len(ls)):
        ws.write(item, 0, ls[item][0])
        ws.write(item, 1, ls[item][1])
    wb.save(file_neme)
    return file_neme

# Функція запису відфільтрованого тексту в файл
def text_writer(ls:list):
    file_neme = str(uuid4().hex)+ '_output.xls'
    wb  =xlwt.Workbook()
    ws = wb.add_sheet('Лист')
    for item in range(len(ls)):
        ws.write(item, 0, ls[item])

    wb.save(file_neme)
    return file_neme