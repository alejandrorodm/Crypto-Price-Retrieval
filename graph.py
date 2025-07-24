"""
This module contains the functions to represent the data in a candlestick chart.
    Author: MrSh4d0w

"""

import mplfinance as mpf
import pandas as pd
import matplotlib.pyplot as plt



def represent_graphic(data, mav=(5, 20, 50)):
    """Represent the data in a candlestick chart. 
    If you want to take the data of an excel file use:  pd.read_excel(excel_file)
    You can take the first x elements with: data.head(x)
    You can take the last x elements with: data.tail(x)

    Args:
        data (dataframe): list of dictionaries with the data to represent
        mav (tuple): moving averages (default: (5, 20, 50))
    """

    # Convert the date column to datetime format
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s')

    # Set the date column as the index of the DataFrame
    data.set_index('Timestamp', inplace=True)

    # Sort the DataFrame by the index (dates) in ascending order
    data.sort_index(ascending=True, inplace=True)

    # Plot the candlestick chart
    mpf.plot(data, type='candle', style='yahoo', volume=True, mav=(5, 20, 50))

def represent_graphic_excel(excelFile, mav=(5, 20, 50)):
    """Represent the data in a candlestick chart from an excel file. 
    If you want to take the data of an excel file use:  pd.read_excel(excel_file)
    You can take the first x elements with: data.head(x)
    You can take the last x elements with: data.tail(x)
    Args:
        excelFile (str): path to the excel file            
        mav (tuple): moving averages (default: (5, 20, 50))
    """

    # Read the excel file into a DataFrame
    data = pd.read_excel(excelFile, skiprows=3)

    # Convert the date column to datetime format
    data['Timestamp'] = pd.to_datetime(data['Timestamp'], unit='s')

    # Set the date column as the index of the DataFrame
    data.set_index('Timestamp', inplace=True)

    # Sort the DataFrame by the index (dates) in ascending order
    data.sort_index(ascending=True, inplace=True)
    
    # Extract the names of EMA columns
    ema_names = [col for col in data.columns if 'EMA_Close_' in col]

    # Extract RSI Stochastic columns    
    rsi_stoch_names = ['Stoch_RSI', '%K', '%D']

    # Create addplot for EMAs
    apdict_ema = mpf.make_addplot(data[ema_names], mav=mav)

    # Create addplot for RSI Stochastic
    try:
        apdict_rsi_stoch = mpf.make_addplot(data[rsi_stoch_names], panel=1, secondary_y=False)
    except:
        print("Stoch RSI not found")
        apdict_rsi_stoch = None
    
    buy_signals = data[data['Signal'] == 1]
    sell_signals = data[data['Signal'] == -1]
    
    apdict_signals = [
        mpf.make_addplot(buy_signals['Close'], type='scatter', marker='^', color='green', markersize=100),
        mpf.make_addplot(sell_signals['Close'], type='scatter', marker='v', color='red', markersize=100)
    ]
    
    # Plot candlestick chart with volume, EMAs, and RSI Stochastic
    mpf.plot(data, type='candle', style='yahoo', volume=True, addplot=[apdict_ema, apdict_rsi_stoch, apdict_signals], panel_ratios=(2,1))

