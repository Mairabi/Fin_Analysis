from ratio_extractor import RatioExtractor, FileProcessingError
import ratio_calculator


class DataCreator:
    def __init__(self, files_path):
        self.files_path = files_path
        self.years_of_balance = []

    def get_ratios(self):
        r1 = RatioExtractor(self.files_path[0])
        r2 = RatioExtractor(self.files_path[1])
        r3 = RatioExtractor(self.files_path[2])
        try:
            balance1 = r1.get_data()
            balance2 = r2.get_data()
            financials = r3.get_data()
        except FileProcessingError as e:
            print(f"{e.message}")
            raise
        else:
            self.years_of_balance = r1.years

            # Объединяем все словари показателей в один
            full_info = {**balance1, **balance2, **financials}

            try:
                abs_fin_stab = ratio_calculator.calculate_absolute_financial_stability(full_info['1300'],
                                                                                       full_info['1100'],
                                                                                       full_info['1210'],
                                                                                       full_info['1400'],
                                                                                       full_info['1510'],
                                                                                       full_info['1520'])

                fin_stab = ratio_calculator.calculate_financial_stability(full_info['1300'], full_info['1600'],
                                                                          full_info['1400'], full_info['1510'],
                                                                          full_info['1520'],
                                                                          abs_fin_stab['Абс. фин. устойчивость']
                                                                          ['Собств. оборотные средства'])

                liquidity = ratio_calculator.calculate_liquidity_ratios(full_info['1250'], full_info['1510'],
                                                                        full_info['1520'], full_info['1230'])

                return_on = ratio_calculator.calculate_return_on_ratios(full_info['2400'], full_info['2120'],
                                                                        full_info['1150'], full_info['2200'],
                                                                        full_info['2110'], full_info['1600'][:-1],
                                                                        full_info['1300'][:-1])

                turnover = ratio_calculator.calculate_turnover_ratios(full_info['2110'], full_info['1600'][:-1],
                                                                      full_info['1300'][:-1], full_info['1400'][:-1],
                                                                      full_info['1510'], full_info['1100'][:-1],
                                                                      full_info['2120'], full_info['1210'][:-1],
                                                                      full_info['1230'][:-1])


            except KeyError:
                raise
            else:
                # Собираем все расчеты в один словарь

                fin_ratios = {**abs_fin_stab, **fin_stab, **liquidity, **return_on, **turnover}
                return fin_ratios


if __name__ == '__main__':
    filename_in = ['xlx/Бухгалтерский баланс. Лист 1.xls', 'xlx/Бухгалтерский баланс. Лист 2 — копия.xls',
                   'xlx/Отчет о финансовых результатах. Лист 2.xls']
    extr = DataCreator(filename_in)
    extr.get_ratios()
