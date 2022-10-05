import math
import os

InstName = "ARCS"
#InstName = "CNCS"
#InstName = "SEQ"

# EDIT THIS: Directory of a Mantid subversion checkout
MantidSrcHome=os.path.expanduser(os.path.join("~", "Mantid"))
DataDir = os.path.join("Test", "Data", "sns_event_prenexus")

if InstName == "ARCS":
    DataFileName = os.path.join(MantidSrcHome, DataDir, "ARCS_5025",
                                "ARCS_5025_neutron_event.dat")
    DetectorNumber = 0
elif InstName == "CNCS":
    DataFileName = os.path.join(MantidSrcHome, DataDir, 
                                "CNCS_7850_neutron_event.dat")
    DetectorNumber = 0
elif InstName == "SEQ":
    DataFileName = os.path.join(MantidSrcHome, DataDir, "SEQ_2731",
                                "SEQ_2731_neutron_event.dat")
    DetectorNumber = 37888

print DataFileName
WkspcName = InstName.lower()

LoadEventPreNeXus(EventFilename=DataFileName, PadEmptyPixels="1",
                  OutputWorkspace=WkspcName)
outWS = mtd[WkspcName]

source = outWS.getInstrument().getSource()
sample = outWS.getInstrument().getSample()

samplePos = sample.getPos()
beamPos = samplePos - source.getPos()

detector = outWS.getDetector(DetectorNumber)

r = detector.getDistance(sample)
polar = detector.getTwoTheta(samplePos, beamPos)
azi = detector.getPhi()

print "Distance: %.5f" % r
print "Polar: %.5f" % polar
print "Azimuthal: %.6f" % azi
