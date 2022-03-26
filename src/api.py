import csv
from io import StringIO
import locale
from abc import ABC, abstractmethod
from typing import List

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

from .stock import Stock

LOCALE = "pt_BR"
FUNDAMENTUS_URL = "https://www.fundamentus.com.br/resultado.php"
STATUS_INVEST_URL = "https://statusinvest.com.br/category/advancedsearchresultexport?search=%7B%22Sector%22%3A%22%22%2C%22SubSector%22%3A%22%22%2C%22Segment%22%3A%22%22%2C%22my_range%22%3A%22-20%3B100%22%2C%22forecast%22%3A%7B%22upsideDownside%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22estimatesNumber%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22revisedUp%22%3Atrue%2C%22revisedDown%22%3Atrue%2C%22consensus%22%3A%5B%5D%7D%2C%22dy%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_L%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22peg_Ratio%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_VP%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemBruta%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemEbit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22margemLiquida%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_Ebit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22eV_Ebit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividaLiquidaEbit%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22dividaliquidaPatrimonioLiquido%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_SR%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_CapitalGiro%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22p_AtivoCirculante%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roe%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roic%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22roa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezCorrente%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22pl_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22passivo_Ativo%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22giroAtivos%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22receitas_Cagr5%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22lucros_Cagr5%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22liquidezMediaDiaria%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22vpa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22lpa%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%2C%22valorMercado%22%3A%7B%22Item1%22%3Anull%2C%22Item2%22%3Anull%7D%7D&CategoryType=1"  # noqa: 501

locale.setlocale(locale.LC_ALL, LOCALE)


def ptof(string: str) -> float:
    return round(locale.atof(string.strip("%")) / 100, 3)


class Api(ABC):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/\
                537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
    }

    def parse_stock(
        self, ticker: str, ev_ebit: str, roic: str, liquidity: str
    ) -> Stock:
        return Stock(
            ticker=ticker,
            ev_ebit=locale.atof(ev_ebit),
            roic=ptof(roic),
            liquidity=locale.atof(liquidity),
        )

    @abstractmethod
    def get_stocks(self) -> List[Stock]:
        pass


class StatusInvestScraper(Api):
    def __parse_csv(self, csv_text: str) -> List[Stock]:
        return [
            self.parse_stock(
                row["TICKER"],
                row["EV/EBIT"],
                row["ROIC"],
                row[" LIQUIDEZ MEDIA DIARIA"],
            )
            for row in csv.DictReader(StringIO(csv_text), delimiter=";")
            if row["ROIC"] and row["EV/EBIT"] and row[" LIQUIDEZ MEDIA DIARIA"]
        ]

    def get_stocks(self) -> List[Stock]:
        res = requests.get(STATUS_INVEST_URL, headers=self.headers)
        rows = self.__parse_csv(res.text)
        return rows


class FundamentusScraper(Api):
    def __parse_html(self, page: BeautifulSoup) -> List[Stock]:
        def get_text(el: Tag) -> str:
            return el.get_text(strip=True)

        def select_col(idx: int) -> ResultSet[Tag]:
            return page.select(f"td:nth-child({idx})")  # type: ignore

        headers = list(map(get_text, page.select(selector="th a")))  # type: ignore
        ticker_idx = headers.index("Papel") + 1
        ev_ebit_idx = headers.index("EV/EBIT") + 1
        roic_idx = headers.index("ROIC") + 1
        liquidity_idx = headers.index("Liq.2meses") + 1

        return [
            self.parse_stock(ticker, ev_ebit, roic, liquidity)
            for (ticker, ev_ebit, roic, liquidity) in zip(
                map(get_text, select_col(ticker_idx)),
                map(get_text, select_col(ev_ebit_idx)),
                map(get_text, select_col(roic_idx)),
                map(get_text, select_col(liquidity_idx)),
            )
        ]

    def get_stocks(self) -> List[Stock]:
        res = requests.get(FUNDAMENTUS_URL, headers=self.headers)
        page = BeautifulSoup(res.text, "html.parser")
        rows = self.__parse_html(page)
        return rows
