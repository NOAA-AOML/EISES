#!/usr/bin/env python3

#test_init_Facts.py
#tests fact initialization

__author__= "Madison.Soden"
__date__= "Thu Jul 19, 2018  03:23PM"
__license__= "NA?"
__email__= "madison.soden@gmail.com"
__status__= "Production"

import sys
sys.path.append('../')
import mcb
import pytest

@pytest.fixture(scope="session", autouse=True)
def declared_engine():
    """Returns knowledge engine that has been initially reset"""
    print('\n____declared_engine(): ')
    e = mcb.MCB()
    yield e
    print('\n____tear down engine')

@pytest.fixture(scope = 'class', params = [1,2,3,])
def psetup(declared_engine, request):
    """Passes parameters into test classes"""
    print('\n_+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++reset engine++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
    declared_engine.reset()


    print('\n____passing parameters')

    #initializing
    if(request.param == 1):
        testnames = ('sst', 'seandbc', 'parsurf', 'windsp', 'tide1m', 'sea1m',
            'seandbcM', 'windsp3day', 'sea1mM', 'curveB')
        filename = "./fact_CSVs/test1.csv"
        rulesfiredorder = ('u_fI_seandbcM', 'u_fI_seandbc')

    if(request.param == 2):
        testnames = ('parsurf', 'windsp', 'sst', 'tide1m', 'seandbc', 'sea1m', 'seandbcM', 'windsp3day', 'curveB', 'sea1mM')
        filename = "./fact_CSVs/test2.csv"
        rulesfiredorder = ( 'u_fI_curveB', 'u_fI_windsp3day', 'mcb_AM', 'u_fI_seandbc', 'mcb_PwS')

    if(request.param == 3):
        testnames = ('parsurf', 'windsp', 'sst', 'tide1m', 'seandbc', 'sea1m', 'seandbcM', 'windsp3day', 'curveB', 'sea1mM')
        filename = "./fact_CSVs/test3.csv"
        rulesfiredorder = ('u_fI_curveB', 'mcb_AM', 'mcb_PwS', 'm_fI_sea1m', 'm_fI_seandbc')

    #create everything for instance

    #inject class variables
    request.cls.testnames = testnames
    request.cls.filename = filename
    request.cls.rulesfiredorder = rulesfiredorder
    yield
    #delete everything for instance


#@pytest.mark.parametrize("i", [ (0), (1), ] )
@pytest.mark.usefixtures( 'declared_engine', 'psetup')
class Test1:

    def test_fact_init_order( self, declared_engine, psetup):
        print('\n____test_fact_init_order(declared_engine): ')
        declared_engine.import_facts( self.filename)
        assert (declared_engine.facts[0].__class__ == mcb.fact.InitialFact)
        assert (declared_engine.facts[1].__class__.__name__ == self.testnames[0]) 
        assert (declared_engine.facts[2].__class__.__name__ == self.testnames[1])
        assert (declared_engine.facts[3].__class__.__name__ == self.testnames[2])
        assert (declared_engine.facts[4].__class__.__name__ == self.testnames[3])
        assert (declared_engine.facts[5].__class__.__name__ == self.testnames[4])
        assert (declared_engine.facts[6].__class__.__name__ == self.testnames[5])
        assert (declared_engine.facts[7].__class__.__name__ == self.testnames[6])
        assert (declared_engine.facts[8].__class__.__name__ == self.testnames[7])
        assert (declared_engine.facts[9].__class__.__name__ == self.testnames[8])
        assert (declared_engine.facts[10].__class__.__name__ == self.testnames[9])
        assert (declared_engine.facts.last_index == 11)

    def test_function_output(self, declared_engine, psetup):
        print("\n____running declared_engine")
        #declared_engine.run()
        print('\n____finding consequents')
        consequents = declared_engine.agenda.activations
        numConsequents = len(consequents)
        i = 0 
        if (i <  numConsequents):
            assert consequents[i].rule.__name__ == self.rulesfiredorder[i]
            i = i +1
        print('____running engine')
        declared_engine.run()

