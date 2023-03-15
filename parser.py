# The idea of this script is to run a showcase on how to parse a csv file, with data from my portfolio
# For that we'll only use pandas

import pandas as pd

# From the dataset I'll run different portfolio analysis by filtering only certain columns out of the dataset at a time
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

# First, we'll show the daily movers, that is, the instruments high higher price change in 1 day (column chgPct1D)
# Tracking Daily Movers

##### a) Top 20 daily growth

#Import the .csv file as a dataframe
port = pd.read_csv('minhaReq2.20220126.csv', index_col=False)
# From the imported dataframe we'll only use the cols columns and sort them by 'chgPct1D' in descending order
dailymovers = port[cols].sort_values(by='chgPct1D',ascending=False).fillna('-').set_index('ticker')
# Diplaying only the first 20 records with .head()
dailymovers.head(20)

##### b) Top 20 daily loss 

# Diplaying only the last 20 records with .tail()
dailymovers.tail(20)

# Tracking the Price Movement - Medium Term

# Now following the same steps but sorting by the column 'chgPct6M' which represents the change in price for the last 6 months.
# The idea is to get a medium term price change
pricetracker = port[colsprice].sort_values(by='chgPct6M',ascending=False).set_index('ticker').head(20).fillna('-')
pricetracker

pricetrackerloss = port[colsprice].sort_values(by='chgPct6M',ascending=False).set_index('ticker').tail(20).fillna('-')
pricetrackerloss

# Creating a new column to calculate the difference between Analyst Recommendations and last price
P_t = port[colsprice].set_index('ticker').fillna('0')
P_t['bestTargetPrice'] = P_t['bestTargetPrice'].astype(float)

p_e = P_t[P_t['bestTargetPrice'] != 0.0]
p_e['pE'] = p_e['bestTargetPrice'] / p_e['pxLast'] -1
p_e.sort_values(by='pE', ascending=False)

# Ranking by Growth Potential (Analyst Recommendation / Last Price)

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
    industria
