#!/usr/bin/env python
import os
from MantidFramework import mtd
mtd.initialise()
import datetime
starttime = datetime.datetime.now()

wksp = "VULCAN_5836"
workdir = "./"
nxsdir = "./"
peakpos = 1.3823
dstep =-0.002
dmin = 0.2
dmax = 10.0

peakmin = peakpos-0.1
peakmax = peakpos+0.1

# Load event file for East and West detectors
LoadSNSEventNexus(Filename=nxsdir+wksp+"_event.nxs", OutputWorkspace=wksp)
# Sort output events	      
Sort(InputWorkspace=wksp) 

# Remove old calibration files
cmd = "rm "+workdir+wksp+".cal*"
os.system(cmd) 
# Add detector groups to calibration file
CreateCalFileByNames(InstrumentWorkspace=wksp, GroupingFileName=workdir+wksp+".cal",
    GroupNames="bank21,bank22,bank23,bank26,bank27,bank28")
#Optimize Detectors
DspacemaptoCal(InputWorkspace=wksp, DspacemapFile="./pid_offset_vulcan_new.dat",CalibrationFile=workdir+wksp+".cal",FileType="VULCAN-ASCII")
# Align detectors using new calibration file with offsets
AlignDetectors(InputWorkspace=wksp, OutputWorkspace=wksp, 
    CalibrationFile=workdir+wksp+".cal", VULCANDspacemapFile=True)
# Diffraction focusing using new calibration file with offsets
DiffractionFocussing(InputWorkspace=wksp, OutputWorkspace=wksp,
    GroupingFileName=workdir+wksp+".cal")
# Rebin file with offsets
Rebin(InputWorkspace=wksp, OutputWorkspace=wksp,Params=str(dmin)+","+str(dstep)+","+str(dmax))
#ConvertUnits(InputWorkspace=wksp, OutputWorkspace=wksp,Target="TOF")
#NormaliseByCurrent(InputWorkspace=wksp, OutputWorkspace=wksp)
#SaveSNSNexus(InputFilename=wksp+".nxs",InputWorkspace=wksp, OutputFilename=wksp+"_mantid.nxs", Compress=True)
gl = plotSpectrum(wksp, [0,1,2,3,4,5])
l = gl.activeLayer()
l.setAxisScale(Layer.Bottom, 0.95,1.35)


elapsedtime = datetime.datetime.now() - starttime
print "total time to run", str(elapsedtime)

