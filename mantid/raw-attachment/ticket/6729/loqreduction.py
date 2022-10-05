from mantid.simpleapi import * 
import ISISCommandInterface as ici

ici.LOQ()
ici.Set1D()

print ici.ReductionSingleton().instrument.getDetector('FRONT').rescaleAndShift.fitShift
print ici.ReductionSingleton().instrument.getDetector('FRONT').rescaleAndShift.fitScale


ici.MaskFile('/tmp/loqsystem/MASKLOQ_MAN.112A')

print ici.ReductionSingleton().instrument.getDetector('FRONT').rescaleAndShift.fitShift
print ici.ReductionSingleton().instrument.getDetector('FRONT').rescaleAndShift.fitScale
