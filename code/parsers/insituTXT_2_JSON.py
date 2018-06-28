### insituTXT_to_JSON converts a data stream txt file (for a year of mlrf1) to A standardized JSON file format for
### fact factories to process
__author__="Madison.Soden"
__date__="Wed Jun 27 11:32:41 2018"
__license__="NA?"
__version__="insituTXT_to_JSON"
__email__="madison.soden@gmail.com"
__status__="Production"

import pandas as pd
import json
filename = "mlrf1h2017"

with open('../../data/mlrf1_insitu_data/'+ filename+'.txt', 'r') as fin:
    data = fin.read().splitlines(True)
header= data[0]
units= data[1]
data=data[2:]

##Parsing units and header
header= header[1:-1]
headerp= header.split(' ')
headerp= list(filter(None, headerp))

units= units[1:-1]
unitsp= units.split(' ')
unitsp= list(filter(None, unitsp))

##initalizing  data frame with header and units
unitsp=[unitsp]
df= pd.DataFrame(unitsp, columns=headerp)

#paresing the rest of data into properly formated lists
datal= len(data)
i=0
while (i < datal):
    datap= data[i]
    datap=datap[:-1]
    datap=datap.split(' ')
    datap= list(filter(None, datap))
    data[i]= datap
    i= i+1

df1= pd.DataFrame(data, columns=headerp)
df= df.append(df1)

#not sure which json writing method to use
jsondf=df.to_json(orient='split')

with open('../../data/mlrf1_insitu_data/'+filename+'.json', 'w') as f:
     json.dump(jsondf, f)

