# Test Detector Group

# Any MAPS file other than a calibration run can be used here.
# If copied across, the accompanying files may also need to be copied across to ensure grouping.
path = r"C:/Temp/" # Path name of folder containing input and output files
filename = 'MAPS17275.raw' # Name of calibration run

# Get calibration raw file and integrate it    
WS = Load(path+filename)  #'raw' in 'rawCalibInstWS' means unintegrated.

group = WS.getDetector(2)
IDs = group.getDetectorIDs()
names = group.getName()
fullNames = group.getFullName()
sep = group.getNameSeparator()
print "Detector IDs",IDs 
print "Detector names",names 
print "Detector full names",fullNames 
print "The separator",sep,"should occur after each name in the detector names and full names."
