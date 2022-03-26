from abc import ABC, abstractmethod
import csv
import dataclasses
from datetime import date
import json
from os import path
from typing import List

from .stock import Result

FILENAME_FORMAT = "%Y-%m-%d"


class Storage(ABC):
    api: str

    def __init__(self, api: str):
        self.api = api
        self.outpath = self.__get_outpath(api)

    def __get_outpath(self, api: str) -> str:
        filename = f"{date.today().strftime(FILENAME_FORMAT)}_{api}"
        return path.abspath(path.join(path.dirname(__file__), "../data", filename))

    @abstractmethod
    def write(self, results: List[Result]) -> str:
        pass


class CSVStorage(Storage):
    def write(self, results: List[Result]) -> str:
        with open(self.outpath + ".csv", mode="w+") as file:
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


class JSONStorage(Storage):
    def write(self, results: List[Result]) -> str:
        with open(self.outpath + ".json", mode="w+") as file:
            json.dump(list(map(lambda r: dataclasses.asdict(r), results)), file)
            return file.name
