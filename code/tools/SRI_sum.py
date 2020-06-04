import csv
from os import listdir
from os.path import isfile
import pandas as pd
import configParameters as config

def main( stationName): 
    SRI_file_path= config.data+"/SRI/"+stationName
    SRI_file_list= [ f for f in listdir(SRI_file_path) if isfile(SRI_file_path+"/"+f)]
    SRI_file_list.sort()
    SRI_year_sums= {}
    for f in SRI_file_list:
        year= f[-8:-4]
        filename= SRI_file_path+"/"+f
        df= pd.read_csv( filename, header= None, names= ['A','B'])
        SRI_sum= df['B'].sum()
        SRI_year_sums[year]= SRI_sum
    return pd.DataFrame.from_dict( SRI_year_sums, orient='index', columns=['SRI'])
