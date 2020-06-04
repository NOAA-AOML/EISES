#!/usr/bin/env python3

### csv_to_JSON converts a data stream CSV to A standardized JSON file format for
### fact factories to process

__author__= "Madison.Soden"
__date__= "Thu Jul 19, 2018  03:20PM"
__license__= "NA?"
__email__= "madison.soden@gmail.com"
__status__= "Production"

import pandas as pd

with open('file.dat', 'r') as fin:
    data = fin.read().splitlines(True)
header= data[:1]
with open('file1.dat', 'w') as fout:
    fout.writelines(data[1:])
foo = pd.read_csv("file1.dat")
foo = foo.drop(foo.index[1])
foo = foo.reset_index(drop=True)
