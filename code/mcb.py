### main function to call knowledge engine based ecoforecast pipeline

__author__= "Madison.Soden"
__date__= "Wed May 15, 2019  05:57PM"
__license__= "NA?"
__email__= "madison.soden@gmail.com"
__status__= "Production"

import os
import os.path
import pyknow as pk
import numpy as np
import json
import glob
import csv
import datetime
import re

import configParameters as config
from  parsers import insitu_to_json
import fact
import ffmcb as ff
import kemcb as ke


"""ADD Functionality for multiple years to be specified as standalone dates or
as multiple years EG:
    mcb.main("mlrf1", ["1_02_1998", "02_02_1997"])
    or
    mcb.main("mlrf1", ["1998", "1999"])
    """

def check_timeframe( lookUpDate):
    ## identifying which function to call to run knowledge engine
    ## and what year knowledge engine is being run for
    if isinstance(lookUpDate, list):
        if lookUpDate and all(isinstance(s, str) for s in lookUpDate):
            if all(re.match("^(0[1-9]|1[0-2])_(0|1|2|3)[0-9]_(19(8|9)[0-9]|20(0|1)[0-9])$", s) for s in lookUpDate):
                return lookUpDate[0][-4:], "dates" #call date iterator
            else:
                 raise ValueError( "3rd function argument must be a list of strings in  the format MM_DD_YYYY. For years between 1987-2018\n")
        else:
            raise ValueError( "3rd function argument must be a none empty list of strings. Of the format MM_DD_YYYY for years 1987-2018)\n")
    elif isinstance(lookUpDate, str):
        if re.match("^(19|20)(8|9|0|1)[0-9]$", lookUpDate):
            return lookUpDate, "year" #call year creator
        else:
            raise ValueError("3rd function argument must be a string of the format YYYY for years 1987-2018.\n")
    else:
        raise ValueError("for 3rd function argument please input list of strings MM_DD_YYYY for 3rd function argument. Alternatively, input a string YYYY to run a coral bleaching forecast on the entire year\n")

def check_file_path( stationName, year):
    if not(os.path.isdir( os.path.join(config.data,"facts", stationName))):
        print("\t"+config.data+"/facts/"+stationName+" is not an existing directory")
        os.makedirs(os.path.join(config.data,"facts", stationName))
        print("\t"+config.data+"/facts/"+stationName+" directory created.")
    if not(os.path.isdir( os.path.join(config.data,"facts", stationName, year))):
        print("\t"+config.data+"/facts/"+stationName+"/"+year+" is not an existing directory")
        os.makedirs(os.path.join(config.data,"facts", stationName, year))
        print("\t"+config.data+"/facts/"+stationName+"/"+year+" directory created.")

def create_facts( stationName, year):
    factFileName= stationName+"h"+year
    insitu_to_json.main( factFileName) #parse insitu txt file and save as json file
    return ff.factfactory( factFileName, stationName) #call fact factory to generate facts

