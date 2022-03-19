import csv
from datetime import date
from os import path
from typing import List, Protocol

from .stock import Result

FILENAME_FORMAT = "%Y-%m-%d"


class Storage(Protocol):
    def write(self, data: List[Result]) -> str:
        raise NotImplementedError("write")


class CSVStorage:
    def write(self, results: List[Result]) -> str:
        filename = f"{date.today().strftime(FILENAME_FORMAT)}.csv"
        filepath = path.abspath(path.join(path.dirname(__file__), "../data", filename))
        with open(filepath, mode="w+") as file:
            fieldnames = [
                "ticker",
                "ev_ebit",
                "roic",
                "ev_ebit_rank",
                "roic_rank",
                "magic_formula",
            ]
            writer = csv.writer(file)
            writer.writerow(fieldnames)
            for r in results:
                row = [
                    r.stock.ticker,
                    str(r.stock.ev_ebit),
                    str(r.stock.roic),
                    str(r.ev_ebit_rank),
                    str(r.roic_rank),
                    str(r.magic_formula),
                ]
                writer.writerow(row)
            return file.name
