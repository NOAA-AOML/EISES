#!/usr/bin/env python3

### ffmcb.py is a prototype fact factory implementation, meant to help provide an
#       example for a future, inherited fact factory implementation that would apply to
#       any ecoforecast. Not just MCB for MLRF1

__author__= "Madison.Soden" 
__date__= "Wed May 08, 2019  04:37PM"
__license__= "NA?"
__email__= "madison.soden@gmail.com"
__status__= "Production"

import os
import os.path
import pandas as pd
import pyknow as pk
import numpy as np
import json
import csv
import datetime

import configParameters as config
import fact
import fffunctions as fff
import fuzzy_ranges_values as frv

def data2function( index):
#dictionary function to return a call to fact type specific generating functions given a fact data frame abbreviation
    dataDict= {
            'WDIR': 'NA',
            'WSPD': 'NA',
            'GST': 'NA',
            'WVHT': 'NA',
            'DPD': 'NA',
            'APD': 'NA',
            'MWD': 'NA',
            'PRES': 'NA',
            'ATMP': 'NA',
            'WTMP': 'NA',
            'DEWP': 'NA',
            'VIS': 'NA',
            'TIDE': 'NA',
            'ATMP_three_hour_mean': 'NA',
            'WTMP_three_hour_mean': seandbcGen,
            'PRES_three_hour_mean': 'NA',
            'GST_three_hour_mean': 'NA',
            'WSPD_three_hour_mean': windspGen,
            'WDIR_three_hour_mean': 'NA',
            'TIDE_three_hour_mean': 'NA', #tide1mGen,
            'WSPD_three_day_mean': windsp3dayGen,
            'WTMP_30day_rolling_mean': seandbcMGen}
    return dataDict. get( index, 'unregistered data time series')

def data2fact( index):
    #return system fact type  name given a fact type data frame abbreviation
    dataDict= {
            'WDIR': 'NA',
            'WSPD': 'NA',
            'GST': 'NA',
            'WVHT': 'NA',
            'DPD': 'NA',
            'APD': 'NA',
            'MWD': 'NA',
            'PRES': 'NA',
            'ATMP': 'NA',
            'WTMP': 'NA',
            'DEWP': 'NA',
            'VIS': 'NA',
            'TIDE': 'NA',
            'ATMP_three_hour_mean': 'NA',
            'WTMP_three_hour_mean': 'seandbc',
            'PRES_three_hour_mean': 'NA',
            'GST_three_hour_mean': 'NA',
            'WSPD_three_hour_mean': 'windsp',
            'WDIR_three_hour_mean': 'NA',
            'TIDE_three_hour_mean': 'NA', #'tide1m',
            'WSPD_three_day_mean': 'windsp3day',
            'WTMP_30day_rolling_mean': 'seandbcM'}
    return dataDict. get( index, 'unregistered data time series')

class MyException(Exception):
    pass

def factfactory(  filen, stationn):
    ##TO READ JSON string file
    #check that user requested filename exists in file archive
    if os.path.exists(config.data+'/data/'+filen+".json"):
        #read json file into a pandas data frame
        jsonstring= open(config.data+'/data/'+filen+".json", 'r').read()
        df= pd.read_json(jsonstring, orient='split')
        #check that sst exists in yearly data before continuing to run.
        numNA= df["WTMP"].isna().sum()
        hourlyYearLen= config.insitu_samplingRate #Hourly len(df.index)
        if( numNA> hourlyYearLen*0.5):
            print("\tThere is not enough sst data for station " + stationn+ " in "+ filen[-4:]+ " for an accurate analysis.")
            return True
        else:
            factorySort( df, filen, stationn)
    else:
        #if requested file does not exist alert the user
        raise MyException(' '+filen+' data input file does not exist')
        return False

def factorySort( df, filen, stationn):
#partition data frame into series containing one fact type and then begin fact creation/storage process for each fact type separately
    factlist= df.columns.values
    for datatype in factlist:
        if data2fact(datatype) != 'NA':
            factory( df[datatype], datatype, filen, stationn)

def factory( datadf, datatype, filen, stationn):
    ##if there is no specific range list for [locus][facttype] exit factory function
    if not frv.ranges[stationn][data2fact(datatype)]:
        #alert user of error
        assert MyException( 'datatype locus combination: '\
            +datatype+'/'+stationn+' does not have specified range file.\
            Cannot factize.')
        return False
    if datadf.isnull().all():
        date= datadf.index.values[0]
        date=pd.Timestamp(date)
        date=pd.to_datetime(date)
        date=date.strftime('%m_%d_%Y')
        assert MyException( 'Data does not exist or is not recorded for: '\
                +datatype + ', ' + stationn + ', ' + date +'/n')

    ##else continue to factize datadf
    #find initial date for entire fact file and convert into string of form MM_DD_YYYY
    first= datadf.index.values[0]
    first= pd.Timestamp(first)
    first= pd.to_datetime(first)
    first= first.strftime('%m_%d_%Y')
    currdate= first
    #initialize empty fact list
    factlist= []

    #iterate through all datetime indexes in series datadf
    for index in datadf.index.values:
        #get int representation of index location
        indexloc= datadf.index.get_loc(index)
        #convert index of type np.datetime to type datetime.datetime
        i=pd.Timestamp(index)
        i=pd.to_datetime(i)
        #get  int representation of fact intensity corresponding to current index value
        intensity= datadf.iat[ indexloc]
        #check if current date is the same as previous date
        if(i.strftime('%m_%d_%Y')!=currdate): #if not
            #create super periods for factlist
            factlist= fff.make_super_periods( factlist)
            #store list for previous date
            factoryStore(factlist, data2fact(datatype), filen, currdate)
            #update currdate tracker
            currdate= i.strftime('%m_%d_%Y')
            #clear factlist for new day
            factlist= []
        #check that fact intensity is recorded for current date time (i.e not missing data)
        if not np.isnan( intensity):
            # if data is recorded create corresponding fact and add to current days fact list
            factlist.append( data2function(datatype)(intensity, i, stationn))


