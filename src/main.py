import sys

from . import magic_formula
from .api import FundamentusScraper
from .storage import CSVStorage


def main():
    api = FundamentusScraper()
    storage = CSVStorage()
    stocks = api.get_stocks()
    outpath = storage.write(magic_formula.apply(stocks))
    print(f"Done: {outpath}")


if __name__ == "__main__":
    sys.exit(main())
