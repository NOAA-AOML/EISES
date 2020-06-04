#!/usr/bin/env python3

###fffunctions is a script containg helper functions used in ffmcb.py

__author__= 'Madison Soden'
__date__= "Tue Aug 14, 2018  12:24PM"
__license__= 'NA?'
__email__= 'madison.soden@gmail.com'
__status__= 'Production'

import fact

 # 'night-hours'.-.'nite'.-.0000.to.0900$
 # 'dawn-morning'.-.'dayb'.-.0900.to.1500$
 # 'afternoon'.-.'aftn'.-.1800.to.2400$
 # 'daylight-hours'.-.'dayl'.-.0900.to.2400$
 # 'all-day'.-.'all'.-.0300.to.0300$

def name_to_fact( fact_type):
    fact_dic= {
            'windsp': fact.windsp,
            'windsp3day': fact.windsp3day,
            'seandbc': fact.seandbc,
            'tide1m': fact.tide1m,
            'seandbdM': fact.seandbcM
            }
    return fact_dic.get( fact_type, 'unregistered fact type')


def rm_redundant_facts( factlist):
    newfactlist= []
    for i in range(len(factlist)):
        singlefact= factlist.pop(i)
        for j in range(len(factlist)):
            if  (type(singlefact) == type(factlist[j]))and\
                (singlefact[fuzzyI] == factlist[j][fuzzyI])and\
                (singlefact[fuzzyTod] == factlist[j][fuzzyTod]):
                    factlist.pop(j)
        newfactlist.append(singlefact)

def make_nite( factlist):
    nitelist= []
    for fact_it in factlist:
        if (fact_it['fuzzyTod'] == 'even') or (fact_it['fuzzyTod'] == 'midn') or (fact_it['fuzzyTod'] == 'pdaw'):
            factlist.remove(fact_it)
            nitelist.append(fact_it)
    if(len(nitelist)==3):
        if(nitelist[0]['fuzzyI']==nitelist[1]['fuzzyI'])and(nitelist[1]['fuzzyI']==nitelist[2]['fuzzyI']):
            nine_hour_average_intensity= round((nitelist[0]['I']+nitelist[1]['I']+nitelist[2]['I'])/3, 3)
            factlist.append( name_to_fact(nitelist[0]['fact_type'])\
                                        (fuzzyI= nitelist[0]['fuzzyI'],\
                                        fuzzyTod= 'nite',\
                                        date= nitelist[0]['date'],\
                                        locus= nitelist[0]['locus'],\
                                        I= nine_hour_average_intensity,\
                                        fact_type= nitelist[0]['fact_type']))
            return factlist
    return factlist+nitelist

def make_dayb( factlist):
    dayblist= []
    for fact_it in factlist:
        if (fact_it['fuzzyTod'] == 'dawn') or (fact_it['fuzzyTod'] == 'morn'):
            factlist.remove(fact_it)
            dayblist.append(fact_it)
    if(len(dayblist)==2):
        if(dayblist[0]['fuzzyI']==dayblist[1]['fuzzyI']):
            six_hour_average_intensity= round((dayblist[0]['I']+dayblist[1]['I'])/2, 3)
            factlist.append( name_to_fact(dayblist[0]['fact_type'])\
                                        (fuzzyI= dayblist[0]['fuzzyI'],\
                                        fuzzyTod= 'dayb',\
                                        date= dayblist[0]['date'],\
                                        locus= dayblist[0]['locus'],\
                                        I= six_hour_average_intensity,\
                                        fact_type= dayblist[0]['fact_type']))
            return factlist
    return factlist+dayblist


def make_aftn( factlist):
    aftnlist= []
    for fact_it in factlist:
        if (fact_it['fuzzyTod'] == 'psun') or (fact_it['fuzzyTod'] == 'suns'):
            factlist.remove(fact_it)
            aftnlist.append(fact_it)
    if(len(aftnlist)==2):
        if(aftnlist[0]['fuzzyI']==aftnlist[1]['fuzzyI']):
            six_hour_average_intensity= round((aftnlist[0]['I']+aftnlist[1]['I'])/2, 3)
            factlist.append( name_to_fact(aftnlist[0]['fact_type'])\
                                        (fuzzyI= aftnlist[0]['fuzzyI'],\
                                        fuzzyTod= 'aftn',\
                                        date= aftnlist[0]['date'],\
                                        locus= aftnlist[0]['locus'],\
                                        I= six_hour_average_intensity,\
                                        fact_type= aftnlist[0]['fact_type']))
            return factlist
    return factlist+aftnlist


def make_dayl( factlist):
    dayllist= []
    for fact_it in factlist:
        if ((fact_it['fuzzyTod'] == 'dawn') or (fact_it['fuzzyTod'] == 'morn') or (fact_it['fuzzyTod'] == 'midd') or (fact_it['fuzzyTod'] == 'psun') or (fact_it['fuzzyTod'] == 'suns')):
            factlist.remove(fact_it)
            dayllist.append(fact_it)
    if(len(dayllist)==5):
        if(dayllist[0]['fuzzyI']==dayllist[1]['fuzzyI'])and(dayllist[1]['fuzzyI']==dayllist[2]['fuzzyI'])and(dayllist[2]['fuzzyI']==dayllist[3]['fuzzyI'])and(dayllist[3]['fuzzyI']==dayllist[4]['fuzzyI']):
            fifteen_hour_average_intensity= round((dayllist[0]['I']+dayllist[1]['I']+dayllist[2]['I']+dayllist[3]['I']+dayllist[4]['I'])/5, 3)
            factlist.append( name_to_fact(dayllist[0]['fact_type'])\
                                        (fuzzyI= dayllist[0]['fuzzyI'],\
                                        fuzzyTod= 'dayl',\
                                        date= dayllist[0]['date'],\
                                        locus= dayllist[0]['locus'],\
                                        I= fifteen_hour_average_intensity,\
                                        fact_type= dayllist[0]['fact_type']))
            return factlist
    return factlist+dayllist


def make_all( factlist):
    if(len(factlist)==8):
        if  (factlist[0]['fuzzyI']==factlist[1]['fuzzyI']) and\
            (factlist[1]['fuzzyI']==factlist[2]['fuzzyI']) and\
            (factlist[2]['fuzzyI']==factlist[3]['fuzzyI']) and\
            (factlist[3]['fuzzyI']==factlist[4]['fuzzyI']) and\
            (factlist[4]['fuzzyI']==factlist[5]['fuzzyI']) and\
            (factlist[5]['fuzzyI']==factlist[6]['fuzzyI']) and\
            (factlist[6]['fuzzyI']==factlist[7]['fuzzyI']):
            twentyfour_hour_average_intensity= round((factlist[0]['I']+factlist[1]['I']+factlist[2]['I']+factlist[3]['I']+factlist[4]['I']+factlist[5]['I']+factlist[6]['I']+factlist[7]['I'])/8, 3)
            factHolder = []
            factHolder.append( name_to_fact(factlist[1]['fact_type'])\
                                            (fuzzyI= factlist[0]['fuzzyI'],\
                                            fuzzyTod= 'all',\
                                            date= factlist[0]['date'],\
                                            locus= factlist[0]['locus'],\
                                            I= twentyfour_hour_average_intensity,\
                                            fact_type= factlist[0]['fact_type']))
            return factHolder
    return factlist


def make_super_periods( factlist):
    factlist= make_all(factlist)
    factlist= make_dayl(factlist)
    factlist= make_aftn(factlist)
    factlist= make_dayb(factlist)
    factlist= make_nite(factlist)
    return factlist
