import yfinance as yf
import pandas_datareader.data as web
import datetime
import pandas as pd
import math
ticker_list = ['BRK-B']
Dgrowthratelist = [0.02]
Requiredreturnlist = [0.1]
DDMappropriate = [True]
Grahamappropriate = [True]

GrowthRate = [5]#graham formula uses % not decimal

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

    HEPS = annual.loc['Basic EPS']

    last_value = HEPS.iloc[-1]

    percentage_changes = {}

    if pd.isnull(HEPS).values.any():
        last_value = HEPS.iloc[-2]

    print("Presenting usefull information for graham formula (Basic EPS growth since 2020) \n")

    for date, value in HEPS.items():
        if pd.notna(value): 
            pct_change = ((value - last_value) / last_value) * 100
            percentage_changes[date] = pct_change

    for date, pct_change in percentage_changes.items():
        print(f"Percentage change for {date}: {pct_change:.2f}%")
    
    print("\n")

def DIVinfo(company):
    annual = company

    HDIV= annual.dividends
    HDIV = HDIV[::-1]
    print(HDIV)
    last_value = HDIV.iloc[-1]

    percentage_changes = {}

    #if pd.isnull(HDIV).values.any():
        #last_value = HDIV.iloc[-2]

    print("Presenting usefull information for DDM model formula (Dividend history) \n")

    for date, value in HDIV.items():
        if pd.notna(value): 
            pct_change = ((value - last_value) / last_value) * 100
            percentage_changes[date] = pct_change

    for date, pct_change in percentage_changes.items():
        print(f"Percentage change for {date}: {pct_change:.2f}%")
    
    print("\n") 



while i < (len(ticker_list)):
    company = yf.Ticker(ticker_list[i])
    fundamentalinfo = company.info
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

    Dividend_growth_rate_calc(DperShare, i)
    Grahamformula(EPS, GrowthRate, AAAbondyield, i)
    i += 1