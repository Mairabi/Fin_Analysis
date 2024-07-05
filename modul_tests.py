import pymupdf
import os
from unittest import TestCase

tex = 'Бухгалтерский баланс'
os.environ['TESSDATA_PREFIX'] = "E:/PO/Tesseract/tessdata"


class SomeTests(TestCase):

    # Поиск страницы, с которой начинается бух. баланс
    def test_page_number_detection(self):
        doc = pymupdf.open("Бух. отчет Сургутнефтегаз.pdf")
        search = 'Бухгалтерский баланс'
        count_of_i = 0
        res = False

        for i in range(doc.page_count):
            # text = page.get_text()
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

    def test_fake(self):
        search = 'Бухгалтерский баланс'
        s = ['фывфывыпппп', 'кцуква', 'бю.вазз', 'у444уцк', 'Бухгалтерский баланс']
        for w in s:
            self.assertIn(search, w)
