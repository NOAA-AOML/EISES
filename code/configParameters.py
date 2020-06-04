#generate none relative file paths
#sampling rates dictionary of sensors
import os

#PATHS
currentLocation= os.path.realpath(__file__)
code= currentLocation[:-20]
data= currentLocation[:-24]+"data"


#CONSTANTS
insitu_samplingRate= 365*24
sri_max_4f= 24*2.5*4
sri_max_3f= 24*2.5*3
sri_max_2f= 24*2.5*2
sri_max_1f= 24*2.5

