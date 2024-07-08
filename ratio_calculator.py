import decimal
from decimal import Decimal

def calculate_absolute_financial_stability(capital, non_current_assets, supplies, long_passive, ):
    own_working_capital = []
    own_capital_for_supply = []
    own_capital_and_lp_for_supply = []
    for num1, num2 in zip(capital, non_current_assets):
        own_working_capital.append(num1 - num2)
    for num1, num2 in zip(own_working_capital, supplies):
        own_capital_for_supply.append(num1 - num2)
    for num1, num2, num3 in zip(own_working_capital, long_passive, supplies):
        own_capital_and_lp_for_supply.append(num1 + num2 - num3)
    for num1, num2, num3, num4 in zip(own_working_capital, supplies): # Посмотреть как это считается
        own_capital_for_supply.append(num1 - num2)
    return own_working_capital


def calculate_financial_stability(capital, balance, sum_passive, own_working_capital):
    equity_ratio = []
    debt_to_equity_ratio = []
    mobility_ratio = []
    for num1, num2 in zip(capital, balance):
        equity_ratio.append(Decimal(num1) / Decimal(num2))

    for num1, num2 in zip(sum_passive, capital):
        debt_to_equity_ratio.append(Decimal(num1) / Decimal(num2))

    for num1, num2 in zip(own_working_capital, capital):
        mobility_ratio.append(Decimal(num1) / Decimal(num2))



