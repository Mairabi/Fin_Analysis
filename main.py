import pymupdf
from ratio_extractor import RatioExtractor


def main():
    filename_in = 'xlx\Бухгалтерский баланс. Лист 2.xls'
    filename_out = "Бухгалтерский баланс. Лист 2.pdf"
    extractor = RatioExtractor(filename_in, filename_out)
    balance = extractor.get_data()
    print(balance)


if __name__ == '__main__':
    main()
