import pymupdf
import re


def table_cleaner(table):
    clean_table = []
    for row_num in range(len(table)):
        row = table[row_num]
        cleaned_row = [
            item.replace('\n', ' ') if '\n' in item else item
            for item in row
            if item is not None
        ]
        clean_table.append(cleaned_row)
    return clean_table


def num_cleaner(info):
    pattern = r'\d'
    for key in info:
        numbers = info[key]
        for i in range(len(numbers)):
            if re.search(pattern, numbers[i]):
                numbers[i] = int(numbers[i].replace(' ', ''))
    return info


def dict_creator(table):
    pattern = r"1[1-6][0-9][0-1]"
    economic_values = {}
    # Итеративно обходим каждую строку в таблице
    for row_num in range(len(table)):
        row = table[row_num]
        code = next((s for s in row if re.fullmatch(pattern, s)), None)  # Находим код строки (напр. 1150)
        if code is not None:
            code_id = row.index(code)  # Определяем индекс этого кода в списке
            economic_values[code] = row[code_id + 1:]

    return economic_values


doc = pymupdf.open("Бух. отчет Сургутнефтегаз.pdf")
page = doc[0]
tabs = page.find_tables(snap_tolerance=2.5)

print(f"{len(tabs.tables)} found on {page}")  # display number of found tables

if tabs.tables:  # at least one table found?
    tab = tabs[0].extract()
    new_table = table_cleaner(tab)
    res = dict_creator(new_table)
    res = num_cleaner(res)
    print(res)
    print(res.get('1110'))
else:
    print("No tables!")