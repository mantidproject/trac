from mantid.simpleapi import OSIRISDiffractionReduction
OSIRISDiffractionReduction(
OutputWorkspace="OsirisDiffractionTest",
Sample="osiris00102567.raw,osiris00102568.raw",
CalFile="osiris_041_RES10.cal", Vanadium="osiris00102543.raw,osiris00102544.raw,osiris00102545.raw,osiris00102542.raw")
