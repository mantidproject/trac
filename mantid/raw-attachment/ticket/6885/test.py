config['default.facility']="SNS"

DgsReduction(
             SampleInputFile="/SNS/ARCS/IPTS-3310/1/10451/NeXus/ARCS_10451_event.nxs",
             OutputWorkspace="w1",
             ShowIntermediateWorkspaces=True,
             IncidentBeamNormalisation="ByCurrent",
             TimeIndepBackgroundSub=True,
             DetectorVanadiumInputFile="/SNS/ARCS/IPTS-3310/1/10454/NeXus/ARCS_10454_event.nxs",
             UseBoundsForDetVan=True,
             DetVanIntRangeLow=5000.0,
             DetVanIntRangeHigh=7000.0,
             DetVanIntRangeUnits="TOF",
            )
