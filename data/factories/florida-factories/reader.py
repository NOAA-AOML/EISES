import csv
import re

with open('smkf1-factories.csv','r') as csvfile:
    smkreader = csv.reader(csvfile, delimiter=',')
    for row in smkreader:
        numbers= [0, 1, 2, 3, 4, 5, 6, 7, 8]
        num=[]
        for i in numbers:
            if ( i+4<len(row)):
                num.append(re.search('([+-]?\d+\.*\d*)\s([+-]?\d+\.*\d*)', row[i+4]))
        print('\nranges[\'smkf1\'][{}\']= [{}'.format(row[0], num[0].group(1)), end='')
        for i in numbers:
            if(i+4<len(row)):
                print(', {}'.format(num[i].group(2)),end='')
        print('], standardfuzzy]', end='')


