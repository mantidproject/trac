from mantid.simpleapi import *

#test file
sample = 'osiris00102605.raw'
#vanadium files
vanFiles = ['osiris00102542.raw', 'osiris00102543.raw', 'osiris00102544.raw']

vanFiles =','.join(vanFiles)

#calibration file
calFile = 'osiris_041_RES10.cal'

OSIRISDiffractionReduction(
Sample=sample,
Vanadium=vanFiles,
CalFile=calFile,
OutputWorkspace="OutWs")

ConvertUnits(InputWorkspace="OutWs", OutputWorkspace="OutWs_tof", Target='TOF')