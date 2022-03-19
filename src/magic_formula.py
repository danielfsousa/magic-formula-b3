from typing import Dict, List

from .stock import Result, Stock

MIN_LIQUIDITY = 200_000


def apply(stocks: List[Stock]) -> List[Result]:
    filtered_stocks = list(filter(should_include, stocks))
    ranked_by_ev_ebit = rank(filtered_stocks, "ev_ebit")
    ranked_by_roic = rank(filtered_stocks, "roic", desc=True)
    return sorted(
        [
            Result(
                stock,
                ev_ebit_rank=(ev_ebit_rank := ranked_by_ev_ebit[stock.ticker]),
                roic_rank=(roic_rank := ranked_by_roic[stock.ticker]),
                magic_formula=calculate(ev_ebit_rank, roic_rank),
            )
            for stock in filtered_stocks
        ],
        key=lambda r: r.magic_formula,
    )


def rank(stocks: List[Stock], key: str, desc: bool = False) -> Dict[str, int]:
    return {
        stock.ticker: idx + 1
        for (idx, stock) in enumerate(
            sorted(stocks, key=lambda s: getattr(s, key), reverse=desc)
        )
    }


def calculate(ev_ebit_rank: int, roic_rank: int) -> int:
    return ev_ebit_rank + roic_rank


def should_include(stock: Stock) -> bool:
    return stock.ev_ebit > 0 and stock.roic > 0 and stock.liquidity > MIN_LIQUIDITY
