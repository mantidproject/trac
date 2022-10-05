def createVULCANWorkspace():
    """
    """
    import mantid.simpleapi as api

    api.Load(Filename = "/home/wzz/Projects/MantidTests/Tickets/9101_VULCAN_RecordTxt/VULCAN_42583_event.nxs",
            OutputWorkspace = "VULCAN_42583",
            MetaDataOnly = True,
            LoadLogs = True)

    wksp = AnalysisDataService.retrieve("VULCAN_42583")

    return wksp
    
def createVULCANRecordTitles():
    """ Create a list of records for VULCAN
    """
    titlebase = [
        ("RUN",             "run_number", None),
        ("IPTS",            "IPTS", None),
        ("Title",           "run_title", None),
        ("Notes",           "Notes", None),
        ("Sample",          "Sample", None),
        ("StartTime",       "run_start", None),
        ("Duration",        "duration", None),
        ("ProtonCharge",    "proton_charge", "sum"),
        ("TotalCounts",     "TotalCounts", None),
        ("Monitor1",        "Monitor2", None),
        ("Monitor2",        "Monitor3", None),
        ("X",               "X", "0"),
        ("Y",               "Y", "0"),
        ("Z",               "Z", "0"),
        ("O",               "Omega", "0"),       
        ("HROT",            "HROT", "0"),
        ("MTSDisplacement", "loadframe.displacement", "0"),
        ("MTSForce",        "loadframe.force", "0"),
        ("MTSStrain",       "loadframe.strain", "0"),
        ("MTSStress",       "loadframe.stress", "0"),
        ("MTSAngle",        "loadframe.rot_angle", "0"),
        ("MTSTorque",       "loadframe.torque", "0"),
        ("MTSLaser",        "loadframe.laser", "0"),
        ("MTSlaserstrain",  "loadframe.laserstrain", "0"),
        ("MTSDisplaceoffset","loadframe.x_offset", "0"),
        ("MTSAngleceoffset", "loadframe.rot_offset", "0"),
        ("MTST1",           "loadframe.furnace1", "0"),
        ("MTST2",           "loadframe.furnace2", "0"),
        ("MTST3",           "loadframe.extTC3", "0"),
        ("MTST4",           "loadframe.extTC4", "0"),
        ("FurnaceT",        "furnace.temp1", "0"),
        ("FurnaceOT",       "furnace.temp2", "0"),
        ("FurnacePower",    "furnace.power", "0"),
        ("VacT",            "partlow1.temp", "0"),
        ("VacOT",           "partlow2.temp", "0")
    ]
    
    sampletitles = []
    samplenames = []
    sampleops = []
    
    for i in xrange(len(titlebase)):
        tuple3 = titlebase[i]
        sampletitles.append(tuple3[0])
        samplenames.append(tuple3[1])
        sampleops.append(tuple3[2])
    # ENDFOR
    
    return sampletitles, samplenames, sampleops


# Generate the matrix workspace with some logs
#     api.Load(Filename = "/home/wzz/Projects/MantidTests/Tickets/9101_VULCAN_RecordTxt/VULCAN_42583_event.nxs",
#             OutputWorkspace = "VULCAN_42583",
#             MetaDataOnly = True,
#             LoadLogs = True)

ws = createVULCANWorkspace()

vulcantitles, vulcansamplenames, vulcanops = createVULCANRecordTitles()

# Test algorithm
ExportExperimentLog(InputWorkspace = str(ws),
    OutputFilename = "/tmp/AutoRecord.txt",
    FileMode = "append",
    SampleLogNames = vulcansamplenames,
    SampleLogTitles = vulcantitles,
    SampleLogOperation = vulcanops)

