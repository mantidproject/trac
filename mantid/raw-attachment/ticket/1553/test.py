from MantidFramework import *
from mantidsimple import *
mtd.initialise(False)
import os 

TEST_DIR = "../../../Test/Data/SANS2D/"
filepath = os.path.join(TEST_DIR, "BioSANS_test_data.xml") 
instrpath = "../../../Test/Instrument/BIOSANS_Definition.xml" 

success = True 

loader = LoadSpice2D(filepath, "test") 
test1 = mtd['test'].getInstrument().getComponentByName("detector1").getPos().getZ()==6.0 
test2 = mtd['test'].getInstrument().getStringParameter("detector-name")[0] == 'detector1' 

LoadEmptyInstrument(instrpath, 'inst') 
loader = LoadSpice2D(filepath, "test") 
test3 = mtd['test'].getInstrument().getComponentByName("detector1").getPos().getZ()==6.0 
test4 = len(mtd['test'].getInstrument().getStringParameter("detector-name")) == 1 
test5 = mtd['inst'].getInstrument().getStringParameter("detector-name")[0] == 'detector1' 

print "SUCCESS ? " 
print test1 
print test2 
print test3 
print test4 
print test5 

