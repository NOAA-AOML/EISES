import os
import json
import re

import configParameters as config

def get_len( listobj):
    if listobj is None:
        return str(0)
    else:
        return str(len(listobj))

def alert_display( stationdict):
    #types of rules fired: mcb_AM, mcb_w3A, mcb_A
    stations= list(stationdict.keys())
    years= list(stationdict[stations[0]].keys())
    ruleTypes= list( stationdict[stations[0]][years[0]].keys())
    for s in stations:
        for y in years:
            print("["+s+"]"+"["+str(y)+"]\t"+ruleTypes[0]+":\t "+get_len(stationdict[s][y][ruleTypes[0]]))
            print("\t\t"+ ruleTypes[1]+": "+get_len(stationdict[s][y][ruleTypes[1]]))
            print("\t\t"+ ruleTypes[2]+":\t "+get_len(stationdict[s][y][ruleTypes[2]]))
            print("\t\t"+ ruleTypes[3]+":\t "+get_len(stationdict[s][y][ruleTypes[3]]))

def import_alert_dict(alertDict, years, station):
    for y in years:
        if os.path.isfile(config.data+"/alerts/"+station+"/"+str(y)+".json"):
            with open(config.data+"/alerts/"+station+"/"+str(y)+".json") as alertfile:
                dictImport= json.load( alertfile)
            alertDict.update( dictImport)
        else:
            print("\tThe file \""+config.data+"/alerts/"+station+"/"+str(y)+".json\" does not exist\n")

def alert_load( stations, startY, endY):
    alertDict= {}
    years= range(startY, endY)

    if type(stations)== list:
        for s in stations:
            import_alert_dict( alertDict, years, s)
    elif re.match("^[a-z]{3}f1$", stations):
        import_alert_dict( alertDict, years, stations)

    alertkeys= list(alertDict.keys())
    stationdict= dict.fromkeys(stations)
    for s in stations:
        stationdict[s]= dict.fromkeys(years)
        for y in years:
            stationdict[s][y]= dict.fromkeys(["mcb_AM", "mcb_w3A", "mcb_A", "mcb_wA"])

    for k in alertkeys:
        keystring= str(k)
        keyyear= int(keystring[6:10])
        station= keystring[10:15]
        ruletype= re.search('[\S]{15}(.+?)#(.+?)', keystring).group(1)
        iteration= int(re.search('[\S]{15}(.+?)#(.+?)', keystring).group(2))
        if stationdict[station][keyyear][ruletype] is None:
            stationdict[station][keyyear][ruletype]=[alertDict[k]]
        else:
            stationdict[station][keyyear][ruletype].append(alertDict[k])

    return stationdict

def main( stations, startY, endY):
    stationdict= alert_load(stations, startY, endY)
    alert_display( stationdict)
    return stationdict
