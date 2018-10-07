#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  5 23:35:02 2018

@author: jiayipan
"""

""""Original strategy:
    
"""


# Here you can
# 1. import necessary python packages for your strategy
# 2. Load your own facility files containing functions, trained models, extra data, etc for later use
# 3. Set some global constants
# Note:
# 1. You should put your facility files in the same folder as this strategy.py file
# 2. When load files, ALWAYS use relative path such as "data/facility.pickle"
# DO NOT use absolute path such as "C:/Users/Peter/Documents/project/data/facility.pickle"

import pandas as pd

asset_index = 1  # only consider BTC (the **second** crypto currency in dataset)
mid_window = 55  # the middle-length average period
short_window = 8  # the short-length average period
extra_memry = 1  # the number of extra data we will record in memory
memry_length = mid_window + extra_memry  # we add one to check the change of Moving Averages, more details below
t = 4

# enlarge_para = 1.05
# shrinken_para = 0.95


# Here is your main strategy function
# Note:
# 1. DO NOT modify the function parameters (time, data, etc.)
# 2. The strategy function AWAYS returns two things - position and memory:
# 2.1 position is a np.array (length 4) indicating your desired position of four crypto currencies next minute
# 2.2 memory is a class containing the information you want to save currently for future use


def handle_bar(counter,  # a counter for number of minute bars that have already been tested
               time,  # current time in string format such as "2018-07-30 00:30:00"
               data,  # data for current minute bar (in format 2)
               init_cash,  # your initial cash, a constant
               transaction,  # transaction ratio, a constant
               cash_balance,  # your cash balance at current minute
               crypto_balance,  # your crpyto currency balance at current minute
               total_balance,  # your total balance at current minute
               position_current,  # your position for 4 crypto currencies at this minute
               memory  # a class, containing the information you saved so far
               ):
    # We use Moving Average Convergence Divergence to indicate when to long and when to short.
    # Every time we decide what to do, we calculate the mean of the past few minutes.
    # Let's call the 26-minute average as "mid", and the 13-minute average as "short"
    # once "short" surpasses "mid", it is a to-long signal
    # once "mid" surpasses "short", it is a to-short signal
    # otherwise we do nothing
    # in order to lower the transition cost, we receive the signal every 13 minutes
    # (in the beginning, we receive the signal every minute, but the transition cost is high, so we kept losing money)
    # once we receive the signal, we long/short everything we have, in order to amplify the effect

    # Get position of last minute
    position_new = position_current  # to record the current position

    # Since we do not want a large memory to crash the program, we need to set up an index 'r' first
    if (counter == 0):
        memory.data_save = pd.DataFrame(columns = ['close', 'high', 'low', 'open', 'volume']) # to create an empty DataFrame with column names
        memory.data_save2 = pd.DataFrame(columns = ['close', 'high', 'low', 'open', 'volume']) # to create an empty DataFrame with column names
        memory.signal_buy=None
        memory.signal_sell=None
        memory.t_increment=0
        memory.t=0
    #r = counter % memry_length # This is to record the order of this data recorded in our memory        
    memory.data_save.loc[counter] = data[asset_index,] # record the first data we met in the memory

# When the number of data recorded exceed the length of the memory we desire, we can start to make decisions about buying and selling.

    if (counter >= memry_length - 1): 
        for i in range(0, memry_length):
            # we set up a new memory recording the past few data in the order of time
            memory.data_save2.loc[i] = memory.data_save.loc[len(memory.data_save)-memry_length+i] #? not sure if it works yet
    
        memory.data_save2['average'] = (memory.data_save2['close'] + memory.data_save2['high'] + memory.data_save2['low'] + memory.data_save2['open']) / 4
        memory.data_save2['short_mavg'] = memory.data_save2.average.rolling(window=short_window).mean()
        memory.data_save2['mid_mavg'] = memory.data_save2.average.rolling(window=mid_window).mean()
        memory.data_save2['MACD'] = memory.data_save2['short_mavg'] - memory.data_save2['mid_mavg']
        if (memory.data_save2.iloc[len(memory.data_save2) - 2]['MACD'] < 0 and memory.data_save2.iloc[len(memory.data_save2) - 1]['MACD'] > 0):
            position_new[asset_index] = 10
        elif (memory.data_save2.iloc[len(memory.data_save2) - 2]['MACD'] > 0 and memory.data_save2.iloc[len(memory.data_save2) - 1]['MACD'] < 0):
            position_new[asset_index] = -8
  
    if (counter == 58 or counter ==60):
        print(memory.data_save2)
    #        roll_short_old = roll_short
    #        roll_mid_old = roll_mid

    # End of strategy
    return position_new, memory



