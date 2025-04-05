import yfinance as yf
ticker_list = ['AAPL', 'NKE', 'EDP.LS']
Dgrowthratelist = [0.08, 0.07, 0.008]
Requiredreturnlist = [0.1, 0.1, 0.1]
DDMappropriate = [False, False, True]
Grahamappropriate = [True, False, True]

GrowthRate = [17, 5, 0] #graham formula uses % not decimal

i = 0

lqd = yf.Ticker('LQD')
lqd_history = lqd.history(period="1d")
AAAbondyield= lqd.info['dividendYield']

#Using lqd as AAA corporate bonds is inneficient


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
  