# magic-formula-b3

A CLI to scrape and calculate Joel Greenblatt's magic formula from Brazil's stock market (B3)

## Dependencies

- Python 3.10
- [PDM](https://pdm.fming.dev)

## Getting Started

1. Install dependencies

```bash
$ pdm install
```

2. See all the available options

```bash
$ pdm run cli --help
```

3. Scrape, calculate magic formula and write results

```bash
$ pdm run cli
```

4. A csv file named with the current date will be created on `data` folder.

5. Print top stocks

```bash
$ head data/2022-03-26_status_invest.csv | column -t -s,

ticker  ev_ebit  roic   ev_ebit_rank  roic_rank  magic_formula
AZEV4   1.13     2.596  4             1          5
BRKM3   2.25     0.534  11            3          14
G2DI33  0.86     0.363  1             13         14
BRKM5   2.25     0.534  12            4          16
FHER3   2.58     0.724  15            2          17
BRAP3   1.89     0.365  9             11         20
SYNE3   1.21     0.352  5             15         20
BRAP4   1.89     0.365  10            12         22
ETER3   2.49     0.446  14            9          23
```