def factoryStore( factlist, factname, filen, date):
    year= filen[-4:]
    #create directory for corresponding date if one does not already exist
    if not os.path.exists(os.path.dirname(config.data+'/facts/'+filen[:5]+'/'+year+'/'+date+'/'+factname+'.json')):
        os.makedirs(os.path.dirname(config.data+'/facts/'+filen[:5]+'/'+year+'/'+date+'/'+factname+'.json'))
    #save list of specific date & fact type as json file
    with open(config.data+'/facts/'+filen[:5]+'/'+year+'/'+date+'/'+factname+'.json', 'w') as fout:
        json.dump( factlist, fout)

def fuzzyTod( t):
    #round to nearest hour
    t= t.hour +t.minute//30
    #get lists of all fuzzy lower bounds(xcoor) and corresponding positions in list (ycoor) to use in interpolate function
    xcoor= frv.times['mlrf1']['standard_time'][0]
    ycoor= range(len( xcoor))
    #predict position of time intensity relative to fuzzy lower bounds
    y= np.floor( np.interp( t, xcoor, ycoor))
    #look up corresponding fuzzyTod string value
    fuzzyTod=frv.standardtime[ int(y)]
    return fuzzyTod

def fuzzyI( intensity, stationn, factn): 
    #get lists of all fuzzy lower bounds(xcoor) and corresponding positions in list (ycoor) to use in interpolate function
    xcoor= frv.ranges[ stationn][ factn][0]
    ycoor= range(len( xcoor))
    #predict position of time intensity relative to fuzzy lower bounds
    y= np.floor( np.interp( intensity, xcoor, ycoor, left=-99, right= 99))
    y= int( y)
    #look up corresponding fuzzyI string value
    if(y== -99):
        return 'uLow'
    elif(y== 99):
        return 'uHigh'
    else: 
        return frv.ranges[ stationn][ factn][ 1][ y]

def windspGen( intensity, dt, stationn):
    #generate wind speed type fact
    ##calculating fuzzyI
    fI= fuzzyI( intensity, stationn, 'windsp')
    ## calculating fuzzyTod
    fTod= fuzzyTod( dt.time())
    return fact.windsp(fuzzyI=fI, fuzzyTod= fTod, date= dt.strftime('%m_%d_%Y'),
            locus= stationn, I= intensity, fact_type= 'windsp')

def seandbcMGen( intensity, dt, stationn):
    #generate sea temperature (NDBC) type fact
    ##calculating fuzzyI
    fI= fuzzyI( intensity, stationn, 'seandbcM')
    ## calculating fuzzyTod
    fTod= fuzzyTod( dt.time())
    return fact.seandbc(fuzzyI=fI, fuzzyTod= fTod, date= dt.strftime('%m_%d_%Y'),
            locus= stationn, I= intensity, fact_type= 'seandbcM')

def seandbcGen( intensity, dt, stationn):
    #generate sea temperature (NDBC) type fact
    ##calculating fuzzyI
    fI= fuzzyI( intensity, stationn, 'seandbc')
    ## calculating fuzzyTod
    fTod= fuzzyTod( dt.time())
    return fact.seandbc(fuzzyI=fI, fuzzyTod= fTod, date= dt.strftime('%m_%d_%Y'),
            locus= stationn, I= intensity, fact_type= 'seandbc')

def tide1mGen( intensity, dt, stationn):
    #generate sea temperature (NDBC) type fact
    ##calculating fuzzyI
    fI= fuzzyI( intensity, stationn, 'tide1m')
    ## calculating fuzzyTod
    fTod= fuzzyTod( dt.time())
    return fact.seandbc(fuzzyI=fI, fuzzyTod= fTod, date= dt.strftime('%m_%d_%Y'),
            locus= stationn, I= intensity, fact_type= 'tide1m')

def windsp3dayGen( intensity, dt, stationn):
    #generate sea temperature (NDBC) type fact
    ##calculating fuzzyI
    fI= fuzzyI( intensity, stationn, 'windsp3day')
    ## calculating fuzzyTod
    fTod= fuzzyTod( dt.time())
    return fact.seandbc(fuzzyI=fI, fuzzyTod= fTod, date= dt.strftime('%m_%d_%Y'),
            locus= stationn, I= intensity, fact_type= 'windsp3day')
