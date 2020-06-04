#!/usr/bin/env python3

###mcb Ecoforecast prototype goal is to implement rules base from http://ecoforecast.coral.noaa.gov/index/0/MLRF1/model-detail&name=MASS-CORAL-BLEACHING and 'print' a forecast###

__author__= "Madison Soden"
__date__= "Wed May 15, 2019  05:58PM"
__license__= "NA?"
__email__= "madison.soden@gmail.com"
__status__= "Production"


############################################################################################???????????????????????????? rule 18 verse rule 20 supposed to call different facts???????????????????????

import pyknow as pk

import configParameters as config
import fact

###Fact Definition Documentation###
    #fact names are declared as 'parsurf', 'sst', 'windsp', 'tide1m',
    #'seandbc', 'sea1m', 'curveB', 'sea1mM', 'seandbcM', 'windsp3day'

    #fuzzyI is a string containing a fuzzy (i.e. proxy) values for sst
    #key = 'fuzzyI' / 0
    #fuzzy values can be 'uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh',
    # 'High', 'vHigh', 'dHigh', 'uHigh'
    #fuzzyTod is a string indicating a fuzzy time of day values for the-
    # time fuzzyI was recorded. Taken in eight 3 hour, then four 6 hour, then
    # two 12 hour , and one 24 hour time increments
    #key = 'fuzzyTod' and/or 1
    #fuzzy values can be
    # 'evening' - 'even' - 0000 to 0300
    # 'midnight' - 'midn' - 0300 to 0600
    # 'pre-dawn' - 'pdaw' - 0600 to 0900
    # 'dawn' - 'dawn' - 0900 to 1200
    # 'morning' - 'morn' - 1200 to 1500
    # 'mid-day' - 'midd' - 1500 to 1800
    # 'pre-sunset' - 'psun' - 1800 to 21:00
    # 'sunset' - 'suns' - 2100 to 2400
    # 'night-hours' - 'nite' - 0000 to 0900
    # 'dawn-morning' - 'dayb' - 0900 to 1500
    # 'afternoon' - 'aftn' - 1800 to 2400
    # 'daylight-hours' - 'dayl' - 0900 to 2400
    # 'all-day' - 'all' - 0300 to 0300

    #date is a string containing the date that fuzzyI was calculated on in DDMMYYYY
    #key = 'date' and/or 2

    #locus is an string containing the abbreviated geographic location that
    #fuzzyI, fuzzyTod and date apply to.
    #key = 'locus' and/or 3

###Helper functions###
def fact_display( fact):
    ruleDict = {
        'parsurf':      'p (parsurf)',
        'sst':          's (sst)',
        'windsp':       'w (windsp)',
        'tide1m':       't (tide1m)',
        'seandbc':      'a (seandbc)',
        'sea1m':        'e (sea1m)',
        'curveB':       'b (curveB)',
        'sea1mM':       'eM (sea1mM)',
        'seandbcM':     'aM (seandbcM)',
        'windsp3day':   'w3 (windsp3day)'}
    print('\t\t  '+ ruleDict.get( fact['fact_type']))
    print('\t\t\t  TOD:', fact['fuzzyTod'])
    print('\t\t\t  Intensity: '+fact['fuzzyI']+' ('+str(fact['I'])+')')
    print('\t\t\t  SRI:', sri_calc(fact))

def sri_calc( fact):
    i_multiplier= {
            'uLow': 0,
            'dLow': 2.5,
            'vLow': 2,
            'Low': 1,
            'sLow': 1,
            'average': 1,
            'sHigh': 1,
            'High': 1,
            'vHigh': 2,
            'dHigh': 2.5,
            'uHigh': 1,
            'n-ne': 1,
            'ne-ene': 1,
            'ene-ese': 1,
            'ese-sse': 1,
            'sse-ssw': 1,
            'ssw-wsw': 1,
            'wsw-w': 1,
            'w-nw': 1,
            'nw-n': 1,
            'onshore': 1,
            'downshore': 1,
            'offshore': 1,
            'upshore': 1,
            'toolow': 1,
            'conductive': 1,
            'toohigh': 1}
    t_multiplier = {
            'even': 3,
            'midn': 3,
            'pdaw': 3,
            'dawn': 3,
            'morn': 3,
            'midd': 3,
            'psun': 3,
            'suns': 3,
            'nite': 9,
            'dayb': 6,
            'aftn': 6,
            'dayl': 15,
            'all': 24}
    intensity_multiplier =  i_multiplier.get( fact['fuzzyI'])
    time_multiplier = t_multiplier.get( fact['fuzzyTod'])
    return intensity_multiplier*time_multiplier

def anyof(*values):
    return pk.P(lambda y: y in values)

