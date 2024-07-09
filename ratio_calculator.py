import decimal
from decimal import Decimal

# Количество знаков после запятой
decimal.getcontext().prec = 6


def calculate_absolute_financial_stability(capital, non_current_assets, z, kT, kt, ap):
    # capital - капитал и резервы
    # non_current_assets - внеоборотные активы
    # z - запасы
    # kT - долгосрочные пассивы
    # kt - краткосрочные кредиты и займы
    # ap - кредиторская задолженность

    own_working_capital = []  # Собственные оборотные средства
    own_capital_for_supply = []  # Дельта собственных средств для формирования запасов и затрат
    own_capital_and_lp_for_supply = []  # Дельта собственных и долгосрочных источников для формирования запасов и затрат
    main_sources_for_supplies = []

    for num1, num2 in zip(capital, non_current_assets):
        own_working_capital.append(num1 - num2)

    for num1, num2 in zip(own_working_capital, z):
        own_capital_for_supply.append(num1 - num2)

    for num1, num2, num3 in zip(own_working_capital, kT, z):
        own_capital_and_lp_for_supply.append(num1 + num2 - num3)

    for num1, num2, num3, num4, num5 in zip(own_working_capital, kT, kt, ap, z):
        main_sources_for_supplies.append(num1 + num2 + num3 + num4 - num5)

    return {'Собств. оборотные средства': own_working_capital,
            'Дельта собств. средства для формирования запасов и затрат': own_capital_for_supply,
            'Дельта собств. и долгосрочных источников для формирования запасов и затрат': own_capital_and_lp_for_supply,
            'Дельта общей  величины  основных  источников для формирования запасов затрат': main_sources_for_supplies
            }


def calculate_financial_stability(capital, balance,  kT, kt, ap, own_working_capital):
    # capital - капитал и резервы
    # balance - баланс
    # kT - долгосрочные пассивы
    # kt - краткосрочные кредиты и займы
    # ap - кредиторская задолженность
    # own_working_capital - собственные оборотные средства

    equity_ratio = []  # К. автономии
    debt_to_equity_ratio = []  # К. соотн. собств. и заемных средств
    mobility_ratio = []  # К. маневренности
    for num1, num2 in zip(capital, balance):
        equity_ratio.append(Decimal(num1) / Decimal(num2))

    for num1, num2, num3, num4 in zip(kT, kt, ap, capital):
        debt_to_equity_ratio.append(Decimal(num1 + num2 + num3) / Decimal(num4))

    for num1, num2 in zip(own_working_capital, capital):
        mobility_ratio.append(Decimal(num1) / Decimal(num2))

    return {'К. автономии': equity_ratio,
            'К. соотн. собств. и заемных средств': debt_to_equity_ratio,
            'К. маневренности': mobility_ratio}


def calculate_liquidity_ratios(d, kt, ap, r):
    # d - день.средства и краткосрочные фин. вложения
    # kt - краткосрочные кредиты и займы
    # ap - кредиторская задолженность
    # r - дебиторская задолженность

    absolute_liquidity_ratios = []
    current_liquidity_ratios = []
    for d_val, kt_val, ap_val, r_val in zip(d, kt, ap, r):
        absolute_liquidity = Decimal(d_val) / (Decimal(kt_val) + Decimal(ap_val))
        current_liquidity = (Decimal(d_val) + Decimal(r_val)) / (Decimal(kt_val) + Decimal(ap_val))
        absolute_liquidity_ratios.append(absolute_liquidity)
        current_liquidity_ratios.append(current_liquidity)
    return {'Абсолютная ликвидность': absolute_liquidity_ratios,
            'Ликвидность': current_liquidity_ratios}


def calculate_return_on_ratios(np, cc, oc, pf, revenue, assets, capital):
    # np - Чистая прибыль
    # cc - Себестоимость
    # oc - Основные средства
    # pf - Прибыль от продаж
    # revenue - Выручка
    # assets - Активы
    # capital- собственный капитал

    rom_s = []
    rofa_s = []
    ros_s = []
    roa_s = []
    roe_s = []
    for np_val, cc_val, oc_val, pf_val, revenue_val, assets_val, capital_val in zip(np, cc, oc, pf, revenue, assets,
                                                                                   capital):
        rom = (Decimal(np_val) / Decimal(cc_val)) * 100
        rofa = (Decimal(np_val) / Decimal(oc_val)) * 100
        ros = (Decimal(pf_val) / Decimal(revenue_val)) * 100
        roa = (Decimal(np_val) / Decimal(assets_val)) * 100
        roe = (Decimal(np_val) / Decimal(capital_val)) * 100

        rom_s.append(rom)
        rofa_s.append(rofa)
        ros_s.append(ros)
        roa_s.append(roa)
        roe_s.append(roe)

    return {'ROE': roe_s,
            'ROA': roa_s,
            'ROS': ros_s,
            'ROFA': rofa_s,
            'ROM': rom_s}


def calculate_turnover_ratios(revenue, balance, capital, kT, kt, f, cc, zp, r):
    # revenue - выручка
    # balance - баланс (среднегодовой)
    # capital - капитал и резервы (ср. годовое значение)
    # kT - долгосрочные пассивы
    # kt - краткосрочные кредиты и займы
    # f - внеоборотные активы (ср. знач. за год)
    # cс - Себестоимость реализованной продукции
    # zp - средняя стоимость запасов
    # r - дербитораская задолженность
    # t - продолжительность производственного цикла или продолжительность года

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
