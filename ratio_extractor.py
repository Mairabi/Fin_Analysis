import pymupdf
import re
from aspose.cells import Workbook


class RatioExtractor:
    def __init__(self, filename_in, filename_out, economic_values=None):
        self.filename_in = filename_in
        self.filename_out = filename_out
        self.economic_values = economic_values

    # Преобразование xlx файлов в pdf
    def xlx_to_pdf(self, filename_in, filename_out):
        workbook = Workbook(filename_in)
        workbook.save(filename_out)

    # Очистка извлеченных строк таблицы от посторонних символов
    def table_cleaner(self, table):
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
    def num_cleaner(self, info):
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
    def dict_creator(self, table):
        pattern = r"[1-2][1-7][0-9][0-2]"
        self.economic_values = {}
        # Итеративно обходим каждую строку в таблице
        for row_num in range(len(table)):
            row = table[row_num]
            code = next((s for s in row if re.fullmatch(pattern, s)), None)  # Находим код строки (напр. 1150)
            if code is not None:
                code_id = row.index(code)  # Определяем индекс этого кода в списке
                self.economic_values[code] = row[code_id + 1:]

        return self.economic_values

    # Основная функция
    def get_data(self):
        self.xlx_to_pdf(self.filename_in, self.filename_out)

        doc = pymupdf.open(self.filename_out)
        page = doc[0]
        tabs = page.find_tables(snap_tolerance=2.5)

        if tabs.tables:  # Хотя бы одна таблица найдена?
            print(f"{len(tabs.tables)} tables found on {page}")  # Количество таблиц на странице
            # Ищем нужную таблицу
            keyword = ''
            k = 0
            while keyword != 'Пояснения':
                if k >= len(tabs.tables):
                    print("Не найдена ни одна подходящая таблица!")
                    return False
                tab = tabs[k].extract()
                keyword = tab[0][0]

                k += 1
            else:
                new_table = self.table_cleaner(tab)
                self.dict_creator(new_table)
                self.num_cleaner(self.economic_values)
                return self.economic_values
        else:
            print("Таблицы не обнаружены!")
            return False


if __name__ == '__main__':

    filename_in = 'xlx\Бухгалтерский баланс. Лист 2.xls'
    filename_out = "Convert.pdf"
    xlx_to_pdf(filename_in, filename_out)

    doc = pymupdf.open(filename_out)
    page = doc[0]
    tabs = page.find_tables(snap_tolerance=2.5)

    if tabs.tables:  # Хотя бы одна таблица найдена?
        print(f"{len(tabs.tables)} tables found on {page}")  # Количество таблиц на странице

        # Ищем нужную таблицу
        keyword = ''
        k = 0
        while keyword != 'Пояснения':
            tab = tabs[k].extract()
            keyword = tab[0][0]
            if k == len(tabs.tables):
                print("Не найдена ни одна подходящая таблица!")
                break
            k += 1
        else:
            new_table = table_cleaner(tab)
            res = dict_creator(new_table)
            res = num_cleaner(res)
            print(res)
    else:
        print("Таблицы не обнаружены!")
