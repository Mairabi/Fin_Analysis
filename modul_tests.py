import pymupdf
import os
import re
import decimal
from decimal import Decimal
from unittest import TestCase

tex = 'Бухгалтерский баланс'
# os.environ['TESSDATA_PREFIX'] = "E:/PO/Tesseract/tessdata"


class TableExtractTest(TestCase):

    # Поиск страницы, с которой начинается бух. баланс
    def test_page_number_detection(self):
        doc = pymupdf.open("Бух. отчет Сургутнефтегаз.pdf")
        search = 'Бухгалтерский баланс'
        count_of_i = 0
        res = False

        for i in range(doc.page_count):
            page = doc[i]
            text = page.get_text()

            if search in text:
                res = True
                count_of_i += 1
        self.assertTrue(res)  # Проверяем, что искомый текст найден
        self.assertEqual(count_of_i, 1)  # Проверяем, что количество совпадений равно 1

    # Поиск страницы с помощью OCR, с которой начинается бух. баланс

    def test_loss_check(self):
        pattern = r'\d'
        loss = ['(34 500)', '(6543 455)', '-', '234 233', '568 876', '(125 4345)', '-']
        for i, item in enumerate(loss):
            if re.search(pattern, item):
                cleaned_number = item.replace(' ', '')
                if cleaned_number[0] == '(':
                    loss[i] = -int(cleaned_number[1:-1])
                else:
                    loss[i] = int(cleaned_number)

        for value in loss:
            print(value)


class RatioCalculateTest(TestCase):

    def test_calculate_own_working_capital(self):
        capital = [913570, 723715, 627671]
        non_current_assets = [318073, 237015, 306853]
        own_working_capital = []
        for num1, num2 in zip(capital, non_current_assets):
            own_working_capital.append(num1 - num2)
        self.assertEqual(own_working_capital, [595497, 486700, 320818])

    def test_calculate_liquidity(self):
        decimal.getcontext().prec = 6
        d = [1128, 188, 12398]
        kt = [1868, 168814, 1094]
        rp = [89867, 498738, 254671]
        r = [27020, 884753, 119679]
        absolute_liquidity_ratios = []
        current_liquidity_ratios = []
        for d_val, kt_val, rp_val, r_val in zip(d, kt, rp, r):
            absolute_liquidity = Decimal(d_val) / (Decimal(kt_val) + Decimal(rp_val))
            current_liquidity = (Decimal(d_val) + Decimal(r_val)) / (Decimal(kt_val) + Decimal(rp_val))

            # Ограничиваем точность до 4-х знаков после запятой
            absolute_liquidity = absolute_liquidity.quantize(Decimal('0.0001'))
            current_liquidity = current_liquidity.quantize(Decimal('0.0001'))

            absolute_liquidity_ratios.append(absolute_liquidity)
            current_liquidity_ratios.append(current_liquidity)
        # return absolute_liquidity_ratios, current_liquidity_ratios
        print('Абсолютная ликвидность')
        for l in absolute_liquidity_ratios:
            print(l)
        print('Текущая ликвидность')
        for l in current_liquidity_ratios:
            print(l)

    def test_calculate_return_on_ratios(self):
        decimal.getcontext().prec = 6

        revenue = [503610, 676958]
        balance = [2022695, 1229238]
        capital = [913570, 723715]

        asset_turnover_ratios = []
        equity_turnover_ratios = []

        for values in zip(revenue, balance, capital):
            asset_turnover_ratio = Decimal(values[0]) / Decimal(values[1])
            equity_turnover_ratio = Decimal(values[0]) / Decimal(values[2])

            asset_turnover_ratio = asset_turnover_ratio.quantize(Decimal('0.0001'))
            equity_turnover_ratio = equity_turnover_ratio.quantize(Decimal('0.0001'))

            asset_turnover_ratios.append(asset_turnover_ratio)
            equity_turnover_ratios.append(equity_turnover_ratio)

        print('Оборачиваемость активов')
        for l in asset_turnover_ratios:
            print(l)
        print('Оборачиваемость собственного капитала')
        for l in equity_turnover_ratios:
            print(l)

    def test_calculate_turnover_ratios(self):
        revenue = [503610, 676958]
        balance = [2022695, 1229238]
        capital = [913570, 723715]
        kT = [366978, 221872]
        kt = [166814, 1094]
        f = [318073, 237015]
        cc = [392258, 433240]
        zp = [818909, 860083]
        r = [884753, 119679]

        asset_turnover_ratios = []  # Оборачиваемость активов
        equity_turnover_ratios = []  # Об. собств. капитала
        borrowed_capital_turnover_ratios = []  # Об. заемного капитала
        fixed_assets_turnover_ratios = []  # Об. основных средств
        inventory_turnover_ratios = []  # Об. запасов и затрат
        production_inventory_turnover_ratios = []  # Об. произв. запасов в днях
        receivables_turnover_ratios = []  # Об. дебиторской задолженности
        credit_terms = []  # Срок товарного кредита

        for values in zip(revenue, balance, capital, kT, kt, f, cc, zp, r):
            asset_turnover_ratio = Decimal(values[0]) / Decimal(values[1])
            equity_turnover_ratio = Decimal(values[0]) / Decimal(values[2])

            borrowed_capital_turnover_ratio = Decimal(values[0]) / (Decimal(values[3]) + Decimal(values[4]))
            fixed_assets_turnover_ratio = Decimal(values[0]) / Decimal(values[5])

            inventory_turnover_ratio = Decimal(values[6]) / Decimal(values[7])
            production_inventory_turnover_ratio = Decimal(365) / Decimal(inventory_turnover_ratio)

            receivables_turnover_ratio = Decimal(values[0]) / Decimal(values[8])
            credit_term = Decimal(365) / Decimal(receivables_turnover_ratio)

            asset_turnover_ratios.append(asset_turnover_ratio)
            equity_turnover_ratios.append(equity_turnover_ratio)

            borrowed_capital_turnover_ratios.append(borrowed_capital_turnover_ratio)
            fixed_assets_turnover_ratios.append(fixed_assets_turnover_ratio)

            inventory_turnover_ratios.append(inventory_turnover_ratio)
            production_inventory_turnover_ratios.append(production_inventory_turnover_ratio)

            receivables_turnover_ratios.append(receivables_turnover_ratio)
            credit_terms.append(credit_term)

        return {
            "Оборачиваемость активов": asset_turnover_ratios,
            "Оборачиваемость собственного капитала": equity_turnover_ratios,
            "Оборачиваемость заемного капитала": borrowed_capital_turnover_ratios,
            "Оборачиваемость основных средств": fixed_assets_turnover_ratios,
            "Оборачиваемость запасов и затрат": inventory_turnover_ratios,
            "Оборачиваемость запасов в днях": production_inventory_turnover_ratios,
            "Оборачиваемость дебиторской задолженности": receivables_turnover_ratios,
            "Срок товарного кредита": credit_terms
        }


