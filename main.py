from ratio_extractor import RatioExtractor
import ratio_calculator


def main():
    file1 = 'xlx/Бухгалтерский баланс. Лист 1.xls'
    file2 = 'xlx/Бухгалтерский баланс. Лист 2.xls'
    file3 = 'xlx/Отчет о финансовых результатах. Лист 1.xls'

    r1 = RatioExtractor(file1)
    r2 = RatioExtractor(file2)
    r3 = RatioExtractor(file3)

    balance1 = r1.get_data()
    balance2 = r2.get_data()
    financials = r3.get_data()

    years_of_balance1 = r1.years
    years_of_balance2 = r2.years
    years_of_balance3 = r3.years

    # Объединяем все словари в один
    # full_info = balance1
    # full_info.update(balance2)
    # full_info.update(financials)

    # abs_fin_stab = ratio_calculator.calculate_absolute_financial_stability(full_info['1300'], full_info['1100'],
    #                                                                        full_info['1210'], full_info['1400'],
    #                                                                        full_info['1510'], full_info['1520'])
    # print(abs_fin_stab)

    # fin_stab = ratio_calculator.calculate_financial_stability(full_info['1300'], full_info['1600'],
    #                                                           full_info['1400'], full_info['1510'],
    #                                                           full_info['1520'],
    #                                                           abs_fin_stab['Собств. оборотные средства'])
    # print(fin_stab)
    #
    # liquidity = ratio_calculator.calculate_liquidity_ratios(full_info['1250'], full_info['1510'],
    #                                                         full_info['1520'], full_info['1230'])
    # print(liquidity)
    #
    # return_on = ratio_calculator.calculate_return_on_ratios(full_info['2400'], full_info['2120'],
    #                                                         full_info['1150'], full_info['2200'],
    #                                                         full_info['2110'], full_info['1600'][:-1],
    #                                                         full_info['1300'][:-1])
    # print(return_on)
    #
    # turnover = ratio_calculator.calculate_turnover_ratios(full_info['2110'], full_info['1600'][:-1],
    #                                                       full_info['1300'][:-1], full_info['1400'][:-1],
    #                                                       full_info['1510'], full_info['1100'][:-1],
    #                                                       full_info['2120'], full_info['1210'][:-1],
    #                                                       full_info['1230'][:-1])
    # print(turnover)


if __name__ == '__main__':
    main()
