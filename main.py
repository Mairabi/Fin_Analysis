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

    # Объединяем все словари показателей в один
    full_info = {**balance1, **balance2, **financials}

    abs_fin_stab = ratio_calculator.calculate_absolute_financial_stability(full_info['1300'], full_info['1100'],
                                                                           full_info['1210'], full_info['1400'],
                                                                           full_info['1510'], full_info['1520'])

    fin_stab = ratio_calculator.calculate_financial_stability(full_info['1300'], full_info['1600'],
                                                              full_info['1400'], full_info['1510'],
                                                              full_info['1520'],
                                                              abs_fin_stab['Собств. оборотные средства'])

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

    # Собираем все расчеты в один словарь
    fin_ratios = {**abs_fin_stab, **fin_stab, **liquidity, **return_on, **turnover}


if __name__ == '__main__':
    main()
