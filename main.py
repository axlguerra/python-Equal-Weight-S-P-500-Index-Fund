import numpy as np
import pandas as pd
import requests
import xlsxwriter
import math
from pprint import pprint

IEX_CLOUD_API_TOKEN = 'Tpk_059b97af715d417d9f49f50b51b1c448'
####Equal-Weight S&P 500 Index Fund



# Introduction & Library Imports
# The S&P 500 is the world's most popular stock market index. The largest fund that is
# benchmarked to this index is the SPDR® S&P 500® ETF Trust.
# It has more than US$250 billion of assets under management.




# Getting the 500 stock index is done through a paid API but this time I saved the 500 stocks from another
# source into a csv file


stocks = pd.read_csv('sp_500_stocks.csv')


# sandbox mode of IEX CLOUD API it returns randomnized financial data

symbol = 'AAPL'
API_END_POINT = 'https://sandbox.iexapis.com'
#
url = f'{API_END_POINT}/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}'
#
data = requests.get(url=f'{API_END_POINT}/stable/stock/{symbol}/quote/?token={IEX_CLOUD_API_TOKEN}')

#marketCap
# price = data.json()['latestPrice']
# market_cap = data.json()['marketCap']/1000000000000

# print(data.json())
# print(price)
# print(market_cap)

#
# # add all stocks and prices to a pandas dataframe
my_columns = ['Ticker', 'stock Price', 'Market Cap', 'Number of shares to buy']

# final_dataframe = pd.DataFrame([[0,0,0,0]],columns=my_columns)
# print(final_dataframe)
final_dataframe = pd.DataFrame(columns=my_columns)

# for stock in stocks['Ticker'][:1]:
#
#
#
#     url = f'{API_END_POINT}/stock/{stock}/quote/?token={IEX_CLOUD_API_TOKEN}'
#
#     data = requests.get(url=f'{API_END_POINT}/stable/stock/{stock}/quote/?token={IEX_CLOUD_API_TOKEN}')
#
#     price = data.json()['latestPrice']
#     market_cap = data.json()['marketCap'] / 1000000000000
#
#     final_dataframe= final_dataframe.append(
#         pd.Series(
#             [
#                 stock,
#                 price,
#                 market_cap,
#                 'N/A'
#             ], index=my_columns
#
#         ),
#         ignore_index=True
#     )



def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# print(stocks['Ticker'])
symbol_group = list(chunks(stocks['Ticker'], 100))
# print(symbol_group)
symbol_strings = []
for i in range(0, len(symbol_group)):
    symbol_strings.append((',').join(symbol_group[i]))


for symbol_string in symbol_strings:
    # print(symbol_string)
    batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote&token={IEX_CLOUD_API_TOKEN}'
    data = requests.get(batch_api_call_url).json()
    for symbol in symbol_string.split(','):



        final_dataframe = final_dataframe.append(
                pd.Series(
                    [
                        symbol,
                        data[symbol]['quote']['latestPrice'],
                        data[symbol]['quote']['marketCap']/1000000000000,
                        'NA'
                    ],
                    index=my_columns
                ),

                ignore_index=True,
            )

# print(final_dataframe)



#Calculate number of shares to buy

portfolio_size = input('Enter the value of your portfolio: $')

try:
    val = float(portfolio_size)
except ValueError:
    print('Please enter an integer')
    portfolio_size = input('Enter the value of your portfolio: $')
    val = float(portfolio_size)

position_size = val/len(final_dataframe.index)


for i in range(0, len(final_dataframe.index)):

    final_dataframe.loc[i,'Number of shares to buy'] = math.floor(position_size/final_dataframe.loc[i, 'stock Price'])

# print(final_dataframe)

writer = pd.ExcelWriter('recommended_trades.xlsx', engine='xlsxwriter')
final_dataframe.to_excel(writer, 'Recommended Trades', index=False)

background_color = '#080823'
font_color = '#ffffff'
string_format = writer.sheets['Recommended Trades']
writer.save()

# Create an API CALL for each stock
# for stock in stocks['Ticker']:
#
#     url = f'{API_END_POINT}/stock/{stock}/quote/?token={IEX_CLOUD_API_TOKEN}'
#
#     data = requests.get(url=f'{API_END_POINT}/stable/stock/{stock}/quote/?token={IEX_CLOUD_API_TOKEN}')
#
#     price = data.json()['latestPrice']
#     market_cap = data.json()['marketCap'] / 1000000000000
#
#     final_dataframe = final_dataframe.append(
#         pd.Series(
#             [
#                 stock,
#                 price,
#                 market_cap,
#                 'NA'
#             ],
#             index=my_columns
#         ),
#
#         ignore_index=True,
#     )
#



#BATCH API
#doing single API calls takes TOO LONG ALMOST 8 MINUTES
#




# for stock in stocks['Ticker']:
#
    # symbol_group = list(chunks(stocks['Ticker'], 100))
#     symbol_strings = []
#     for i in range(0, len(symbol_group)):
#         symbol_strings.append(','.join(symbol_group[i]))
#
#     for symbol_string in symbol_strings[:1]:
#         # print(symbol_string)
#         batch_api_call_url = f'https://sandbox.iexapis.com/stable/stock/market/batch?symbols={symbol_string}&types=quote&token={IEX_CLOUD_API_TOKEN}'
#         data = requests.get(batch_api_call_url)
#
#         for symbol in symbol_string.split(','):
#             print(symbol)


        # print(data.status_code)
        # print(batch_api_call_url)
    # url = f'{API_END_POINT}/stock/{stock}/quote/?token={IEX_CLOUD_API_TOKEN}'
    #
    # data = requests.get(url=f'{API_END_POINT}/stable/stock/{stock}/quote/?token={IEX_CLOUD_API_TOKEN}')
    #
    # price = data.json()['latestPrice']
    # market_cap = data.json()['marketCap'] / 1000000000000
    #
    # final_dataframe = final_dataframe.append(
    #     pd.Series(
    #         [
    #             stock,
    #             price,
    #             market_cap,
    #             'NA'
    #         ],
    #         index=my_columns
    #     ),
    #
    #     ignore_index=True,
    # )
    #





# print(final_dataframe)
