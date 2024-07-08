import pymupdf
import os
import re
from unittest import TestCase

tex = 'Бухгалтерский баланс'
os.environ['TESSDATA_PREFIX'] = "E:/PO/Tesseract/tessdata"


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
    def test_ocr_page_number_detection(self):
        doc = pymupdf.open("Бух.отчет Новатэк 2023.pdf")
        search = 'Бухгалтерский баланс\nна 31 декабря '
        res = False
        count_of_i = 0

        for i in range(doc.page_count):
            page = doc[i]
            page_ocr = page.get_textpage_ocr(flags=3, language='rus', dpi=72, full=False,
                                             tessdata="E:/PO/Tesseract/tessdata")
            text = page_ocr.extractText()

            if search in text:
                res = True
                count_of_i += 1
        self.assertTrue(res)  # Проверяем, что искомый текст найден
        self.assertEqual(count_of_i, 1)  # Проверяем, что количество совпадений равно 1

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