class TestNewIdeas(TestCase):

    def test_create_new_filename(self):
        file1 = 'xlx/Отчет о финансовых результатах. Лист 1.xls'
        file_out1 = re.sub(r'\.xlsx*$', '.pdf', file1)
        self.assertEqual(file_out1, 'xlx/Отчет о финансовых результатах. Лист 1.pdf')

    def test_search_length_of_first_dict_element(self):
        # Определяю минимальную длину списка первого элемента двух словарей
        data = {
            '1110': [47372, 272, 91190],
            '1120': [4899, 48399, 83990],

        }

        data2 = {
            '1140': [47372, 272],
            '1150': [4899, 48399],
        }

        # Получаем первый ключ (порядок в словаре в Python 3.7+ соответствует порядку добавления)
        first_key = list(data.keys())[0]
        first_key2 = list(data2.keys())[0]

        # Получаем список, соответствующий первому ключу
        first_list = data[first_key]
        second_list = data2[first_key2]

        # Определяем длину этого списка
        first_list_length = len(first_list)
        second_list_length = len(second_list)

        self.assertEqual(first_list_length, 3)
        self.assertEqual(second_list_length, 2)
        self.assertGreater(first_list_length, second_list_length)

    def test_file_exceptions(self):
        from aspose.cells import Workbook, LoadOptions, LoadFormat
        flag = False
        filename_in = 'xlx/Бухгалтерский баланс. Лист 1.xlsx'
        try:
            if 'xlsx' in filename_in:
                self.filename_out = re.sub(r'\.xlsx*$', '.pdf', filename_in)
                loadOptions = LoadOptions(LoadFormat.XLSX)
                workbook = Workbook(filename_in, loadOptions)
                workbook.save(self.filename_out)

                flag = True
                self.assertTrue(flag, 'Файл открылся успешно')
            elif 'xls' in filename_in:
                self.filename_out = re.sub(r'\.xlsx*$', '.pdf', filename_in)
                workbook = Workbook(filename_in)
                workbook.save(self.filename_out)

                flag = True
                self.assertTrue(flag, 'Файл открылся успешно')
            else:
                self.assertTrue(flag, 'Неверный формат файла')

        except Exception as e:
            if 'Could not find file' in str(e):
                print('Файл не найден!')
            else:
                print(f'Проблемы с файлом:{e}')
            self.assertFalse(flag, 'Упал в блоке except')

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

    def test_years_extraction(self):

        pattern = r"20[2-9][0-9]"

        doc = pymupdf.open("xlx/Отчет о финансовых результатах. Лист 1.pdf")
        page = doc[0]
        tabs = page.find_tables(snap_tolerance=2.5)

        if tabs:
            tab = tabs[1].extract()
            new_table = self.table_cleaner(tab)
            years = [item.split()[-2] for item in new_table[0] if 'г.' in item]

            print(years)

            self.assertIn('2021', years)
