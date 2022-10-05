########################################################################
# Verify ticket 10928 for HB2A IDF
########################################################################
import math

vecx = []
vecy = []
vece = []
for i in xrange(44):
    vecx.extend([0., 1.0])
    vecy.append( math.exp( -(float(i)-10.)**2/3.**2) + 2.)
    vece.append(1.0)

CreateWorkspace(OutputWorkspace="MockHB2AData", DataX=vecx, DataY=vecy, DataE=vece, NSpec=44)

AddSampleLog(Workspace="MockHB2AData", LogName="rotangle", LogText="5.0", LogType="Number Series")

CloneWorkspace(InputWorkspace='MockHB2AData', OutputWorkspace='Mock2')

LoadInstrument(Workspace="MockHB2AData", InstrumentName="HB2A", RewriteSpectraMap=True)
LoadInstrument(Workspace="Mock2", Filename="HB2A_Definition_manual.xml", RewriteSpectraMap=True)

ws = mtd["MockHB2AData"]
hb2a = ws.getInstrument()

ws2 = mtd['Mock2']
hb2a2 = ws2.getInstrument()

# Compare source
source = hb2a.getSource()
source2 = hb2a2.getSource()
print "Difference in source position: ", source.getPos() - source2.getPos()

sample = hb2a.getSample()
sample2 = hb2a2.getSample()
print "Difference in sample position: ", sample.getPos() - sample2.getPos()

numdet = 0
for i in xrange(100):
    try:
        detx = hb2a.getDetector(i)
        detpos = detx.getPos()
        numdet += 1
        dety = hb2a2.getDetector(i)
        detpos2 = dety.getPos()
        print detx.getFullName(), " Diff in position = ", detpos - detpos2
    except RuntimeError as e:
        # print e
        continue

print "Total %d detectors. " % (numdet)
