import unittest
from ratio_extractor import RatioExtractor

class TestDataExtraction(unittest.TestCase):

    def get_first_list_length(self, data):
        """
        Возвращает длину списка первого элемента словаря.

        :param data: Словарь, где ключами являются строки, а значениями списки.
        :return: Длина списка, соответствующего первому ключу в словаре.
        """
        if not data:
            raise ValueError("Словарь пустой")

        # Получаем первый ключ (порядок в словаре в Python 3.7+ соответствует порядку добавления)
        first_key = list(data.keys())[0]

        # Получаем список, соответствующий первому ключу
        first_list = data[first_key]

        # Определяем длину этого списка
        return len(first_list)

    def test_extract_data_and_calculate_ratios(self):
        # Тест: пользователь добавляет несколько файлов

        file1 = 'xlx/Бухгалтерский баланс. Лист 1.xls'
        file2 = 'xlx/Бухгалтерский баланс. Лист 2.xls'
        file3 = 'xlx/Отчет о финансовых результатах. Лист 1.xls'

        # Информация успешно извлекается

        balance1 = RatioExtractor(file1).get_data()
        balance2 = RatioExtractor(file2).get_data()
        financials = RatioExtractor(file3).get_data()

        self.assertIn('1100', balance1)
        self.assertIn('1510', balance2)
        self.assertIn('2340', financials)

        # Определяем минимальную длину списка в словарях для поддержание соответсвия расчетов показателей.
        # Т.к количество столбцов с показателями в балансе и фин. отчете может быть разным

        len_b1 = self.get_first_list_length(balance1)
        len_b2 = self.get_first_list_length(balance2)
        len_f = self.get_first_list_length(financials)
        min_len = min(len_b1, len_b2, len_f)

        self.assertEqual(min_len, 2)

        # Далее происходит расчет всех показателей

