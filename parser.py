# The idea of this script is to run a showcase on how to parse a csv file, with data from my portfolio
# For that we'll only use pandas

import pandas as pd
import logging  # Import logging module
import os  # Import os module for directory operations

# Configure logging
logging.basicConfig(filename='parser.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

logging.info("Script started")

try:
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

    # Import the .csv file as a dataframe
    port = pd.read_csv('minhaReq2.20220126.csv', index_col=False)
    logging.info("CSV file loaded successfully")
    logging.info(f"Number of records in CSV: {len(port)}")

    # From the imported dataframe we'll only use the cols columns and sort them by 'chgPct1D' in descending order
    dailymovers = port[cols].sort_values(by='chgPct1D',ascending=False).fillna('-').set_index('ticker')
    # Diplaying only the first 20 records with .head()
    dailymovers.head(20)
    logging.info("Top 20 daily growth calculated")
    logging.info(f"Number of records processed for daily growth: {len(dailymovers)}")

    # Diplaying only the last 20 records with .tail()
    dailymovers.tail(20)
    logging.info("Top 20 daily loss calculated")
    logging.info(f"Number of records processed for daily loss: {len(dailymovers)}")

    # Ensure docs directory exists
    os.makedirs('docs', exist_ok=True)
    
    # Export dailymovers top 20 and bottom 20 as HTML
    dailymovers_top20 = dailymovers.head(20)
    dailymovers_bottom20 = dailymovers.tail(20)
    
    # Combine top gainers and losers for the dailymovers table
    dailymovers_combined = pd.concat([
        dailymovers_top20,
        pd.DataFrame([['---'] * len(dailymovers_top20.columns)], 
                    columns=dailymovers_top20.columns, 
                    index=['--- SEPARATOR ---']),
        dailymovers_bottom20
    ])
    
    dailymovers_combined.to_html('docs/dailymovers.html', 
                                table_id='dailymovers-table',
                                classes='table table-striped table-bordered',
                                escape=False)
    logging.info("Daily movers HTML table exported to docs/dailymovers.html")

    # Now following the same steps but sorting by the column 'chgPct6M' which represents the change in price for the last 6 months.
    pricetracker = port[colsprice].sort_values(by='chgPct6M',ascending=False).set_index('ticker').head(20).fillna('-')
    pricetracker
    logging.info("Medium term price change (growth) calculated")
    logging.info(f"Number of records processed for medium term price change (growth): {len(pricetracker)}")

    pricetrackerloss = port[colsprice].sort_values(by='chgPct6M',ascending=False).set_index('ticker').tail(20).fillna('-')
    pricetrackerloss
    logging.info("Medium term price change (loss) calculated")
    logging.info(f"Number of records processed for medium term price change (loss): {len(pricetrackerloss)}")

    # Export pricetracker as HTML (combining top performers and worst performers)
    pricetracker_combined = pd.concat([
        pricetracker,
        pd.DataFrame([['---'] * len(pricetracker.columns)], 
                    columns=pricetracker.columns, 
                    index=['--- SEPARATOR ---']),
        pricetrackerloss
    ])
    
    pricetracker_combined.to_html('docs/pricetracker.html',
                                 table_id='pricetracker-table',
                                 classes='table table-striped table-bordered',
                                 escape=False)
    logging.info("Price tracker HTML table exported to docs/pricetracker.html")

    # Creating a new column to calculate the difference between Analyst Recommendations and last price
    P_t = port[colsprice].set_index('ticker').fillna('0')
    P_t['bestTargetPrice'] = P_t['bestTargetPrice'].astype(float)

    p_e = P_t[P_t['bestTargetPrice'] != 0.0].copy()
    p_e.loc[:, 'pE'] = p_e['bestTargetPrice'] / p_e['pxLast'] - 1
    p_e.sort_values(by='pE', ascending=False)
    logging.info("Growth potential based on Analyst Recommendations calculated")
    logging.info(f"Number of records processed for growth potential: {len(p_e)}")

    # Tracking Financial Exposure
    exposure = port[fin_str].sort_values(by='degreeFinancialLeverage',ascending=True).set_index('ticker').fillna('-')
    exposure.head(20)
    logging.info("Financial exposure tracked")
    logging.info(f"Number of records processed for financial exposure: {len(exposure)}")

    # Tracking Return on Invested Capital
    cap_return = port[cap_ret].sort_values(by='returnOnInvCapital',ascending=False).set_index('ticker').fillna('-')
    cap_return.head(20)
    logging.info("Return on Invested Capital tracked")
    logging.info(f"Number of records processed for return on invested capital: {len(cap_return)}")

    # Tracking Fundamental Data
    fund_data = port[fundamentals].sort_values(by='ebitdaToRevenue',ascending=False).set_index('ticker').fillna(0)
    fund_data.head(20)
    logging.info("Fundamental data tracked")
    logging.info(f"Number of records processed for fundamental data: {len(fund_data)}")

    # Comparing Fundamental Data Across Industry Groups
    grupos = ['Diversified Finan Serv', 'Software', 'REITS',
           'Commercial Services', 'Real Estate', 'Electric', 'Semiconductors',
           'Computers', 'Internet', 'Oil&Gas Services', 'Healthcare-Products',
           'Private Equity', 'Cosmetics/Personal Care', 'Oil&Gas', 'Retail',
           'Home Furnishings', 'Auto Manufacturers', 'Pharmaceuticals',
           'Apparel', 'Biotechnology', 'Banks', 'Insurance']

    for grupo in grupos:
        industria = fund_data[fund_data['industryGroup'] == str(grupo)].sort_values(by='ebitdaToRevenue',ascending=False)
        industria
        logging.info(f"Fundamental data compared across industry group: {grupo}")
        logging.info(f"Number of records processed for industry group {grupo}: {len(industria)}")

    logging.info("Script completed successfully")

except Exception as e:
    logging.error("Error occurred: " + str(e))
    logging.info("Script terminated with errors")
