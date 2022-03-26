from enum import Enum
import typer

from . import magic_formula
from .api import Api, FundamentusScraper, StatusInvestScraper
from .storage import CSVStorage, JSONStorage, Storage


class ApiSource(str, Enum):
    status_invest = "status_invest"
    fundamentus = "fundamentus"


class Format(str, Enum):
    csv = "csv"
    json = "json"


def main(
    api: ApiSource = typer.Option(ApiSource.status_invest, help="API data source."),
    format: Format = typer.Option(Format.csv, help="File output format."),
):
    fetcher = make_fetcher(api)
    storage = make_storage(format, api)

    typer.echo(f"fetching stocks with {api} api ...")
    stocks = fetcher.get_stocks()

    typer.echo(f"writing {format} ...")
    outpath = storage.write(magic_formula.apply(stocks))

    typer.echo(f"done: {outpath}")


def make_fetcher(api: ApiSource) -> Api:
    match api:
        case ApiSource.status_invest: return StatusInvestScraper()
        case ApiSource.fundamentus: return FundamentusScraper()


def make_storage(format: Format, api: ApiSource) -> Storage:
    match format:
        case Format.csv: return CSVStorage(api)
        case Format.json: return JSONStorage(api)


if __name__ == "__main__":
    typer.run(main)
