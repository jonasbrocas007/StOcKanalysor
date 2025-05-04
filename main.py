import yfinance as yf
import pandas_datareader.data as web
import datetime
import pandas as pd
import math

i = 0

start = datetime.datetime.today() - datetime.timedelta(days=10)
end = datetime.datetime.today()

aaa_yield = web.DataReader('DAAA', 'fred', start, end)
AAAbondyield = aaa_yield.dropna().iloc[-1, 0]

def Dividend_growth_rate_calc(DperShare, i, ticker, Dgrowthrate, Requiredreturn):
    if (Dgrowthrate == Requiredreturn):
        return
    stockPrice = (DperShare + (DperShare * Dgrowthrate)) / (Requiredreturn - Dgrowthrate)
    print(f"DDM says buy {ticker} at {stockPrice} or bellow to get expected return")
    return stockPrice


def Grahamformula(EPS, growth, AAAbondyield, i, ticker):
    stockPrice = (EPS * (8.5 + (2 * growth)) * 4.4) / AAAbondyield
    print(f"Graham says: price target of {stockPrice} for {ticker}")
    return stockPrice

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

def common(company):
    company = yf.Ticker(company)
    fundamentalinfo = company.info

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

    return {
        "Price": Price,
        "EPS": EPS,
        "PEratio": PEratio,
        "PEG": PEG,
        "Dyield": Dyield,
        "DperShare": DperShare
    
    }


while True:
    action = input(": ")

    if action == "quit":
        quit()

    if action.startswith("analyse"):
        action = action.replace("analyse ", "")
        pricedata = common(action)

        DIVinfo(yf.Ticker(action))
        EPSinfo(yf.Ticker(action))

        print(f"Most current price is {pricedata['Price']}")
        print(f"Earnings per share is {pricedata['EPS']}")
        print(f"The PE ratio is {pricedata['PEratio']}")
        print(f"The PEG is {pricedata['PEG']}")
        print(f"The Dividend yield is {pricedata['Dyield']}")

    elif action.startswith("graham "):
        action = action.replace("graham ", "")
        ticker = action.split(' ')

        data = common(str(ticker[0]))
        GrowthRate = float(ticker[1])

        Grahamformula(data['EPS'], GrowthRate, AAAbondyield, i, action)

    elif action.startswith("ddm "):
        action = action.replace("ddm ", "")
        ticker = action.split(' ')

        data = common(str(ticker[0]))

        Dividend_growth_rate_calc(data["DperShare"], i, ticker[0], float(ticker[1]), float(ticker[2]))

    elif action == "help":
        print("type analyse ticker to get analyses")
        print("type graham ticker to get the graham valuation")
        print("type ddm ticker to get the ddm valuation")

        print("example: analyse BCP.LS")
        print("example: graham BCP.LS 40 (40 percent eps growth)")
        print("example: ddm BCP.LS 0.01 0.1 (0.01 dividend growth and 0.01 expect return)")


    i += 1
