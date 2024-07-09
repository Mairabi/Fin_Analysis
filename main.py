import decimal
from decimal import Decimal
from ratio_extractor import RatioExtractor


def main():
    filename_in = 'xlx\Бухгалтерский баланс. Лист 2.xls'
    extractor = RatioExtractor(filename_in)
    balance = extractor.get_data()
    print(balance)


if __name__ == '__main__':
    main()
