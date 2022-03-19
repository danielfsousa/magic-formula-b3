import locale
from typing import List, Protocol

import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

from .stock import Stock

URL = "https://www.fundamentus.com.br/resultado.php"
LOCALE = "pt_BR"

locale.setlocale(locale.LC_ALL, LOCALE)


class Api(Protocol):
    def get_stocks(self) -> List[Stock]:
        raise NotImplementedError("get_stocks")


class FundamentusScraper(Api):
    def __parse_html(self, page: BeautifulSoup):
        def get_text(el: Tag) -> str:
            return el.get_text(strip=True)

        def select_col(idx: int) -> ResultSet[Tag]:
            return page.select(f"td:nth-child({idx})")  # type: ignore

        def ptof(string: str) -> float:
            return round(locale.atof(string.strip("%")) / 100, 3)

        headers = list(map(get_text, page.select(selector="th a")))  # type: ignore
        ticker_idx = headers.index("Papel") + 1
        ev_ebit_idx = headers.index("EV/EBIT") + 1
        roic_idx = headers.index("ROIC") + 1
        liquidity_idx = headers.index("Liq.2meses") + 1

        return [
            Stock(
                ticker=ticker,
                ev_ebit=locale.atof(ev_ebit),
                roic=ptof(roic),
                liquidity=locale.atof(liquidity),
            )
            for (ticker, ev_ebit, roic, liquidity) in zip(
                map(get_text, select_col(ticker_idx)),
                map(get_text, select_col(ev_ebit_idx)),
                map(get_text, select_col(roic_idx)),
                map(get_text, select_col(liquidity_idx)),
            )
        ]

    def get_stocks(self) -> List[Stock]:
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/\
                537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
        }
        res = requests.get(URL, headers=headers)
        page = BeautifulSoup(res.text, "html.parser")
        rows = self.__parse_html(page)
        return rows
