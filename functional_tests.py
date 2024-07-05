import pymupdf
import re
from pprint import pprint


def table_cleaner(table):
    for row_num in range(len(table)):
        row = table[row_num]
        cleaned_row = [
            item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item
            for item in row]
        print(cleaned_row)


def dict_creator(table):
    pattern = r"1[1-6][0-9][0-1]"
    economic_values = {}
    # Итеративно обходим каждую строку в таблице
    for row_num in range(len(table)):
        row = table[row_num]
        code = [s for s in row if re.fullmatch(pattern, s)]
        code_id = row.find(code)
        economic_values[code[0]] = row[code_id + 1:]
    return economic_values


def table_converter(table):
    table_string = ''
    # Итеративно обходим каждую строку в таблице
    for row_num in range(len(table)):
        row = table[row_num]
        # Удаляем разрыв строки из текста с переносом
        cleaned_row = [
            item.replace('\n', ' ') if item is not None and '\n' in item else 'None' if item is None else item
            for item in row]
        # Преобразуем таблицу в строку
        table_string += ('|' + '|'.join(cleaned_row) + '|' + '\n')
    # Удаляем последний разрыв строки
    table_string = table_string.replace("|None", '')[:-1]
    return table_string


doc = pymupdf.open("Бух. отчет Сургутнефтегаз.pdf")
page = doc[0]
tabs = page.find_tables(snap_tolerance=2.5)

print(f"{len(tabs.tables)} found on {page}")  # display number of found tables

if tabs.tables:  # at least one table found?
    tab = tabs[0].extract()
    # pprint(tab)  # print content of first table
    # res = table_converter(tab)
    # res = dict_creator(tab)
    # print(res)
    table_cleaner(tab)
else:
    print("No tables!")
