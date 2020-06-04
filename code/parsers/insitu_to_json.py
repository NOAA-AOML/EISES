#!/usr/bin/env python3

### insituTXT_to_JSON converts a data stream txt file (for a year of mlrf1) to A standardized JSON file format for
#### fact factories to process

__author__= "Madison.Soden"
__date__= "Thu Sep 27, 2018  06:32PM"
__license__= "NA?"
__email__= "madison.soden@gmail.com"
__status__= "Production"

import pandas as pd
import json
import datetime
import numpy as np
from .dataframe_averaging import * 
import configParameters as config

def main( filename):
    ###########################################################
    # 1.PARSING txt file 
    ###########################################################

    with open(config.data+'/data/'+ filename+'.txt', 'r') as fin:
        data = fin.read().splitlines(True)
    ##Parsing units and header
    header= data[0]
    header= header[:-1]
    headerp= header.split(' ')
    headerp= list(filter(None, headerp))
    h = headerp

    ##initializing   data frame with header and units
    if(data[1][3].isdigit()):
        data=data[1:]
    else:
        data=data[2:]

    ##parsing the rest of data into properly formatted lists
    datal= len(data)
    i=0
    while (i < datal):
        datap= data[i]
        datap=datap[:-1]
        datap=datap.split(' ')
        datap= list(filter(None, datap))
        data[i]= datap
        i= i+1
    
    df= pd.DataFrame(data, columns=h)
    df = df.reset_index(drop=True)

    #fix name discontinuity between years
    for i in range(len(headerp)):
        if(headerp[i]=='BAR'):
            headerp[i]='PRES'
            df = df.rename(index=str, columns={'BAR':'PRES'})
        if(headerp[i]=='WD'):
            headerp[i]='WDIR'
            df = df.rename(index=str, columns={'WD':'WDIR'})
        if(headerp[i]=='YY'):
            headerp[i]='YYYY'
            df = df.rename(index=str, columns={'YY':'YYYY'})
        if(headerp[i]=='#YY'):
            headerp[i]='YYYY'
            df = df.rename(index=str, columns={'#YY':'YYYY'})
        if(headerp[i]=='PTDY'):
            del headerp[i]
            df = df.drop(['PTDY'], axis=1)
            break
    
    
    #################################################################
    # 2. CLEANING AND CONVERTING DATA FRAME
   #################################################################

    #creating a datetime column
    df['datetime']= np.nan

    #converting all strings in data frame into ints of floats
    df = df.apply(pd.to_numeric, errors='coerce', downcast='float')
    df['YYYY'] = df['YYYY'].astype(int)
    df['MM'] = df['MM'].astype(int)
    df['DD'] = df['DD'].astype(int)
    df['hh'] = df['hh'].astype(int)
    l = range(len(df.index.values))
    li = list(df.index.values)

    for ind in l:
        #translate 2 digit years into four digit years
        year= df.iat[ind, 0]
        if(year< 60):
            year= year +2000
        elif(year< 100):
            year= year+1900

        #create datetime
        currdatetime= datetime.datetime(year, df.iat[ind, 1], df.iat[ind, 2], df.iat[ind, 3], 0, 0)
        df.at[li[ind], 'datetime']= currdatetime

    #removing duplicate date times
    df.drop_duplicates(subset= 'datetime', keep= 'last', inplace= True)


    #re indexing df by datetime
    df.index= df['datetime']
    del df['datetime']

    namedict= { 'YYYY': ['year', 'years', 1111],
                'MM': ['month', 'months', np.nan],
                'DD': ['day', 'days', np.nan],
                'hh': ['hour', 'hours', np.nan],
                'mm': [ 'minuet', 'minuets', np.nan],
                'WDIR': ['Wind Direction', 'degrees "T"', 999],
                'WSPD': ['Wind Speed', 'knots', 99.0],
                'GST': ['Wind Gust', 'm/s', 99.0],
                'WVHT': ['Wave Height', 'm', 99.00],
                'DPD': ['Dominant Wave Period', 'sec', 99.00],
                'APD': ['Average Wave Period', 'sec', 99.00],
                'MWD': ['Mean wave Direction', 'degrees', 999],
                'PRES': ['Air Pressure', 'hPa', 9999.0],
                'ATMP': ['Air Temperature', 'degC', 999.0],
                'WTMP': ['Water Temperature', 'degC', 999.0],
                'DEWP': ['Dew Point', 'degC', 999.0],
                'VIS': ['Visibility', 'nmi', 99.0],
                'TIDE': ['Tide', 'ft', 99.00]}


    ##adding appropriate Nan values to replace dummy values in time series
    for c in range(len(headerp)):
        for ind in list(df.index.values):
            if(df.iat[df.index.get_loc(ind), c] ==
                    namedict[headerp[c]][2]):
                df.at[ind, headerp[c]]= np.nan

    #create hourly time series with no gaps
    df = cleanDataframe( df)

    #slice data frame to begin an end on day intervals
    df= cuttimeseries( df)

    #drop extra datetime info columns now that information is stored in index
    df= removeExtraDateTime( df)

    #ipdb.set_trace()
    #convert WSPD from m/s to knots/s 
    df= convert_MS_to_Knots( df)
    #ipdb.set_trace()

    #create 3 hour mean time series
    ##use every third column when accessing means
    df= append_3H_Mean( 'ATMP', df)
    df= append_3H_Mean('WTMP', df)
    df= append_3H_Mean('PRES', df)
    df= append_3H_Mean('GST', df)
    df= append_3H_Mean('WSPD', df)
    df=  append_3H_Mean('WDIR', df)
    if 'TIDE' in headerp:
        df= append_3H_Mean('TIDE', df)
    else:
        df["TIDE"] = np.nan
    df= append_3D_Mean('WSPD', df)
    df= append_30D_Mean('WTMP', df)
    #################################################################
    # 3. PUTTING DATA FRAME INTO JSON FILE
    #################################################################
    ##Creating json file
    jsondf= df.to_json(orient='split')
    with open(config.data+'/data/'+filename+'.json', 'w') as f:
        f.write(jsondf)

#TO READ JSON string file
#>>import pandas as pd
#>>import json
#>>jsonstring = open("filename.json", 'r').read()
#>>df= pd.read_json(jsonstring, orient='split')
