import pandas as pd
from datetime import date

today=date.today().strftime('%Y%m%d')

colsprice = ['ticker',
             'chgPct6M',
             'chgPctMovAvg100D',
             'pxLast',
             'bestTargetPrice',
             'eqyRawBeta6M',
             'volatility360D',
             'bestPeRatio',
             'industryGroup']

cols = ['ticker',
        'name',
        'chgPct1D',
        'pxLast',
        'bestTargetPrice',
        'eqyRawBeta6M',
        'bdvdProjDivAmt',
        'esgLinkedBonus',
        'industryGroup']

fin_str = ['ticker',
         'waccNetOperProfit',
         'degreeFinancialLeverage',
         'degreeOperatingLeverage',
         'cfNetInc',
         'cfFreeCashFlow',
          'industryGroup']

cap_ret = ['ticker',
         'salesRevTurn',
         'operMargin',
         'bdvdNextProjAct',
         'bdvdProjDivAmt',
         'retrnOnCommnEqtyAdjstd',
         'returnOnInvCapital',
         'waccTotalInvCapital',
         'bestPeRatio',
          'industryGroup']

fundamentals = ['ticker',
         'bestPeRatio',
         'ebitdaToRevenue',
         'currentEvToT12mEbitda',
         'netIncome',
         'cfNetInc',
         'cfFreeCashFlow',
         'freeCashFlowEquity',
         'freeCashFlowMargin',
         'freeCashFlowPerSh',
         'industryGroup']

# Tracking Daily Movers

##### a) Top 20 daily growth

port = pd.read_csv('minhaReq2.20220126.csv', index_col=False)
dailymovers = port[cols].sort_values(by='chgPct1D',ascending=False).fillna('-').set_index('ticker')
dailymovers.head(20)

##### b) Top 20 daily loss 

dailymovers.tail(20)

port.columns

# Tracking the Price Movement - Medium Term

pricetracker = port[colsprice].sort_values(by='chgPct6M',ascending=False).set_index('ticker').head(20).fillna('-')
pricetracker

pricetrackerloss = port[colsprice].sort_values(by='chgPct6M',ascending=False).set_index('ticker').tail(20).fillna('-')
pricetrackerloss

P_t = port[colsprice].set_index('ticker').fillna('0')
P_t['bestTargetPrice'] = P_t['bestTargetPrice'].astype(float)

p_e = P_t[P_t['bestTargetPrice'] != 0.0]
p_e['pE'] = p_e['bestTargetPrice'] / p_e['pxLast'] -1
p_e.sort_values(by='pE', ascending=False)

# Ranking by ANR Growth Potential

p_e = P_t[P_t['bestTargetPrice'] != 0.0]
p_e['pE'] = p_e['bestTargetPrice'] / p_e['pxLast'] -1
p_e.sort_values(by='pE', ascending=False)
#p_e.info()
#p_e['pE'].map("{:.2%}".format).sort_values(ascending=False)
#p_e.head(20)

#p_e.sort_values(by='pE',ascending=False)

# Tracking Financial Exposure

exposure = port[fin_str].sort_values(by='degreeFinancialLeverage',ascending=True).set_index('ticker').fillna('-')
exposure.head(20)

# Tracking Return on Invested Capital

cap_return = port[cap_ret].sort_values(by='returnOnInvCapital',ascending=False).set_index('ticker').fillna('-')
cap_return.head(20)

# Tracking Fundamental Data

fund_data = port[fundamentals].sort_values(by='ebitdaToRevenue',ascending=False).set_index('ticker').fillna(0)
fund_data.head(20)

# Comparing Fundamental Data Across Industry Groups

grupos = ['Diversified Finan Serv', 'Software', 'REITS',
       'Commercial Services', 'Real Estate', 'Electric', 'Semiconductors',
       'Computers', 'Internet', 'Oil&Gas Services', 'Healthcare-Products',
       'Private Equity', 'Cosmetics/Personal Care', 'Oil&Gas', 'Retail',
       'Home Furnishings', 'Auto Manufacturers', 'Pharmaceuticals',
       'Apparel', 'Biotechnology', 'Banks', 'Insurance']

#We can add .to_excel(grupo+".xlsx") if we want each of the tables exported to Excel

for grupo in grupos:
    industria = fund_data[fund_data['industryGroup'] == str(grupo)].sort_values(by='ebitdaToRevenue',ascending=False)
    display(industria)