class MCB( pk.KnowledgeEngine):

    def __init__(self, station):
        pk.KnowledgeEngine.__init__(self)
        self.station= station
        self.SRI= 0
        self.MaxSRI= 0
        self.alerts = {}

    def retract(self, idx_or_declared_fact):
        """
        Retracts a specific fact, using its index
        .. note::
            This updates the agenda
        """
        self.facts.retract(idx_or_declared_fact)
        #if not self.running:
        added, removed = self.get_activations()
        self.strategy.update_agenda(self.agenda, added, removed)

    def alert_add( self, ruleName, rule_des, sri, factList):
        date= factList[0]['date']
        i= 0
        alertName= date+self.station+ruleName+"#"+str(i)
        while True:
            if alertName in self.alerts.keys():
                i+=1
                alertName= alertName[:-1]+str(i)
            else:
                break

        self.alerts[alertName]= {}
        self.alerts[alertName]['rule_name']= ruleName
        self.alerts[alertName]['rule_description']= rule_des
        self.alerts[alertName]['SRI']= sri
        self.alerts[alertName]['fact_list']= factList


###OLD KE tools
#initial instruction output
    def display(self):
        print('\n',
            '----------------------------------------------------------------------\n',
            'To declare Knowledge Engine:\n',
            '>> e = mcb.MCB()\n',
            '>> e.reset()\n',
            '\n\n',
            'To add facts to fact list call:\n',
            '>> e.declare_facts()\n',
            '>> e.declare_facts(\'factname\', \'fuzzyI\', \'fuzzyTod\', \'date\', \'locus\')\n',
            '\n\n',
            'To import a fact csv call:\n',
            '>> e.import_facts(\'./test_suite/fact_CSVs/testX.csv\')\n',
            '\n\n',
            'To view current rule base call:\n',
            '>> e.get_rules()\n',
            '\n\n',
            'To view rule nomenclature reference call:\n',
            '\n\n',
            'To view current fact base call:\n',
            '>> e.facts\n',
            '\n\n',
            'To run Knowledge Engine call:\n',
            '>> e.run()\n',
            '----------------------------------------------------------------------\n',
            '\n  \n \n\n')

#test functions to initialize specific combinations of facts
    def import_facts(self, filename='1'):
        factlines= [x.rstrip('\n') for x in open(filename)]
        while factlines:
            factString = factlines.pop(0)
            factName, factFuzzyI, factFuzzyTod, factDate, factLocus = factString.split(",")
            exec("self.declare(%s(fuzzyI=factFuzzyI, fuzzyTod=factFuzzyTod, date=factDate, locus=factLocus))" % (factName))


#function to automate declaring facts: has a function call mode w/ attributes
##or an interactive mode for terminal
    def declare_facts(self, x='na', y='na', z='na'):
        if x!='na':
            print("""
                'windsp3day', 'seandbcM', 'sea1mM', 'curveB','sea1m','seandbc', 'tide1m', 'windsp', 'sst', or 'parsurf'
                'uLow', 'dLow', 'vLow', 'Low', 'sLow','average', 'sHigh','High', 'vHigh','dHigh', or 'uHigh'
                'even'(00-03), 'midn'(03-06), 'pdaw'(06-09), 'dawn'(09-12),'morn'(12-15), 'midd'(15-18), 'psun'(18-21), 'suns'(21-24), 'nite'(00-09), 'dayb'(09-15), 'aftn'(18-24), 'dayl'(09-24), 'all'(03-03)
                """)
            exec("self.declare(%s(fuzzyI=y, fuzzyTod=z))" % (x))
        else:
            done='n'
            while(done=='n'):
                print("""Which fact would you like to declare?('windsp3day', 'seandbcM', 'sea1mM', 'curveB', 'sea1m', 'seandbc', 'tide1m', 'windsp', 'sst', or 'parsurf').""")
                x = input('  ')
                print("""What is the fuzzyI?('uLow', 'dLow', 'vLow', 'Low', 'sLow','average', 'sHigh', 'High', 'vHigh', 'dHigh', or 'uHigh').""")
                y = input('  ')
                print("""What is the fuzzyTod?( 'even'(00-03), 'midn'(03-06), 'pdaw'(06-09), 'dawn'(09-12), 'morn'(12-15), 'midd'(15-18), 'psun'(21-24), 'suns'(21-24), 'nite'(00-09), 'dayb'(09-15), 'aftn'(18-24), 'dayl'(09-24), 'all'(03-03).""")
                z = input('  ')
                exec("self.declare(%s(fuzzyI=y, fuzzyTod=z))" % (x))
                print("""Are you finished declaring facts? (y/n)""")
                done = input('  ')

