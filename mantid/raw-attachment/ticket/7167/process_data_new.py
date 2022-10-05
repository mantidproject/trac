
folder = '/SNS/SNAP/IPTS-8561/shared/'


if mtd.doesExist('cols')== False : CreateGroupingWorkspace(InstrumentName='SNAP',GroupDetectorsBy='Column',OutputWorkspace='cols')
if mtd.doesExist('mask_edges')== False : LoadMask(Instrument='SNAP',InputFile=r'/SNS/SNAP/IPTS-8561/shared/mask_detectors.xml',OutputWorkspace='mask_edges')

#Loading Vanadium Spectra Files


runs = [12278]
runs=range(12281,12317)+[12279]


for run in runs:
	print 'Processing run %s'%run
	LoadEventNexus(Filename=r'SNAP_%s_event.nxs'%run,OutputWorkspace='SNAP_%s'%run,Precount='1',MonitorsAsEvents='1')	
	MaskDetectors(Workspace='SNAP_%s'%run, MaskedWorkspace='mask_edges')
	AddSampleLog(Workspace='SNAP_%s'%run,LogName='det_arc1',LogText='-50.75',LogType='Number Series')
	LoadInstrument(Workspace='SNAP_%s'%run,InstrumentName='SNAP',RewriteSpectraMap='0')
	AlignDetectors(InputWorkspace='SNAP_%s'%run, OutputWorkspace='SNAP_%s_d'%run,CalibrationFile=folder+'/SNAP_calibrate_d12276_2013_05_17.cal') 
#	ConvertUnits(InputWorkspace='SNAP_%s'%run,OutputWorkspace='SNAP_%s_d'%run,Target='dSpacing')
	Rebin(InputWorkspace='SNAP_%s_d'%run,OutputWorkspace='SNAP_%s_d'%run,Params='0.5,-0.004,8')
	DiffractionFocussing(InputWorkspace='SNAP_%s_d'%run,OutputWorkspace='SNAP_%s_col'%run,GroupingWorkspace='cols',PreserveEvents='0')
	SumSpectra(InputWorkspace='SNAP_%s_col'%run,OutputWorkspace='SNAP_%s_14'%run,ListOfWorkspaceIndices='0,1,2,3',IncludeMonitors='0')
	SumSpectra(InputWorkspace='SNAP_%s_col'%run,OutputWorkspace='SNAP_%s_56'%run,ListOfWorkspaceIndices='4,5',IncludeMonitors='0')
	ConjoinWorkspaces(InputWorkspace1='SNAP_%s_14'%run,InputWorkspace2='SNAP_%s_56'%run,CheckOverlapping='0')
	ConvertUnits(InputWorkspace='SNAP_%s_col'%run,OutputWorkspace='SNAP_%s_col_tof'%run,Target='TOF',AlignBins='0')
	ConvertUnits(InputWorkspace='SNAP_%s_14'%run,OutputWorkspace='SNAP_%s_14_tof'%run,Target='TOF',AlignBins='0')
	
#	ConvertToPointData(InputWorkspace='SNAP_%s_col'%run,OutputWorkspace='SNAP_%s_col'%run)
	Divide(LHSWorkspace='SNAP_%s_col'%run,RHSWorkspace='SNAP_12278_col',OutputWorkspace='SNAP_%s_nor'%run)
	ReplaceSpecialValues(InputWorkspace='SNAP_%s_nor'%run,OutputWorkspace='SNAP_%s_nor'%run,NaNValue='0',BigNumberThreshold='30')
	SaveAscii(InputWorkspace='SNAP_%s_nor'%run, Filename=folder+'data/d_spacing/SNAP_%s_d.csv'%run)
#	RemoveLogs(Workspace='SNAP_%s_col'%run)
#	RemoveLogs(Workspace='SNAP_%s_nor'%run)
	
#	ConvertToPointData(InputWorkspace='SNAP_%s_14'%run,OutputWorkspace='SNAP_%s_14'%run)
	Divide(LHSWorkspace='SNAP_%s_14'%run,RHSWorkspace='SNAP_12278_14',OutputWorkspace='SNAP_%s_nor_14'%run)
	ReplaceSpecialValues(InputWorkspace='SNAP_%s_nor_14'%run,OutputWorkspace='SNAP_%s_nor_14'%run,NaNValue='0',BigNumberThreshold='30')
	SaveAscii(InputWorkspace='SNAP_%s_nor_14'%run, Filename=folder+'data/d_spacing/SNAP_%s_d.csv'%run)
#	RemoveLogs(Workspace='SNAP_%s_14'%run)
#	RemoveLogs(Workspace='SNAP_%s_nor_14'%run)
	
#	ConvertToPointData(InputWorkspace='SNAP_%s_col_tof'%run,OutputWorkspace='SNAP_%s_col_tof'%run)
	Divide(LHSWorkspace='SNAP_%s_col_tof'%run,RHSWorkspace='SNAP_12278_col_tof',OutputWorkspace='SNAP_%s_nor_tof'%run)
	ReplaceSpecialValues(InputWorkspace='SNAP_%s_nor_tof'%run,OutputWorkspace='SNAP_%s_nor_tof'%run,NaNValue='0',BigNumberThreshold='30')
	SaveGSS(InputWorkspace='SNAP_%s_nor_tof'%run,Filename=folder +'data/gsas/SNAP_%s.gsa'%run, Format = 'SLOG',SplitFiles='False')
	SaveFocusedXYE(InputWorkspace='SNAP_%s_nor_tof'%run,Filename=folder +'data/fullprof/SNAP_%s.dat'%run,SplitFiles='True',IncludeHeader='1')
	
#	ConvertToPointData(InputWorkspace='SNAP_%s_14_tof'%run,OutputWorkspace='SNAP_%s_14_tof'%run)
	Divide(LHSWorkspace='SNAP_%s_14_tof'%run,RHSWorkspace='SNAP_12278_14_tof',OutputWorkspace='SNAP_%s_nor_14_tof'%run)
	ReplaceSpecialValues(InputWorkspace='SNAP_%s_nor_14_tof'%run,OutputWorkspace='SNAP_%s_nor_14_tof'%run,NaNValue='0',BigNumberThreshold='30')
	SaveGSS(InputWorkspace='SNAP_%s_nor_14_tof'%run,Filename=folder +'data/gsas/SNAP_%s_14.gsa'%run, Format = 'SLOG',SplitFiles='False')
	SaveFocusedXYE(InputWorkspace='SNAP_%s_nor_14_tof'%run,Filename=folder +'data/fullprof/SNAP_%s_14.dat'%run,SplitFiles='True',IncludeHeader='1')

	
	DeleteWorkspace(Workspace='SNAP_%s'%run)
	DeleteWorkspace(Workspace='SNAP_%s_d'%run)
	DeleteWorkspace(Workspace='SNAP_%s_col'%run)
	DeleteWorkspace(Workspace='SNAP_%s_14'%run)
	DeleteWorkspace(Workspace='SNAP_%s_col_tof'%run)
	DeleteWorkspace(Workspace='SNAP_%s_14_tof'%run)
	DeleteWorkspace(Workspace='SNAP_%s_nor_tof'%run)
	DeleteWorkspace(Workspace='SNAP_%s_nor_14_tof'%run)

