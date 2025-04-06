import yfinance as yf
import pandas_datareader.data as web
import datetime
import pandas as pd
import math
ticker_list = ['PG']
Dgrowthratelist = [0.07]
Requiredreturnlist = [0.1]
DDMappropriate = [True]
Grahamappropriate = [True]

GrowthRate = [2]#graham formula uses % not decimal

i = 0

start = datetime.datetime.today() - datetime.timedelta(days=10)
end = datetime.datetime.today()

aaa_yield = web.DataReader('DAAA', 'fred', start, end)
AAAbondyield = aaa_yield.dropna().iloc[-1, 0]

def Dividend_growth_rate_calc(DperShare, i):
    while i< (len(Dgrowthratelist)):
        if DDMappropriate[i] == True:
            Dgrowthrate = Dgrowthratelist[i]
            Requiredreturn = Requiredreturnlist[i]

            if (Dgrowthrate == Requiredreturn):
                return
            stockPrice = (DperShare + (DperShare * Dgrowthrate)) / (Requiredreturn - Dgrowthrate)
            print(f"DDM says buy {ticker_list[i]} at {stockPrice} or bellow to get expected return")
            return stockPrice
        else:
            return

def Grahamformula(EPS, growth, AAAbondyield, i):
    while i < len(ticker_list):
        if Grahamappropriate[i] == True:
            stockPrice = (EPS * (8.5 + (2 * growth[i])) * 4.4) / AAAbondyield
            print(f"Graham says: price target of {stockPrice} for {ticker_list[i]}")
            return stockPrice
        else:
            return
# WHAT TO DO::: MAKE EPS INFO AND DIVINFO COUNT YEAR ON YEAR CHANGES NOT TOTAL CHANGES!
def EPSinfo(company):
    annual = company.income_stmt
    HEPS = annual.loc['Basic EPS'].dropna()

    HEPS.index = HEPS.index.astype(str).str[:4].astype(int)

    HEPS = HEPS.sort_index()

    HEPS = HEPS[HEPS.index >= 2020]

    if len(HEPS) < 2:
        print("Not enough EPS data to calculate growth from 2021 onwards.")
        return

    print("Presenting useful information for Graham formula (Basic EPS growth since 2021) \n")
    for i in range(1, len(HEPS)):
        year = HEPS.index[i]
        prev_year = HEPS.index[i - 1]

        if prev_year >= 2020:
            current = HEPS.loc[year]
            previous = HEPS.loc[prev_year]

            if previous != 0:
                pct_change = ((current - previous) / abs(previous)) * 100
            else:
                pct_change = float('inf')

        print(f"Percentage change for {year}: {pct_change:.2f}%")

    print("\n")

def DIVinfo(company):
    HDIV = company.dividends.dropna()

    HDIV.index = pd.to_datetime(HDIV.index)

    current_year = pd.Timestamp.today().year
    HDIV = HDIV[HDIV.index.year < current_year]

    annual_dividends = HDIV.groupby(HDIV.index.year).sum()

    annual_dividends = annual_dividends.sort_index()

    if len(annual_dividends) < 2:
        print("Not enough data to calculate year-over-year dividend growth.")
        return

    print("Presenting useful information for DDM model formula (Dividend history)\n")

    for i in range(1, len(annual_dividends)):
        year = annual_dividends.index[i]
        prev_year = annual_dividends.index[i - 1]

        current = annual_dividends.iloc[i]
        previous = annual_dividends.iloc[i - 1]

        if previous == 0:
            pct_change = float('inf')
        else:
            pct_change = ((current - previous) / previous) * 100

        print(f"Percentage change for {year} (vs {prev_year}): {pct_change:.2f}%")

    print("\n")


while i < (len(ticker_list)):
    company = yf.Ticker(ticker_list[i])
    fundamentalinfo = company.info
    print("Choose what you need")
    print("1 - have company info")
    print("2 - calculate a price target and intrinsic value")
    action = input(": ")
    if action == "1":
        DIVinfo(company)
        EPSinfo(company)

    EPS = fundamentalinfo['epsTrailingTwelveMonths']
    Price = fundamentalinfo['currentPrice']
    PEG = fundamentalinfo['trailingPegRatio']

    try:
        Dyield = fundamentalinfo['dividendYield']
        if Dyield is None:
            raise ValueError("Dividend yield is None")
    except (KeyError, ValueError):
        Dyield = 0  

    Dyield_calc = Dyield/100
    DperShare = Price*Dyield_calc
    PEratio = Price/EPS

    if action == "2":
        Dividend_growth_rate_calc(DperShare, i)
        Grahamformula(EPS, GrowthRate, AAAbondyield, i)
    i += 1