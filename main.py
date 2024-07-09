import decimal
from decimal import Decimal
from ratio_extractor import RatioExtractor


def main():
    file1 = 'xlx/Бухгалтерский баланс. Лист 1.xls'
    file2 = 'xlx/Бухгалтерский баланс. Лист 2.xls'
    file3 = 'xlx/Отчет о финансовых результатах. Лист 1.xls'
    extractor = RatioExtractor(file1)
    balance = extractor.get_data()
    print(balance)


if __name__ == '__main__':
    main()
