import pymupdf
import re
from aspose.cells import Workbook, LoadOptions, LoadFormat, PdfSaveOptions


class FileProcessingError(Exception):
    """Обработка файловых исключений"""

    def __init__(self, message):
        super().__init__(message)
        self.message = message

    def __str__(self):
        return self.message


class RatioExtractor:
    def __init__(self, filename_in, filename_out=''):
        self.filename_in = filename_in
        self.filename_out = filename_out
        self.economic_values = None
        self.years = None

    # Преобразование xlx файлов в pdf
    def xlx_to_pdf(self, filename_in):
        try:
            if filename_in.endswith('.xlsx'):
                self.filename_out = re.sub(r'\.xlsx*$', '.pdf', filename_in)
                loadOptions = LoadOptions(LoadFormat.XLSX)
                workbook = Workbook(filename_in, loadOptions)
            elif filename_in.endswith('.xls'):
                self.filename_out = re.sub(r'\.xls$', '.pdf', filename_in)
                workbook = Workbook(filename_in)
            else:
                raise FileProcessingError('Неверный формат файла!')

            # Установка параметров страницы для печати на одной странице
            for worksheet in workbook.worksheets:
                worksheet.page_setup.fit_to_pages_wide = 1
                worksheet.page_setup.fit_to_pages_tall = 1

            # Сохранение в PDF с использованием параметров печати
            pdf_save_options = PdfSaveOptions()
            workbook.save(self.filename_out, pdf_save_options)

        except Exception as e:
            if 'Could not find file' in str(e):
                print('Файл не найден!')
                raise FileProcessingError('Файл не найден!') from e
            else:
                print(f'Проблемы с файлом: {e}')
                raise FileProcessingError(f'Проблемы с файлом: {e}') from e

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
                    if cleaned_number.startswith('-'):
                        numbers[i] = int(cleaned_number)
                    elif cleaned_number.startswith('('):
                        numbers[i] = -int(cleaned_number[1:-1])
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
        try:
            self.xlx_to_pdf(self.filename_in)

        except FileProcessingError as e:
            print(f"Прерывание выполнения из-за ошибки преобразования файла:{e.message}")
            raise

        try:
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
                        doc.close()
                        raise FileProcessingError("Не найдена ни одна подходящая таблица!")

                    tab = tabs[k].extract()
                    keyword = tab[0][0]

                    k += 1
                else:
                    new_table = self.table_cleaner(tab)
                    self.years = [item.split()[-2] for item in new_table[0] if 'г.' in item]

                    self.dict_creator(new_table)
                    self.num_cleaner(self.economic_values)

                    doc.close()
                    return self.economic_values
            else:
                doc.close()
                raise FileProcessingError("Таблицы не обнаружены!")

        except Exception as e:
            raise FileProcessingError(f"Ошибка при обработке PDF: {e}")


if __name__ == '__main__':
    filename_in = 'xlx/Тестовый отчет о фин. Лист 1.xlsx'
    extr = RatioExtractor(filename_in).get_data()
    print(extr)
