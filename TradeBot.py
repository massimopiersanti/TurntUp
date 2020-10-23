#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 13:12:33 2020

@author: aprillowry
"""


import alpaca_trade_api as tradeapi

api = tradeapi.REST('PKIK0Y04MGOFO5B5KKCU', 'Cj5IXI0vEHh6O2IHoItZ5j6gfs96kyLBr3d7363X', base_url='https://paper-api.alpaca.markets')


# api.submit_order(
#     symbol='AAPL',
#     qty=1,
#     side='buy',
#     type='market',
#     time_in_force='gtc'
# )

# print(api.list_positions())

# barset is just a dictionary data type that contains the open price(o), high and low price(h, l) time(t dont give shit about 
# this one) and volume v.
# when we put limit 5 this is getting the barset for apple over the past 5 days(ie the week trading period)
barset = api.get_barset('AAPL', 'day', limit=5)
aapl_bars=barset['AAPL']
print(aapl_bars)

# the data for week open is contained at index 0, the data for week end is contained in last index of the barset 
# which can be accessed with index -1
week_open = aapl_bars[0].o
week_close = aapl_bars[-1].c
percent_change = (week_close - week_open) / week_open * 100
#print('AAPL moved {}% over the last 5 days'.format(percent_change))

# so this shows an example of placing a buy order if the stock has moved >5% positively over the last week
# or a sell order if it has dropped more than 5% over same interval
# -- not what we are doing with volume, but wanted to show example
if percent_change > 5:
    api.submit_order(
    symbol='AAPL',
    qty=1,
    side='buy',
    type='market',
    time_in_force='gtc'
    )
   
if percent_change < -5:
    api.submit_order(
    symbol='AAPL',
    qty=1,
    side='sell',
    type='market',
    time_in_force='gtc'    
    )


# to check if maybe momentum is building for a stock over the week, compare volume on last day to volume on first day
week_open_volume = aapl_bars[0].v
week_close_volume = aapl_bars[-1].v
volume_percent_change = (week_close_volume - week_open_volume) / week_open_volume *100
print(volume_percent_change)

# so clearly this week we dropped a buttload in volume, 40% fewer shares were traded on friday than on monday
# if our gameplan is to try and simply ride a stock that has momentum, having fewer shares traded means less activity
# around the stock and less of a chance to ride large movements either upwards or downwards

# if momentum was building and our percent chance was positive we maybe want to buy and ride some momentum
# so for this weak ass example we buy a share if our share price increased 5% over the last week and the volume of
#shares traded is 20% higher at end of week 
if (percent_change > 5 ) and (volume_percent_change > 20):
    api.submit_order(
    symbol='AAPL',
    qty=1,
    side='buy',
    type='market',
    time_in_force='gtc'    
    )