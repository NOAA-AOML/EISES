#!/usr/bin/env python3

###g2_to_csv.py is a parse to convert a g2 fact file in .bb format to a csv fact file

__author__= "Madison.Soden"
__date__= "Thu Jul 19, 2018  03:20PM"
__license__= "NA?"
__email__= "madison.soden@gmail.com"
__status__= "Production"

import datetime as dt
import pickle as p
import csv

###SAMPLE FACT
#(mlrf1 sat-chlor_a 0 23 low all-day of day 169 year 2017)

class MyException(Exception):
    pass

def locusID(location):
    locusDict = {\
            'mlrf1': "MLRF1",\
            'foo': "FOO",\
            }
    return locusDict[location]

def nameID(factname):
    nameDict= { 
            'windsp': 'windsp',
            'winddir': 'winddr',
            'seandbc': 'seandbc',
            'windsp-3day': 'windsp3day',
            'windsp-7day': 'windsp7day',
            'windgu': 'windgu',
            'surfbarom': 'surfb',
            'surfcur-umin': 'surfc',
            'seandbc-monthly': 'seandbcM',
            'airt': 'airt',
            'windsd-7day': 'windsd7',
            'spawning-seatemp': 'spawt',
            'photo-accum': 'paccum',
            'airt-variability': 'airtV',
            'barom': 'barom',
            'bleaching-seatemp': 'bleaST',
            'ekmandir-7day': 'ekmD7day',
            'mwsst': 'sst',
            'sat-chlor_a': 'satCA',
            'seandbc-1d': 'seandbcD',
            'seandbc-variability': 'seandbcV',
            }
    return nameDict[factname]

def SRIID(SRI):
    return SRI

def fuzzyIID(fuzzyI):
    fuzzyIDict =  {
            'average': 'average',
            'very-low': 'vLow',
            'somewhat-low': 'sLow',
            'low': 'Low',
            'somewhat-high': 'sHigh',
            'high': 'High',
            'unbelievably-low': 'uLow',
            'drastic-low': 'dLow',
            'very-high': 'vHigh',
            'drastic-high': 'dHigh',
            'wsw-w': 'wsw-w',
            'nw-n': 'nw-n',
            'ssw-wsw': 'ssw-wsw',
            'w-nw': 'w-nw',
            'n-ne': 'n-ne',
            'ne-ene': 'ne-ene',
            'ene-ese': 'ene-ese',
            'ese-sse': 'ese-sse',
            'sse-ssw': 'sse-ssw',
            'conducive': 'cond',
            'too-low': 'uLow',
            'too-high': 'uHigh',
            'offshore': 'offshore',
            'onshore': 'onshore',
            'downshore': 'downshore',
            'upshore': 'upshore',
            }
    return fuzzyIDict[fuzzyI]

def fuzzyTID(fuzzyT):
    fuzzyTDict = {
            'dawn': 'dawn',
            'pre-dawn': 'pdaw',
            'morning': 'morn',
            'mid-day': 'midd',
            'pre-sunset': 'psun',
            'sunset': 'suns',
            'all-day': 'all',
            'midnight': 'midn',
            'evening': 'even',
            'dawn': 'dawn',
            'night-hours': 'nite',
            'dawn-morning': 'dayb',
            'afternoon': 'aftn',
            'daylight-hours': 'dayl',
            }
    return fuzzyTDict[fuzzyT]

def dateID(day, year):
    factdate = dt.datetime(int(year), 1, 1, 0, 0) + dt.timedelta(days = int(day))
    return factdate

def parse(filename= "./test_suite/MLRF_G2FACTS.bb", output = 'CSV'):
    factlines = [x.rstrip('\n') for x in open(filename)]
    factlist = []
    #initialize array of lists to store parsed facts
    while factlines:
        factstring = factlines.pop(0)
        factstring = factstring[1:-1]
        location, name, SRI, fuzzyI, fuzzyT, t0, t1, day, t2, year = factstring.split(' ')
        
        #parse location
        location = locusID(location)
        print("Parsing location ...", location)
        
        #parse fact name
        name = nameID(name)
        print("Parsing Fact name ...", name)
        
        #parse SRI
        SRI = SRIID(SRI)
        print("Parsing SRI ...", SRI)
        
        #parse fuzzyI
        fuzzyI = fuzzyIID(fuzzyI)
        print("Parsing fuzzyI ...", fuzzyI)
        
        #parse fuzzyT
        fuzzyT = fuzzyTID(fuzzyT)
        print("Parsing fuzzyT ...", fuzzyT)
        
        #parse date
        factdate = dateID(day, year)
        print("Parsing date", factdate)
        
        #add everything as list into array
        facttuple = (name, fuzzyI, fuzzyT, factdate, location)
        factlist.append(facttuple)
        print("Adding into array ...")

    if((output=='pickle')or(output=='PICKLE')or(output=='Pickle')):
        #make a pickle file
        print("Making a pickle file ...")
        p.dump( factlist, open(filename[:-3]+'.p', "wb"))

    elif ((output=='CSV')or(output=='csv')or(output=='CSV')or(output ==\
            '.csv')or(output=='.CSV')):
        #make a csv file
        print("Making a csv file...")
        f = open(filename[:-3]+'.csv', 'w', newline='')
        while factlist:
            factline =\
            factlist[0][0]+","+factlist[0][1]+","+factlist[0][2]+","+factlist[0][3].strftime('%m%d%Y')+","+factlist[0][4]+"\n"
            f.write(factline)
            factlist.pop(0)
        f.close()

    else :
        raise MyException("Not a supported output type")

def divide(filename= "./test_suite/MLRF_G2FACTS.csv", output = "CSV"):
    datedict = {}
    with open(filename, newline='') as f:
        factdata = csv.reader(f, delimiter = ',', quotechar='|')
        for row in factdata:
            if row[3] in datedict:
                datedict[row[]].append(row)
            else:
                datedict[row[3]] = []
                datedict[row[3]].append(row)
    for key in list(datedict):
        with open("./test_suite/fact_CSVs/"+key+'.csv', 'w+', newline='') as f1:
            writer = csv.writer(f1, delimiter= ',', quotechar='|',
                    quoting=csv.QUOTE_MINIMAL)
            for row in datedict[key]:
                writer.writerow(row)