###RULE DECLARATIONS###
#Unbelievable value Rules
    @pk.Rule(pk.OR(fact.sst(fuzzyI='uLow'), fact.sst(fuzzyI='uHigh')))
    def u_fI_sst(self):
        print("sst values in unbelievable range")

    @pk.Rule(pk.OR(fact.windsp(fuzzyI='uLow'), fact.windsp(fuzzyI='uHigh')))
    def u_fI_windsp(self):
        print("wind scalar values in unbelievable range")

    @pk.Rule(pk.OR(fact.seandbc(fuzzyI='uLow'), fact.seandbc(fuzzyI='uHigh')))
    def u_fI_seandbc(self):
        print("seandbc values in unbelievable range")

    @pk.Rule(pk.OR(fact.parsurf(fuzzyI='uLow'), fact.parsurf(fuzzyI='uHigh')))
    def u_fI_parsurf(self):
        print("parsurf values in unbelievable range")

    @pk.Rule(pk.OR(fact.tide1m(fuzzyI='uLow'), fact.tide1m(fuzzyI='uHigh')))
    def u_fI_tide1m(self):
        print("tide1m values in unbelievable range")

    @pk.Rule(pk.OR(fact.sea1m(fuzzyI='uLow'), fact.sea1m(fuzzyI='uHigh')))
    def u_fI_sea1m(self):
        print("sea1m values in unbelievable range")

    @pk.Rule(pk.OR(fact.seandbcM(fuzzyI='uLow'), fact.seandbcM(fuzzyI='uHigh')))
    def u_fI_seandbcM(self):
        print("seandbcM values in unbelievable range")

    @pk.Rule(pk.OR(fact.windsp3day(fuzzyI='uLow'), fact.windsp3day(fuzzyI='uHigh')))
    def u_fI_windsp3day(self):
        print("windsp3day values in unbelievable range")

    @pk.Rule(pk.OR(fact.sea1mM(fuzzyI='uLow'), fact.sea1mM(fuzzyI='uHigh')))
    def u_fI_sea1mM(self):
        print("sea1mM values in unbelievable range")

    @pk.Rule(pk.OR(fact.curveB(fuzzyI='uLow'), fact.curveB(fuzzyI='uHigh')))
    def u_fI_curveB(self):
        print("curveB values in unbelievable range")

