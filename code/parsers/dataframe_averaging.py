#!/usr/bin/env python3

###pdsAveraging.py contains helper functions to calculate average values for
####time series of data stored in a pandas data frame
####usually called by insituTXT_2_JSON.py

__author__= "Madison.Soden"
__date__= "Thu Sep 27, 2018  06:32PM"
__license__= "NA?"
__email__= "madison.soden@gmail.com"
__status__= "Production"

import pandas as pd 
import numpy as np
import json 
import datetime

def cleanDataframe( df):
    df= df.reindex(pd.date_range( df.index[1], df.index[-1], freq='H'))
    return df

def MperS_Knots( x):
    """function to convert meters per second to knots"""
    return float(x/0.51444444444)

def convert_MS_to_Knots( df): 
    df["WSPD"]= df["WSPD"].apply(MperS_Knots)
    return df

def append_3H_Mean( columnname, df):
# every third column should be used to avoid overlapping means
    timeseries= df.rolling(window=3, min_periods= 1)[columnname].mean()
    #timeseries= df[columnname]
    timeseries= timeseries.asfreq('3H')
    timeseries= timeseries.reindex(df.index.values)
    timeseries.name= columnname+'_three_hour_mean'
    df[columnname+'_three_hour_mean'] = timeseries
    return df

def append_3D_Mean( columnname, df):
    timeseries= df.rolling(window=72, min_periods= 1, center=True)[columnname].mean()
    #timeseries= df[columnname]
    timeseries= timeseries.asfreq('3D')
    timeseries= timeseries.reindex(df.index.values)
    timeseries.name= columnname+'_three_day_mean'
    df[columnname+'_three_day_mean'] = timeseries
    return df

def append_30D_Mean (columnname, df):
    timeseries= df.rolling(window=720, min_periods= 1)[columnname].mean()
    #timeseries= df[columnname]
    timeseries= timeseries.asfreq('30D')
    timeseries= timeseries.reindex(df.index.values)
    timeseries.name= columnname+'_30day_rolling_mean'
    df[columnname+'_30day_rolling_mean'] = timeseries
    return df


def removeExtraDateTime( df):
    df= df.drop(['YYYY', 'MM', 'DD', 'hh'], axis=1)
    if('mm' in df.columns.values):
        df= df.drop(['mm'], axis=1)
    return df

def cuttimeseries( df):
    datetimes= df.index.tolist()
    start = -9
    end = -9
    for i in range(len(datetimes)):
        if datetimes[i].time() == datetime.time( 5, 0, 0):
            start = i
            break
    for i in reversed(range(len(datetimes))):
        if datetimes[i].time() == datetime.time( 5, 0, 0):
            end = i
            break
    if (start==-9):
        return None
    df= df[start:(end)]
    return df