def main( stationName, lookUpDate, run_ff=False):

    print("["+stationName+"][XXXX]Checking for available data files.")
    year, engine_case= check_timeframe(lookUpDate)
    check_file_path(stationName, year)
    print("["+stationName+"]["+year+"]Data location confirmed.")

    NANsst= False

    print("["+stationName+"]["+year+"]Running Fact Factory.")
    if run_ff: #run fact factory if asked to
        NANsst= create_facts( stationName, year)
    else:  #checking to see if required fact data files exist
        glob_string= config.data+"/facts/"+stationName+"/"+year+"/*/*.json"
        fact_files_list= glob.glob(glob_string)
        if not(fact_files_list):
            #if the directory supposed to be containing fact files is empty rerun parser and ff
            NANsst= create_facts( stationName, year)
    if(NANsst):
        print("["+stationName+"]["+year+"]Not enough SST data too run Knowledge Engine.\n\n")
        return

    print("["+stationName+"]["+year+"]Facts Created.")

    print("["+stationName+"]["+year+"]Loading Facts.")
    if (engine_case == 'year'):
        factdatefiles = [
                f for f in os.listdir(config.data+"/facts/"+stationName+'/'+year)
                if os.path.isdir(os.path.join(config.data, "facts", stationName, year, f))]
        #if (len(factdatefiles)!=364) and (len(factdatefiles)!=365):
        #    filepath= os.path.join(config.data,"facts", stationName, year)
        #    print("Please rerun program with 3rd function argument as 'True' to regenerate fact files.\n")
        #    raise FileNotFoundError("There are too many or to few date directories in ", filepath)
    elif (engine_case == 'dates'):
        factdatefiles = lookUpDate

    print("["+stationName+"]["+year+"]Initializing SRI and Alerts.")
    alertDict= {}
    SRI = {}
    dateI = "01_01_"+year
    yearF = int(year) +1
    dateF = "01_01_"+str(yearF)
    dateStart = datetime.datetime.strptime(dateI, '%m_%d_%Y')
    dateFin = datetime.datetime.strptime(dateF, '%m_%d_%Y')
    step = datetime.timedelta(days=1)
    while dateStart < dateFin:
        SRI[dateStart.strftime('%m_%d_%Y')] = np.nan
        dateStart += step

    factdatefiles= sorted(factdatefiles)


    print("["+stationName+"]["+year+"]Running Knowledge Engine.")
    for date_iterator in factdatefiles:
        #put fact files into single fact list
        factlist= []
        try:
            with open(config.data+"/facts/"+stationName+'/'+year+'/'+date_iterator+"/tide1m.json", 'r') as fin:
                factlist= factlist + json.load( fin, object_hook= fact.tide1m_decoder)
        except:
            pass #print('tide1m data does not exist for: '+ date_iterator)
        try:
            with open(config.data+"/facts/"+stationName+'/'+year+'/'+date_iterator+"/windsp3day.json", 'r') as fin:
                factlist= factlist + json.load( fin, object_hook= fact.windsp3day_decoder)
        except:
            pass #print('windsp3day data does not exist for: '+ date_iterator)
        try:
            with open(config.data+"/facts/"+stationName+'/'+year+'/'+date_iterator+"/seandbc.json", 'r') as fin:
                factlist= factlist + json.load( fin, object_hook= fact.seandbc_decoder)
        except:
            pass #print('seandbc data does not exist for: '+ date_iterator)
        try:
            with open(config.data+"/facts/"+stationName+'/'+year+'/'+date_iterator+"/seandbcM.json", 'r') as fin:
                factlist= factlist + json.load( fin, object_hook= fact.seandbcM_decoder)
        except:
            pass #print('seandbcM data does not exist for: '+ date_iterator)
        try:
            with open(config.data+"/facts/"+stationName+'/'+year+'/'+date_iterator+"/windsp.json", 'r') as fin:
                factlist= factlist + json.load( fin, object_hook= fact.windsp_decoder)
        except:
            pass #print('windsp data does not exist for: '+ date_iterator)

        #call knowledge engine to process analyze facts
        daySRI, dayMaxSRI, alertDictapp= ke.knowledge_engine( factlist,stationName)
        SRI[date_iterator]=  [daySRI, dayMaxSRI]
        alertDict.update( alertDictapp)
    print("["+stationName+"]["+year+"]Knowledge Engine Done.")

    print("["+stationName+"]["+year+"]Exporting SRI and Alert data.")
    #exporting SRI and alert data

    #checking file locations for sri and alert data exist. initializing them if
    ##they do not.
    if not os.path.exists(os.path.dirname(config.data+'/SRI/'+stationName+'/')):
        os.makedirs(os.path.dirname(config.data+'/SRI/'+stationName+'/'))
    if not os.path.exists(os.path.dirname(config.data+'/alerts/'+stationName+'/')):
        os.makedirs(os.path.dirname(config.data+'/alerts/'+stationName+'/'))

    #writing SRI list to csv file
    with open(config.data+'/SRI/'+stationName+"/"+year+'.csv', mode='w') as sri_file:
        sri_writer = csv.writer(sri_file, delimiter=',')
        for date_iterator in factdatefiles:
            sri_writer.writerow([date_iterator, SRI[date_iterator][0], SRI[date_iterator][1]])

    #writing alert dict to json file
    with open(config.data+'/alerts/'+stationName+"/"+year+'.json', mode='w') as alert_file:
        json.dump( alertDict, alert_file, indent=4)
    print("["+stationName+"]["+year+"]SRI and Alert Data exported.\n\n")
