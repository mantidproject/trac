def compareEvents(detId, left, right):
    lftTofs = left.getTofs()
    lftPuls = left.getPulseTimes()
    if len(lftTofs) != len(lftPuls):
        raise RuntimeError("Something really wrong with %d left: %d != %d" % (detId, len(lftTofs), len(lftPuls)))

    rgtTofs = right.getTofs()
    rgtPuls = right.getPulseTimes()
    if len(rgtTofs) != len(rgtPuls):
        raise RuntimeError("Something really wrong with %d right: %d != %d" % (detId, len(rgtTofs), len(rgtPuls)))

    if len(lftTofs) != len(rgtTofs):
        print "detId %d has different length events %d != %d" % (len(lftTofs), len(rgtTofs))
        return

    results = []

    total_num_diff = 0
    for i in range(len(lftTofs)):
        is_diff = False
        if abs(lftTofs[i]-rgtTofs[i]) >= .1: # tolerance of 100ns
            is_diff = True
            results.append("tof[%3d] %f != %f (diff=%f)" % (i, lftTofs[i], rgtTofs[i], \
                                                               rgtTofs[i]-lftTofs[i]))
        if lftPuls[i] != rgtPuls[i]:
            diff = rgtPuls[i]-lftPuls[i]
            if abs(diff.total_nanoseconds()) > 1:
                is_diff = True
                diff = diff.total_nanoseconds()/1000000000. # convert to seconds
                minutes = int(diff/60.)
                seconds = abs(diff - minutes*60.)
                diff = [minutes, seconds]
                results.append("pulse[%3d] %s != %s (diff=%dm%ds)" % (i, str(lftPuls[i]), str(rgtPuls[i]), \
                                                                       diff[0], diff[1]))                  
        if is_diff:
            total_num_diff += 1

    if total_num_diff>0:
        print "****", detId, "numEvents:", len(lftTofs), "totalDiff:", total_num_diff
        for result in results:
            print result

    return total_num_diff


files = ("CNCS_7860_event.nxs","CNCS_7860_neutron_event.dat")
files = ("CNCS_67147_event.nxs","/SNS/CNCS/IPTS-5383/0/67147/preNeXus/CNCS_67147_neutron_event.dat")

nexus = LoadEventNexus(files[0], BankName="bank3")
prenexus = LoadEventPreNexus(files[1], SpectrumList="2048-3071")
#SortEvents(nexus, "Pulse Time + TOF")
#SortEvents(prenexus, "Pulse Time + TOF")
numNxsSpec = nexus.getNumberHistograms()
numPreSpec = prenexus.getNumberHistograms()
total_diff = 0
for i in range(numPreSpec):
    preEvents = prenexus.getEventList(i)
    detId = prenexus.getSpectrum(i).getDetectorIDs()[0]
    nxsEvents = None
    for j in range(i, numNxsSpec):
        if nexus.getSpectrum(j).hasDetectorID(detId):
            nxsEvents = nexus.getEventList(j)
            break

    total_diff += compareEvents(detId, preEvents, nxsEvents)
if total_diff == nexus.getNumberEvents():
    print "all events different out of %d" % nexus.getNumberEvents()
else:
    print "%d events different out of %d" % (total_diff, nexus.getNumberEvents())
