import yfinance as yf
import pandas_datareader.data as web
import datetime
ticker_list = ['PG']
Dgrowthratelist = [0.12]
Requiredreturnlist = [0.13]
DDMappropriate = [True]
Grahamappropriate = [True]

GrowthRate = [3]#graham formula uses % not decimal

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
            print(f"DDM says {stockPrice} for {ticker_list[i]}")
            return stockPrice
        else:
            return

def Grahamformula(EPS, growth, AAAbondyield, i):
    while i < len(ticker_list):
        if Grahamappropriate[i] == True:
            stockPrice = (EPS * (8.5 + (2 * growth[i])) * 4.4) / AAAbondyield
            print(f"Graham says: {stockPrice} for {ticker_list[i]}")
            return stockPrice
        else:
            return



while i < (len(ticker_list)):
    company = yf.Ticker(ticker_list[i])
    fundamentalinfo = company.info

    EPS = fundamentalinfo['epsTrailingTwelveMonths']
    Price = fundamentalinfo['currentPrice']
    PEG = fundamentalinfo['trailingPegRatio']
    Dyield = fundamentalinfo['dividendYield']
    Dyield_calc = Dyield/100
    DperShare = Price*Dyield_calc
    PEratio = Price/EPS

    Dividend_growth_rate_calc(DperShare, i)
    Grahamformula(EPS, GrowthRate, AAAbondyield, i)
    i += 1
  