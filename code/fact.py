#!/usr/bin/env python3

### main function to create facts


__author__= "Madison.Soden"
__date__= "Thu Sep 27, 2018  06:30PM"
__license__= "NA?"
__email__= "madison.soden@gmail.com"
__status__= "Production"

import pyknow as pk
import numpy as np

class airt( pk.Fact):
    pass

class barom( pk.Fact):
    pass

class seandbc( pk.Fact):
    pass

class winddir( pk.Fact):
    pass

class windgu( pk.Fact):
    pass

class windsp( pk.Fact):
    pass

class sst( pk.Fact):
    pass

class parsurf( pk.Fact):
    pass

class tide1m( pk.Fact):
    pass

class sea1m( pk.Fact):
    pass

class seandbcM( pk.Fact):
    pass

class windsp3day( pk.Fact):
    pass

class sea1mM( pk.Fact):
    pass

class curveB( pk.Fact):
    pass


def curveB_decoder( obj):
    return curveB(fuzzyI= obj['fuzzyI'], fuzzyTod= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'], I= np.round(obj['I'], 2), fact_type= obj['fact_type'])


def sea1mM_decoder( obj):
    return sea1mM(fuzzyI= obj['fuzzyI'], fuzzyTod= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'], I= np.round(obj['I'], 2), fact_type= obj['fact_type'])


def windsp3day_decoder( obj):
    return windsp3day(fuzzyI= obj['fuzzyI'], fuzzyTod= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'], I=np.round(obj['I'], 2), fact_type= obj['fact_type'])


def seandbcM_decoder( obj):
    return seandbcM(fuzzyI= obj['fuzzyI'], fuzzyTod= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'], I=np.round(obj['I'], 2), fact_type= obj['fact_type'])


def sea1m_decoder( obj):
    return sea1m(fuzzyI= obj['fuzzyI'], fuzzyTod= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'], I= np.round(obj['I'], 2), fact_type= obj['fact_type'])


def tide1m_decoder( obj):
    return tide1m(fuzzyI= obj['fuzzyI'], fuzzyTod= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'], I= np.round(obj['I'], 2), fact_type= obj['fact_type'])


def parsurf_decoder( obj):
    return parsurf(fuzzyI= obj['fuzzyI'], fuzzyTod= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'], I= np.round(obj['I'], 2), fact_type= obj['fact_type'])


def sst_decoder( obj):
    return sst(fuzzyI= obj['fuzzyI'], fuzzyTod= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'], I= np.round(obj['I'], 2), fact_type= obj['fact_type'])


def airt_decoder( obj):
    return airt(fuzzyI= obj['fuzzyI'], fuzzyTod= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'], I= np.round(obj['I'], 2), fact_type= obj['fact_type'])


def barom_decoder( obj):
    return barom(fuzzyI= obj['fuzzyI'], fuzzyTod= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'], I= np.round(obj['I'], 2), fact_type= obj['fact_type'])


def seandbc_decoder( obj):
    return seandbc(fuzzyI= obj['fuzzyI'], fuzzyTod= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'], I= np.round(obj['I'], 2), fact_type= obj['fact_type'])


def winddir_decoder( obj):
    return winddir(fuzzyI= obj['fuzzyI'], fuzzyTod= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'], I= np.round(obj['I'], 2), fact_type= obj['fact_type'])


def windgu_decoder( obj):
    return windgu(fuzzyI= obj['fuzzyI'], fuzzyTod= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'], I= np.round(obj['I'], 2), fact_type= obj['fact_type'])


def windsp_decoder( obj):
    return windsp(fuzzyI= obj['fuzzyI'], fuzzyTod= obj['fuzzyTod'], date= obj['date'], locus= obj['locus'], I= np.round(obj['I'], 2), fact_type= obj['fact_type'])


