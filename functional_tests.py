import unittest
from ratio_extractor import RatioExtractor
import ratio_calculator

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
        # lens = map(self.get_first_list_length, ) ПРОВЕРИТЬ!!!

        self.assertEqual(min_len, 2)

        # Объединяем все словари в один
        full_info = balance1
        full_info.update(balance2)
        full_info.update(financials)

        self.assertIn('1110', full_info)
        self.assertIn('1400', full_info)
        self.assertIn('2110', full_info)

        # Далее происходит расчет всех показателей

        abs_fin_stab = ratio_calculator.calculate_absolute_financial_stability(full_info['1300'], full_info['1100'],
                                                                               full_info['1210'], full_info['1400'],
                                                                               full_info['1510'], full_info['1520'])
        print(abs_fin_stab)

        fin_stab = ratio_calculator.calculate_financial_stability(full_info['1300'], full_info['1600'],
                                                                  full_info['1400'], full_info['1510'],
                                                                  full_info['1520'],
                                                                  abs_fin_stab['Собств. оборотные средства'])
        print(fin_stab)

        liquidity = ratio_calculator.calculate_liquidity_ratios(full_info['1250'], full_info['1510'],
                                                                full_info['1520'], full_info['1230'])
        print(liquidity)

        return_on = ratio_calculator.calculate_return_on_ratios(full_info['2400'], full_info['2120'],
                                                                full_info['1150'], full_info['2200'],
                                                                full_info['2110'], full_info['1600'][:1],
                                                                full_info['1300'][:1])
        print(return_on)

        turnover = ratio_calculator.calculate_turnover_ratios(full_info['2110'], full_info['1600'][:1],
                                                              full_info['1300'][:1], full_info['1400'][:1],
                                                              full_info['1510'], full_info['1100'][:1],
                                                              full_info['2120'], full_info['1210'][:1],
                                                              full_info['1230'][:1])
        print(turnover)


