from mantid.simpleapi import *
config['default.facility']="ISIS"

DgsReduction(
             SampleInputFile="MAR11001.RAW",
             OutputWorkspace="MAR11001_spe",
             IncidentEnergyGuess=12.0,
             EnergyTransferRange="-11,0.05,11",
             HardMaskFile="mar11015.msk",
             GroupingFile="mari_res.map",
             IncidentBeamNormalisation="ToMonitor",
             DetectorVanadiumInputFile="MAR11060.RAW",
             BackgroundCheck=True,
             DoAbsoluteUnits=True,
             AbsUnitsGroupingFile="mari_res.map",
             AbsUnitsDetectorVanadiumInputFile="MAR11060.RAW",
             AbsUnitsIncidentEnergy=12,
             AbsUnitsMaximumEnergy=1.0,
             SampleMass=10.0,
             SampleRmm=435.96,
            )

