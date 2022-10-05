from mantid.simpleapi import OSIRISDiffractionReduction
OSIRISDiffractionReduction(
OutputWorkspace="OsirisDiffractionTest",
Sample="osi00102569.raw, osi00102570.raw",
CalFile="osiris_041_RES10.cal",
Vanadium="OSI89757, OSI89758, OSI89759, OSI89760, OSI89761")