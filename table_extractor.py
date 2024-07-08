import pymupdf
import re
from aspose.cells import Workbook


# Преобразование xlx файлов в pdf
def xlx_to_pdf(filename_in, filename_out):
    workbook = Workbook(filename_in)
    workbook.save(filename_out)


# def search_page_of_balance(doc, keyword):
#     for i in range(doc.page_count):
#         page = doc[i]
#         page_ocr = page.get_textpage_ocr(flags=3, language='rus', dpi=72, full=False,
#                                          tessdata="E:/PO/Tesseract/tessdata")
#         text = page_ocr.extractText()
#         if keyword in text:
#             return i

# Очистка извлеченных строк таблицы от посторонних символов
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


# Преобразование извлеченных значений показателей в числа
def num_cleaner(info):
    pattern = r'\d'
    for key in info:
        numbers = info[key]
        for i, item in enumerate(numbers):
            if re.search(pattern, item):
                cleaned_number = item.replace(' ', '')
                if cleaned_number[0] == '-':
                    numbers[i] = -int(cleaned_number[2:-1])
                else:
                    numbers[i] = int(cleaned_number)
    return info


# Создание словаря со строками показателей
def dict_creator(table):
    pattern = r"[1-2][1-7][0-9][0-2]"
    economic_values = {}
    # Итеративно обходим каждую строку в таблице
    for row_num in range(len(table)):
        row = table[row_num]
        code = next((s for s in row if re.fullmatch(pattern, s)), None)  # Находим код строки (напр. 1150)
        if code is not None:
            code_id = row.index(code)  # Определяем индекс этого кода в списке
            economic_values[code] = row[code_id + 1:]

    return economic_values


filename_in = 'xlx\Отчет о финансовых результатах. Лист 1.xls'
filename_out = "Convert.pdf"
xlx_to_pdf(filename_in, filename_out)

doc = pymupdf.open(filename_out)
# num_page = search_page_of_balance(doc, '1110')  # Поиск страницы по коду 1110 в таблице Актив
page = doc[0]
tabs = page.find_tables(snap_tolerance=2.5)

if tabs.tables:  # Хотя бы одна таблица найдена?
    print(f"{len(tabs.tables)} tables found on {page}")  # Количество таблиц на странице

    # Прописать условие проверки: если None, то перейти к следующей таблице
    tab = tabs[1].extract()
    new_table = table_cleaner(tab)
    res = dict_creator(new_table)
    res = num_cleaner(res)
    print(res)
    print(res.get('1110'))
else:
    print("Таблицы не обнаружены!")
