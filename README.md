# About EISES
The EISES coding project has been separated into four subsections of the software to be implemented. These sections of the program are, in procedural order: data feed processing, fact generation, rule evaluation , and alert distribution (see below).
[insert image here]
<!--- [EISES graphic]()-->
## Current Functionality

## Future Applications


***
# EISES Development Checklist:
( todo: :white_large_square:, in progress: :hammer:, completed :heavy_check_mark:)
##### Last Updated: 10/08/2019
##### Questions: madison.soden@noaa.gov
<!---
:white_large_square:
:heavy_check_mark:
:hammer:
-->
#### Data Processing:
:heavy_check_mark: 1. Compile a testing data set to use when adapting EISES to be used in PE project.  
  ><b>Testing data: </b>
  >:heavy_check_mark: OBS data  
  >:heavy_check_mark: ABS data   
  >:heavy_check_mark: Light attenuation (surface light and underwater light if possible)  
  >:heavy_check_mark: Deposition  
  >:heavy_check_mark: Waves  
  >:heavy_check_mark: Ocean Current information 

:hammer: 2. Adapt EISES's data loading scripts, and fact class definitions to accept information from these types on sensors. 

:hammer: 3. Adapt EISES's parsers to get data from thredds server and/or parse csv file types. 
  >:hammer: waiting to get copy of csv file format.
 
#### Fact Generation:
#### Rule Evaluation:
#### Alert Distribution:
:hammer: 1. Create use-case/design document based on testing Alert request list (X/J).  
:white_large_square: 2. Review possible design/development of alert distribution and web-based archives.
