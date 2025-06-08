import pandas as pd
import logging
import os

# Set up logging
logging.basicConfig(filename='parser.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
logging.info("Script started")

try:
    colsprice = ['ticker', 'chgPct6M', 'chgPctMovAvg100D', 'pxLast', 'bestTargetPrice', 'eqyRawBeta6M', 'volatility360D', 'bestPeRatio', 'industryGroup']
    cols = ['ticker', 'name', 'chgPct1D', 'pxLast', 'bestTargetPrice', 'eqyRawBeta6M', 'bdvdProjDivAmt', 'esgLinkedBonus', 'industryGroup']
    fin_str = ['ticker', 'waccNetOperProfit', 'degreeFinancialLeverage', 'degreeOperatingLeverage', 'cfNetInc', 'cfFreeCashFlow', 'industryGroup']
    cap_ret = ['ticker', 'salesRevTurn', 'operMargin', 'bdvdNextProjAct', 'bdvdProjDivAmt', 'retrnOnCommnEqtyAdjstd', 'returnOnInvCapital', 'waccTotalInvCapital', 'bestPeRatio', 'industryGroup']
    fundamentals = ['ticker', 'bestPeRatio', 'ebitdaToRevenue', 'currentEvToT12mEbitda', 'netIncome', 'cfNetInc', 'cfFreeCashFlow', 'freeCashFlowEquity', 'freeCashFlowMargin', 'freeCashFlowPerSh', 'industryGroup']

    # Import the .csv file as a dataframe
    port = pd.read_csv('minhaReq2.20220126.csv', index_col=False)
    logging.info("CSV file loaded successfully")
    logging.info(f"Number of records in CSV: {len(port)}")

    dailymovers = port[cols].sort_values(by='chgPct1D', ascending=False).fillna('-').set_index('ticker')
    pricetracker = port[colsprice].sort_values(by='chgPct6M', ascending=False).set_index('ticker').head(20).fillna('-')

    # Ensure docs directory exists
    os.makedirs("docs", exist_ok=True)

    # Save tables as HTML for GitHub Pages
    dailymovers.head(20).to_html("docs/dailymovers.html", classes="table table-striped", border=0)
    pricetracker.to_html("docs/pricetracker.html", classes="table table-striped", border=0)
    logging.info("Tables exported as HTML to docs/.")

except Exception as e:
    logging.error(f"Error occurred: {e}")
    print(f"Error occurred: {e}")
