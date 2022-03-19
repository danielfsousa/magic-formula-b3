from dataclasses import dataclass


@dataclass
class Stock:
    ticker: str
    ev_ebit: float
    roic: float
    liquidity: float


@dataclass
class Result:
    stock: Stock
    ev_ebit_rank: int
    roic_rank: int
    magic_formula: int