#Missing info rules
    @pk.Rule( fact.sst(fuzzyI=~anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh')))
    def m_fI_sst(self):
        print("missing or unreadable value for sst fuzzyI")

    @pk.Rule( fact.seandbc(fuzzyI=~anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh')))
    def m_fI_seandbc(self):
        print("missing or unreadable value for seandbc fuzzyI")

    @pk.Rule( fact.parsurf(fuzzyI=~anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh')))
    def m_fI_parsurf(self):
        print("missing or unreadable value for parsurf fuzzyI")

    @pk.Rule(fact.windsp( fuzzyI=~anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh')))
    def m_fI_windsp(self):
        print("missing or unreadable value for windsp fuzzyI")

    @pk.Rule(fact.tide1m(fuzzyI=~anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh')))
    def m_fI_tide1m(self):
        print("missing or unreadable value for tide1m fuzzyI")

    @pk.Rule(fact.sea1m(fuzzyI=~anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh')))
    def m_fI_sea1m(self):
        print("missing or unreadable value for sea1m fuzzyI")

    @pk.Rule(fact.seandbcM(fuzzyI=~anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh')))
    def m_fI_seandbcM(self):
        print("missing or unreadable value for seandbcM fuzzyI")

    @pk.Rule(fact.curveB(fuzzyI=~anyof('uLow', 'dLow','vLow', 'Low', 'sLow', 'average', 'sHigh', 'High', 'vHigh' ,'dHigh', 'uHigh')))
    def m_fI_curveB(self):
        print("missing or unreadable value for curveB fuzzyI")

    @pk.Rule( fact.sea1mM(fuzzyI=~anyof('uLow', 'dLow', 'vLow', 'Low', 'sLow', 'average', 'sHigh', 'High', 'vHigh', 'dHigh', 'uHigh')))
    def m_fI_sea1mM(self):
        print("missing or unreadable value for sea1mM fuzzyI")


#MCB MASS-CORAL-BLEACHING implementation (forecast model has 24 rules)
#Description: Mass bleaching of hard corals

##Ecoforecast Rule #1: Coral-Bleaching-PtwA
##Description: Mass coral bleaching (high in-situ sea temperature + high light + low wind + low tide)
    @pk.Rule(pk.AS.parsurf << fact.parsurf( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=anyof('midd', 'psun', 'dayl', 'aftn', 'all')),
            pk.AS.tide1m << fact.tide1m( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            pk.AS.windsp << fact.windsp( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            pk.AS.seandbc << fact.seandbc( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=pk.W()))
    def mcb_PtwA(self, parsurf, tide1m, windsp, seandbc):
        print("\t  "+parsurf['date']+" Coral-Bleaching-PtwA fired.")
        fact_display(parsurf)
        fact_display(tide1m)
        fact_display(windsp)
        fact_display(seandbc)
        sri = sri_calc(parsurf) +sri_calc(tide1m) +sri_calc(windsp) +sri_calc(seandbc)
        self.SRI += sri
        self.MaxSRI += config.sri_max_4f 
        self.alert_add( 'mcb_PtwA', 'Mass coral bleaching (high in-situ sea temperature + high light + low wind + low tide)', sri, [ parsurf, tide1m, windsp, seandbc])
        self.retract( parsurf)
        self.retract( tide1m)
        self.retract( windsp)
        self.retract( seandbc)

##Ecoforecast Rule #2: Coral-Bleaching-PtwE
##Description: Mass coral bleaching (high 'shallow' sea temperature + high light + low wind + low tide)
    @pk.Rule(pk.AS.parsurf << fact.parsurf( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=anyof('midd', 'dayl', 'all')),
            pk.AS.tide1m << fact.tide1m( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            pk.AS.windsp << fact.windsp( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            pk.AS.sea1m << fact.sea1m( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=pk.W()))
    def mcb_PtwE(self, parsurf, tide1m, windsp, sea1m):
        print("\t  "+parsurf["date"]+ " Coral-Bleaching-PtwE fired.")
        fact_display( parsurf)
        fact_displary( tide1m)
        fact_display( windsp)
        fact_display( sea1m)
        sri= sri_calc(parsurf) +sri_calc(tide1m) +sri_calc(windsp) +sri_calc(sea1m)
        self.SRI += sri
        self.MaxSRI += config.sri_max_4f
        self.alert_add( 'mcb_PtwE', 'Mass coral bleaching (high \'shallow\' sea temperature + high light + low wind + low tide)', sri, [ parsurf, tide1m, windsp, sea1m])
        self.retract( parsurf)
        self.retract( tide1m)
        self.retract( windsp)
        self.retract( sea1m)

##Ecoforecast Rule #3: Coral-Bleaching-PtwS
##Description: Mass coral bleaching (high SST + high light + low wind + low tide)
    @pk.Rule(pk.AS.parsurf << fact.parsurf(fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=anyof('midd', 'dayl', 'all')),
            pk.AS.tide1m << fact.tide1m( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            pk.AS.windsp << fact.windsp( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'aftn', 'all')),
            pk.AS.sst << fact.sst( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=pk.W()))
    def mcb_PtwS(self, parsurf, tide1m, windsp, sst):
        print("\t  "+parsurf["date"]+" Coral-Bleaching-Tlwt fired.")
        fact_display( parsurf)
        fact_display( tide1m)
        fact_display( windsp)
        fact_display( sst)
        sri= sri_calc(parsurf) +sri_calc(tide1m) +sri_calc(windsp) +sri_calc(sst)
        self.SRI += sri
        self.MaxSRI += config.sri_max_4f
        self.alert_add( 'mcb_PtwS', 'Mass coral bleaching (high SST + high light + low wind + low tide)', sri, [ parsurf, tide1m, windsp, sst])
        self.retract( parsurf)
        self.retract( tide1m)
        self.retract( windsp)
        self.retract( sst)

##Ecoforecast Rule #4: Coral-Bleaching-PwA
## Description: Mass coral bleaching (high in-situ sea temperature + high light + low wind)
    @pk.Rule(pk.AS.parsurf << fact.parsurf( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=anyof('midd', 'psun', 'dayl', 'aftn', 'all')),
            pk.AS.windsp << fact.windsp( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            pk.AS.seandbc << fact.seandbc( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=pk.W()))
    def mcb_PwA(self, parsurf, windsp, seandbc):
        print("\t  "+parsurf["date"]+" Coral-Bleaching-PwA fired.")
        fact_display( parsurf)
        fact_display( windsp)
        fact_display( seandbc)
        sri= sri_calc(parsurf) +sri_calc(windsp) +sri_calc(seandbc)
        self.SRI += sri
        self.MaxSRI += config.sri_max_3f
        self.alert_add( 'mcb_PwA', 'Mass coral bleaching (high in-situ sea temperature + high light + low wind)', sri, [ parsurf, windsp, seandbc])
        self.retract( parsurf)
        self.retract( windsp)
        self.retract( seandbc)

##Ecoforecast Rule #5: Coral-Bleaching-twA
##Description: Mass coral bleaching (high in-situ sea temperature + low wind + low tide)
    @pk.Rule(pk.AS.tide1m << fact.tide1m( fuzzyI=anyof('dLow', 'vLow', 'low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            pk.AS.windsp << fact.windsp( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'day', 'dayb', 'aftn', 'all')),
            pk.AS.seandbc << fact.seandbc( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=pk.W()))
    def mcb_twA(self, tide1m, windsp, seandbc):
        print("\t  "+tide1m["date"]+" Coral-Bleaching-twA fired.")
        fact_display( tide1m)
        fact_display( windsp)
        fact_display( seandbc)
        sri= sri_calc(tide1m) +sri_calc(windsp) +sri_calc(seandbc)
        self.SRI += sri
        self.MaxSRI += config.sri_max_3f
        self.alert_add( 'mcb_twA', 'Mass coral bleaching (high in-situ sea temperature + low wind + low tide)', sri, [ tide1m, windsp, seandbc])
        self.retract( tide1m)
        self.retract( windsp)
        self.retract( seandbc)

#Ecoforecast Rule #6: Coral-Bleaching-PwE
##Description: Mass coral bleaching (high 'shallow' sea temperature + high light + low wind)
    @pk.Rule(pk.AS.parsurf << fact.parsurf( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=anyof('midd', 'dayl', 'all')),
            pk.AS.windsp << fact.windsp( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            pk.AS.sea1m << fact.sea1m( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=pk.W()))
    def mcb_PwE(self, parsurf, windsp, sea1m):
        print("\t  "+parsurf["date"]+" Coral-Bleaching-PwE fired.")
        fact_display( parsurf)
        fact_display( windsp)
        fact_display( sea1m)
        sri= sri_calc(parsurf) +sri_calc(windsp) +sri_calc(sea1m)
        self.SRI += sri
        self.MaxSRI += config.sri_max_3f
        self.alert_add( 'mcb_PwE', 'Mass coral bleaching (high \'shallow\' sea temperature + high light + low wind)', sri, [ parsurf, windsp, sea1m])
        self.retract( parsurf)
        self.retract( windsp)
        self.retract( sea1m)

##Ecoforecast Rule #7: Coral-Bleaching-twE
##Description: Mass coral bleaching (high 'shallow' sea temperature + low wind + low tide)
    @pk.Rule(pk.AS.tide1m << fact.tide1m( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            pk.AS.windsp << fact.windsp( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            pk.AS.sea1m << fact.sea1m( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=pk.W()))
    def mcb_twE(self, tide1m, windsp, sea1m):
        print("\t  "+tide1m["date"]+" Coral-Bleaching-twE fired.")
        fact_display( tide1m)
        fact_display( windsp)
        fact_display( sea1m)
        sri= sri_calc(tide1m) +sri_calc(windsp) +sri_calc(sea1m)
        self.SRI += sri
        self.MaxSRI += config.sri_max_3f
        self.alert_add( 'mcb_twE', 'Mass coral bleaching (high \'shallow\' sea temperature + low wind + low tide)', sri, [ tide1m, windsp, sea1m])
        self.retract( tide1m)
        self.retract( windsp)
        self.retract( sea1m)


##Ecoforecast Rule #8: Coral-Bleaching-PwS
##Description: Mass coral bleaching (high SST + high light + low wind)
    @pk.Rule(pk.AS.parsurf << fact.parsurf( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=anyof('midd', 'dayl', 'all')),
            pk.AS.windsp << fact.windsp( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            pk.AS.sst << fact.sst( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=pk.W()))
    def mcb_PwS(self, parsurf, windsp, sst):
        print("\t  "+parsurf["date"]+" Coral-Bleaching-PwS fired.")
        fact_display( parsurf)
        fact_display( windsp)
        fact_display( sst)
        sri= sri_calc(parsurf) +sri_calc(windsp) +sri_calc(sst)
        self.SRI += sri
        self.alert_add( 'mcb_PwS', 'Mass coral bleaching (high SST + high light + low wind)', sri, [ parsurf, windsp, sst])
        self.retract( parsurf)
        self.retract( windsp)
        self.retract( sst)

##Ecoforecast Rule #9: Coral-Bleaching-twS
##Description: Mass coral bleaching (high SST + low wind + low tide)
    @pk.Rule(pk.AS.tide1m << fact.tide1m( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            pk.AS.windsp << fact.windsp( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            pk.AS.sst << fact.sst( fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=pk.W()))
    def mcb_twS(self, tide1m, windsp, sst):
        print("\t  "+tide1m["date"]+" Coral-Bleaching-twS fired.")
        fact_display( tide1m)
        fact_display( windsp)
        fact_display( sst)
        sri= sri_calc(tide1m) +sri_calc(windsp) +sri_calc(sst)
        self.SRI += sri
        self.MaxSRI += config.sri_max_3f
        self.alert_add( 'mcb_twS', 'Mass coral bleaching (high SST + low wind + low tide)', sri, [ tide1m, windsp, sst])
        self.retract( tide1m)
        self.retract( windsp)
        self.retract( sst)

##Ecoforecast Rule #10: Coral-Bleaching-w3A
##Description: Mass coral bleaching (high in-situ sea temperature + doldrums)
    @pk.Rule(pk.AS.windsp3day << fact.windsp3day( fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=pk.W()),
            pk.AS.seandbc << fact.seandbc( fuzzyI=anyof( 'vHigh', 'dHigh'), fuzzyTod=pk.W())) #removed "High" to match MatLab restrictions better
    def mcb_w3A(self, windsp3day, seandbc):
        print("\t  "+windsp3day["date"]+" Coral-Bleaching-w3A fired.")
        fact_display( windsp3day)
        fact_display( seandbc)
        sri= sri_calc(windsp3day) +sri_calc(seandbc)
        self.SRI += sri
        self.MaxSRI += config.sri_max_2f
        self.alert_add( 'mcb_w3A', 'Mass coral bleaching (high in-situ sea temperature + doldrums)', sri, [ windsp3day, seandbc])
        self.retract( windsp3day)
        self.retract( seandbc)

##Ecoforecast Rule #11: Coral-Bleaching-PA
##Description: Mass coral bleaching (very high in-situ sea temperature + very high light)
    @pk.Rule(pk.AS.parsurf << fact.parsurf(fuzzyI=anyof('vHigh', 'dHigh'), fuzzyTod=anyof('midd', 'psun', 'dayl', 'aftn', 'all')),
            pk.AS.seandbc << fact.seandbc(fuzzyI=anyof('vHigh', 'dHigh'), fuzzyTod=pk.W()))
    def mcb_PA(self, parsurf, seandbc):
        print("\t  "+parsurf["date"]+" Coral-Bleaching-PA fired.")
        fact_display( parsurf)
        fact_display( seandbc)
        sri = sri_calc(parsurf) +sri_calc( seandbc)
        self.SRI += sri
        self.MaxSRI += config.sri_max_2f
        self.alert_add( 'mcb_PA', 'Mass coral bleaching (very high in-situ sea temperature + very high light)', sri, [ parsurf, seandbc])
        self.retract( parsurf)
        self.retract( seandbc)

##Ecoforecast Rule #12: Coral-Bleaching-wA
##Description: Mass coral bleaching (very high in-situ sea temperature + very low wind)
    @pk.Rule(pk.AS.windsp << fact.windsp( fuzzyI=anyof('dLow'), fuzzyTod=
        anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')), #removed "vLow" to match MatLab restrictions better
            pk.AS.seandbc << fact.seandbc( fuzzyI=anyof('vHigh', 'dHigh'), fuzzyTod= pk.W()))
    def mcb_wA(self, windsp, seandbc):
        print("\t  "+windsp["date"]+" Coral-Bleaching-wA fired.")
        fact_display( windsp)
        fact_display( seandbc)
        sri= sri_calc( windsp) +sri_calc(seandbc)
        self.SRI += sri
        self.MaxSRI += config.sri_max_2f
        self.alert_add( 'mcb_wA', 'Mass coral bleaching (very high in-situ sea temperature + very low wind)', sri, [ windsp, seandbc])
        self.retract( windsp)
        self.retract( seandbc)

##Ecoforecast Rule #13: Coral-Bleaching-w3E
##Description: Mass coral bleaching (high 'shallow' sea temperature + doldrums)
    @pk.Rule(pk.AS.windsp3day << fact.windsp3day(fuzzyI=anyof('dLow', 'vLow', 'Low'), fuzzyTod=pk.W()),
            pk.AS.sea1m << fact.sea1m( fuzzyI=anyof('High', 'dHigh', 'vHigh'), fuzzyTod=pk.W()))
    def mcb_w3E(self, windsp3day, sea1m):
        print("\t  "+windsp3day["date"]+" Coral-Bleaching-w3E fired.")
        fact_display( windsp3day)
        fact_display( sea1m)
        sri= sri_calc( windsp3day) +sri_calc( sea1m)
        self.SRI += sri
        self.MaxSRI += config.sri_max_2f
        self.alert_add( 'mcb_w3E', 'Mass coral bleaching (high \'shallow\' sea temperature + doldrums)', sri, [ windsp3day, sea1m])
        self.retract( windsp3day)
        self.retract( sea1m)

##Ecoforecast Rule #14: Coral-Bleaching-PE
##Description: Mass coral bleaching (very high 'shallow' sea temperature + very high light)
    @pk.Rule(pk.AS.parsurf << fact.parsurf(fuzzyI=anyof('vHigh', 'dHigh'), fuzzyTod=anyof('midd', 'dayl', 'all')),
            pk.AS.sea1m << fact.sea1m( fuzzyI=anyof('vHigh', 'dHigh'), fuzzyTod=pk.W()))
    def mcb_PE(self, parsurf, sea1m):
        print("\t  "+parsurf["date"]+" Coral-Bleaching-PE fired.")
        fact_display( parsurf)
        fact_display( sea1m)
        sri= sri_calc( parsurf) +sri_calc( sea1m)
        self.SRI += sri
        self.MaxSRI += config.sri_max_2f
        self.alert_add( 'mcb_PE', 'Mass coral bleaching (very high \'shallow\' sea temperature + very high light)', sri, [ parsurf, sea1m])
        self.retract( parsurf)
        self.retract( sea1m)

##Ecoforecast Rule #15: Coral-Bleaching-wE
##Description: Mass coral bleaching (very high 'shallow' sea temperature + very low wind)
    @pk.Rule(pk.AS.windsp << fact.windsp(fuzzyI=anyof('dLow', 'vLow'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            pk.AS.sea1m << fact.sea1m(fuzzyI=anyof('vHigh', 'dHigh'), fuzzyTod=pk.W()))
    def mcb_wE(self, windsp, sea1m):
        print("\t  "+windsp["date"]+" Coral-Bleaching-wE fired.")
        fact_display( windsp)
        fact_display( sea1m)
        sri= sri_calc( windsp) +sri_calc( sea1m)
        self.SRI += sri
        self.MaxSRI += config.sri_max_2f
        self.alert_add( 'mcb_wE', 'Mass coral bleaching (very high \'shallow\' sea temperature + very low wind)', sri, [ windsp, sea1m])
        self.retract( windsp)
        self.retract( sea1m)

##Ecoforecast Rule #16: Coral-Bleaching-PS
##Description: Mass coral bleaching (very high SST + very high light)
    @pk.Rule(pk.AS.parsurf << fact.parsurf(fuzzyI=anyof('vHigh', 'dHigh'), fuzzyTod=anyof('midd', 'dayl', 'all')),
            pk.AS.sst << fact.sst(fuzzyI=anyof('vHigh', 'dHigh'), fuzzyTod=pk.W()))
    def mcb_PS(self, parsurf, sst):
        print("\t  "+parsurf["date"]+" Coral-Bleaching-PS fired.")
        fact_display( parsurf)
        fact_display( sst)
        sri= sri_calc( parsurf) +sri_calc( sst)
        self.SRI += sri
        self.MaxSRI += config.sri_max_2f
        self.alert_add( 'mcb_PS', 'Mass coral bleaching (very high SST + very high light)', sri, [ parsurf, sst])
        self.retract( parsurf)
        self.retract( sst)


##Ecoforecast Rule #17: Coral-Bleaching-wS
##Description: Mass coral bleaching (very high SST + very low wind)
    @pk.Rule(pk.AS.windsp << fact.windsp(fuzzyI=anyof('dLow', 'vLow'), fuzzyTod=anyof('morn', 'midd', 'psun', 'dayl', 'dayb', 'aftn', 'all')),
            pk.AS.sst << fact.sst(fuzzyI=anyof('vHigh', 'dHigh'), fuzzyTod=pk.W()))
    def mcb_wS(self, windsp, sst):
        print("\t  "+windsp["date"]+" Coral-Bleaching-wS fired.")
        fact_display( windsp)
        fact_display( sst)
        sri= sri_calc( windsp) +sri_calc( sst)
        self.SRI += sri
        self.MaxSRI += config.sri_max_2f
        self.alert_add( 'mcb_wS', 'Mass coral bleaching (very high SST + very low wind)', sri, [ windsp, sst])
        self.retract( windsp)
        self.retract( sst)


##Ecoforecast Rule #18: Coral-Bleaching-B
##Description: Mass coral bleaching (Berkelmans bleaching curve)
    @pk.Rule(pk.AS.curveB << fact.curveB(fuzzyI=anyof('Conductive', 'vConductive'), fuzzyTod=pk.W()))
    def mcb_B(self, curveB):
        print("\t  "+curveB["date"]+" Coral-Bleaching-B fired.")
        fact_display( curveB)
        sri= sri_calc( curveB)
        self.SRI += sri
        self.MaxSRI += config.sri_max_1f
        self.alert_add( 'mcb_B', 'Mass coral bleaching (Berkelmans bleaching curve)', sri, [ curveB])
        self.retract( curveB)


##Ecoforecast Rule #19: Coral-Bleaching-A
##Description: Mass coral bleaching (drastic high in-situ sea temperature)
    @pk.Rule(pk.AS.seandbc << fact.seandbc( fuzzyI=anyof('dHigh'), fuzzyTod=pk.W()))
    def mcb_A(self, seandbc):
        print("\t  "+seandbc["date"]+" Coral-Bleaching-A fired.")
        fact_display( seandbc)
        sri= sri_calc( seandbc)
        self.SRI += sri
        self.MaxSRI += config.sri_max_1f
        self.alert_add( 'mcb_A', 'Mass coral bleaching (drastic high in-situ sea temperature)', sri, [ seandbc])
        self.retract( seandbc)


##Ecoforecast Rule #20: Coral-Bleaching-BB
##Description: Mass coral mortality (>50%) for local sensitive species (Berkelmans)
    @pk.Rule(pk.AS.curveB << fact.curveB(fuzzyI=anyof('Mortality', 'hMortality'), fuzzyTod=pk.W())) 
    def mcb_BB(self, curveB):
        print("\t  "+curveB["date"]+" Coral-Bleaching-BB fired.")
        fact_display( curveB)
        sri= sri_calc( curveB)
        self.SRI += sri
        self.MaxSRI += config.sri_max_1f
        self.alert_add( 'mcb_BB', 'Mass coral mortality (>50%) for local sensitive species (Berkelmans)', sri, [curveB])
        self.retract( curveB)


##Ecoforecast Rule #21: Coral-Bleaching-EM
##Description: Mass coral bleaching (high monthly mean 'shallow' sea temperature)
    @pk.Rule(pk.AS.sea1mM << fact.sea1mM(fuzzyI=anyof('High', 'vHigh', 'dHigh'), fuzzyTod=pk.W()))
    def mcb_EM(self, sea1mM):
        print("\t  "+sea1mM+" Coral-Bleaching-EM fired.")
        fact_display( sea1mM)
        sri = sri_calc( sea1mM)
        self.SRI += sri
        self.MaxSRI += config.sri_max_1f
        self.alert_add( 'mcb_EM', 'Mass coral bleaching (high monthly mean \'shallow\' sea temperature)', sri, [sea1mM])
        self.retract( sea1mM)


##Ecoforecast Rule #22: Coral-Bleaching-AM
##Description: Mass coral bleaching (high monthly mean in situ sea temperature)
    @pk.Rule(pk.AS.seandbcM << fact.seandbcM(fuzzyI=anyof( 'vHigh', 'dHigh'), fuzzyTod=pk.W())) #removed "High" to match MatLab restrictions better
    def mcb_AM(self, seandbcM):
        print("\t  "+seandbcM["date"]+" Coral-Bleaching-AM fired.")
        fact_display( seandbcM)
        sri= sri_calc( seandbcM)
        self.SRI += sri
        self.MaxSRI += config.sri_max_1f
        self.alert_add( 'mcb_AM', 'Mass coral bleaching (high monthly mean in situ sea temperature)', sri, [seandbcM])
        self.retract( seandbcM)


##Ecoforecast Rule #23: Coral-Bleaching-E
##Description: Mass coral bleaching (drastic high 'shallow' sea temperature)
    @pk.Rule(pk.AS.sea1m << fact.sea1m(fuzzyI=pk.L('dHigh'), fuzzyTod=pk.W()))
    def mcb_E(self, sea1m):
        print("\t  "+sea1m["date"]+" Coral-Bleaching-E fired.")
        fact_display( sea1m)
        sri= sri_calc( sea1m)
        self.SRI += sri
        self.MaxSRI += config.sri_max_1f
        self.alert_add( 'mcb_E', "Mass coral bleaching (drastic high \'shallow\' sea temperature)", sri, [sea1m])
        self.retract( sea1m)


##Ecoforecast Rule #24: Coral-Bleaching-S
##Description: Mass coral bleaching (drastic high SST)
    @pk.Rule(pk.AS.sst << fact.sst(fuzzyI=pk.L('dHigh'), fuzzyTod=pk.W()))
    def mcb_S(self, sst):
        print("\t  "+sst["date"]+" Coral-Bleaching-S fired.")
        fact_display( sst)
        sri= sri_calc( sst)
        self.SRI += sri
        self.MaxSRI += config.sri_max_1f
        self.alert_add( "mcb_S", "Mass coral bleaching (drastic high SST)", sri, [sst])
        self.retract( sst)


def knowledge_engine( factlist, station):
    e= MCB(station)
    e.reset()
    if len(factlist) == 0:
        return 0, 0, {}
    for f in factlist:
        e.declare( f)
    e.run()
    return e.SRI, e.MaxSRI, e.alerts
