LoadRaw('IRS21360', 'IRS21360')

GroupDetectors('IRS21360', 'irs21360_grpdA', MapFile='grpA.map')
GroupDetectors('IRS21360', 'irs21360_grpdB', MapFile='grpB.map')

wsA = mtd['irs21360_grpdA']
wsB = mtd['irs21360_grpdB']

detA = wsA.getDetector(3)

detB = wsB.getDetector(3)

print 'WSA', detA.getDetectorIDs()
print 'WSB', detB.getDetectorIDs()