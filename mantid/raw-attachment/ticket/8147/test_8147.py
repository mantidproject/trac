from mantid.simpleapi import *
from mantid import config
import ISISCommandInterface as ici
import SANSBatchMode as batch
import SANSadd2 as sansadd

output_file = '99630sannotrans'
csv_file = 'input.csv'
result = ''


f = open(csv_file,'w')
print >> f, "sample_sans,99630-add,output_as, %s"%output_file
f.close()
runnum = '99630'
sansadd.add_runs((runnum, runnum),'LOQ','.RAW')


ici.LOQ()
ici.Detector("main-detector-bank")
ici.Set1D()
ici.MaskFile('MASK.094AA')    
batch.BatchReduce(csv_file, 'nxs', plotresults=False)
    

ici._refresh_singleton()  
ici.LOQ()
ici.Detector("main-detector-bank")
ici.Set1D()
ici.MaskFile('MASK.094AA')
LOQ99630 = Load('LOQ'+runnum+'.RAW')
LOQ99630 += LOQ99630
ici.AssignSample(LOQ99630, reload=False)
result = ici.WavRangeReduction(None,None,None)

print CheckWorkspacesMatch('99630sannotrans', result, 1.e-8)