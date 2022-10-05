# This is the serious verification script for ticket 9643 for supporting VULCAN

import math

# Constants/Input
eventfname = "/SNS/VULCAN/IPTS-10560/0/51624/NeXus/VULCAN_51624_event.nxs"
vuloffsetfname = "pid_offset_vulcan_new.dat"
effgeofname = "mod_difc_vulcan_new.dat"

def ReadEffectiveGeometryFile(filename, throwemptybank):
	""" Read the effective geometry information file from VULCAN
	Example: mod_difc_vulcan_new.dat
	"""
	# Import file contents
	try:
		gfile = open(filename, "r")
		lines = gfile.readlines()
		gfile.close()
	except IOError, err:
		print "Geometry file %s cannot be opened or read. " % (filename)
		return (False, None)

	# Dictionary to return
	geomdict = {}

	# Import information
	for line in lines:
		line = line.strip()

		# reject empty line and comment line
		if len(line) == 0:
			continue
		terms = line.split()
		if terms[0].isdigit() is False:
			continue

		try:
			bankid = int(terms[0])
			difc = float(terms[2])
			refpid = int(terms[3])
			twotheta = float(terms[4])
		except Exception:
			print "Line '%s' is not conformed with standard format. " % (line)
			continue 

		# reject non-used bank
		if throwemptybank is True and refpid == 0:
			continue 

		geomdict[bankid] = {"DIFC": difc, "2Theta": twotheta, "RefPID": refpid}

	return (True, geomdict)


def ManualDiffractionFocus(eventwsname, groupwsname, groupdict=None):
	""" Manually diffraction focuss the event workspace in unit of TOF
	Arguement:
	- groupdict :: Dictionary is for second level group such that to sum spectra for 
	               2 banks and 1 bank option. 
	"""
	eventws = mtd[eventwsname]
	groupws = mtd[groupwsname]

	# Check unit
	evunit = eventws.getAxis(0).getUnit().unitID()
	if evunit != "TOF":
		raise NotImplementedError("EventWorkspace must be TOF. It is %s now!" % (evunit))

	# Sum spectrum
	groupspecdict = {}
	for groupid in xrange(1, 7):
		groupspecdict[groupid] = ""

	# Get list of spectrum
	for iws in xrange(groupws.getNumberHistograms()):
		gid = int(groupws.readY(iws)[0])
		groupspecdict[gid] += "%d," % (iws)

	for groupid in xrange(1, 7):
		groupspecdict[groupid] = groupspecdict[groupid][0:-1]

        #for groupid in xrange(1, 7):
	#	print "Group %d: %s" % (groupid, groupspecdict[groupid])

	for groupid in xrange(1, 7):
		if len(groupspecdict[groupid]) == 0:
			print "No spectrum in group/bank %d.  Skip!" % (groupid)
			continue
		outwsname = eventwsname+"_bank%d" % (groupid)
		SumSpectra(InputWorkspace=eventws, OutputWorkspace=outwsname,
			ListOfWorkspaceIndices=groupspecdict[groupid])

		outws = mtd[outwsname]
		print "Workspace %s has %d events. " % (outwsname, outws.getNumberEvents())

	return

	# The followed is useless
	# Second-level grouping
	if groupdict is not None:
		for subgroupname in groupdict.keys():
			subgrouplist = groupdict[subgroupname]
			outputwsname = eventwsname+"_%s"%(subgroupname)
			if len(subgrouplist) == 0:
				raise NotImplementedError("Empty subgroup!")
			else:
				wsname0 = eventwsname+"_bank%d" % (subgrouplist[0])
				CloneWorkspace(InputWorkspace = wsname0, OutputWorkspace = outputwsname)
				for gid in subgrouplist[1:]:
					wsnamex = eventwsname + "_bank%d" % (gid)
					Plus(LHSWorkspace = outputwsname, RHSWorkspace = wsnamex, OutputWorkspace = outputwsname)

	# ENDIF

	return


def main(bankmode):
	""" verification main
	- bankmode :: integer (1, 2, 6)
	"""
	# Import VULCAN DIFC geometry file
	tup = ReadEffectiveGeometryFile(effgeofname, True)
	if tup[0] is False:
		print "Unable to read VUCLAN DIFC geometry file %s. Stop!" % (effgeofname)
		return

	geomdict = tup[1]
	print "Used banks: ", sorted(geomdict.keys())

	# Load event data
	eventwsname = eventfname.split("/")[-1].split(".")[0]
	Load(Filename = eventfname, OutputWorkspace=eventwsname)
	eventws = mtd[eventwsname]

	# Calcualte L2
	L1 = eventws.getInstrument().getSource().getPos().norm()
	for bankid in sorted(geomdict.keys()):
		difc = geomdict[bankid]["DIFC"]
		twotheta = geomdict[bankid]["2Theta"]
		l = difc/252.777/2./math.sin(twotheta*0.5*math.pi/180.)
		l2 = l - L1
		geomdict[bankid]["L2"] = l2
		print "Bank %d, L = %f, L2 = %f" % (bankid, l, l2)
		
	################################################################################### 
	# Load Vulcan Calibration Filename and Focus event in unit of TOF
	###################################################################################
	# Convert the effective DIFCs and 2thetas to N-bank mode
	newgeomdict = {}
	if bankmode == 2:
		for bankid in [21, 22, 23]:
			newgeomdict[bankid] = geomdict[22]
		for bankid in [26, 27, 28]:
			newgeomdict[bankid] = geomdict[27]
	elif bankmode == 1:
		for bankid in geomdict.keys():
			newgeomdict[bankid] = geomdict[22]
	elif bankmode == 6:
		newgeomdict = geomdict
	else:
		raise NotImplementedError("Bank mode %d is not supported. " % (bankmode))
	
	# Write out the input string for LoadVulcanCalFile
	bankids = ""
	effdifcs = ""
	eff2thetas = ""
	for bankid in newgeomdict:
		difc = newgeomdict[bankid]["DIFC"]
		twotheta = newgeomdict[bankid]["2Theta"]
		bankids+= "%d," % (bankid)
		effdifcs +="%f," % (difc)
		eff2thetas += "%f," % (twotheta)

	# remove last ','
	bankids = bankids[0:-1]
	effdifcs = effdifcs[0:-1]
	eff2thetas = eff2thetas[0:-1]

	print "Bank IDs = ", bankids 
	print "DIFCs    = ", effdifcs
	print "2Thetas  = ", eff2thetas

        tofcal_eventwsname = eventwsname+"_TOF_Cal"
	CloneWorkspace(InputWorkspace=eventwsname, OutputWorkspace=tofcal_eventwsname)

	# LoadVulcanCalFile and work on an test EventWorkspace
	if bankmode == 2:
	    groupmode = '2Banks'
	elif bankmode == 1:
	    groupmode = '1Bank'
	elif bankmode == 6:
		groupmode = '6Modules'
	LoadVulcanCalFile(
		OffsetFilename=r'pid_offset_vulcan_new.dat',
		BadPixelFilename=r'bad_pids_vulcan_new_6867_7323.dat',
		Grouping = groupmode,
		BankIDs = bankids,
		EffectiveDIFCs = effdifcs,
		Effective2Thetas = eff2thetas,
		WorkspaceName='Vulcan_idl',
		EventWorkspace=tofcal_eventwsname)
		
	Rebin(InputWorkspace=tofcal_eventwsname, OutputWorkspace=tofcal_eventwsname, Params="-0.001", PreserveEvents=True)

	# Do diffraction focussing manually
	groupwsname = "Vulcan_idl_group"
	tofcaleventwsname = eventfname.split("/")[-1].split(".")[0] + "_TOF_Cal"	
	
	if groupmode == 1:
		subgroupdict = {"Pack": [1,2,3,4,5,6]}
	elif groupmode == 2:
		subgroupdict = {"East": [2, 1, 3], "West": [5,4,6]}	
	else:
		subgroupdict = None
	ManualDiffractionFocus(tofcaleventwsname, groupwsname, subgroupdict)
	

	###################################################################################
	# Focus event data by using SNSPowderReduction's approach (for vervification)
	###################################################################################
	if bankmode == 1:
	    banks = [22]
	elif bankmode == 2:
	  banks = [22, 27]
	elif bankmode == 6:
	  banks = geomdict.keys()

	eff2thetas = ""
	effl2s = ""
	for bid in sorted(banks):
		twotheta = geomdict[bid]["2Theta"]
		l2 = geomdict[bid]["L2"]
		effl2s += "%f," % (l2)
		eff2thetas += "%f," %(twotheta)
	effl2s = effl2s[0:-1]
	eff2thetas = eff2thetas[0:-1]

	print "L2s: ", effl2s
	print "2Thetas: ", eff2thetas

	groupwsname = "Vulcan_idl_group"
	offsetswsname = "Vulcan_idl_offsets"
	print "Event workspace: ", eventwsname
	AlignDetectors(InputWorkspace = eventwsname, OutputWorkspace = eventwsname,
		OffsetsWorkspace = offsetswsname)
	DiffractionFocussing(InputWorkspace = eventwsname, OutputWorkspace = eventwsname,
		GroupingWorkspace = groupwsname, PreserveEvents=True)
	EditInstrumentGeometry(Workspace = eventwsname,
		L2 = effl2s, Polar = eff2thetas)
	ConvertUnits(InputWorkspace=eventwsname, OutputWorkspace=eventwsname,
		Target="TOF", Emode="Elastic")

	###################################################################################	
	# Compare
	###################################################################################
	eventws = mtd[eventwsname]
	for iws in xrange(eventws.getNumberHistograms()):
		numevents = eventws.getEventList(iws).getNumberEvents()
		print "Spectrum %d: Number of events = %d" % (iws, numevents)
	
	binpar = "10000., -0.001, 50000."
	Rebin(InputWorkspace=eventws, OutputWorkspace=eventws, Params=binpar)


	for bankid in xrange(1, bankmode+1):
		tofcaleventws = mtd["VULCAN_51624_event_TOF_Cal_bank%d"%(bankid)]
		Rebin(InputWorkspace=tofcaleventws, OutputWorkspace=tofcaleventws, Params=binpar)
	
		Minus(LHSWorkspace=eventws, RHSWorkspace=tofcaleventws, AllowDifferentNumberSpectra=True, OutputWorkspace="diff_%d"%(bankid))
		ConvertToMatrixWorkspace(InputWorkspace="diff_%d"%(bankid), OutputWorkspace="diff_%d"%(bankid))

	# combine the difference workspaces
	targetdiffws = mtd["diff_%d"%(1)]
	for bankid in xrange(2, bankmode+1):
		sourcediffws = mtd["diff_%d"%(bankid)]
		iws = bankid-1
		for i in xrange(len(sourcediffws.readY(iws))):
			targetdiffws.dataY(iws)[i] = sourcediffws.readY(iws)[i]
		DeleteWorkspace(Workspace=sourcediffws)

	RenameWorkspace(InputWorkspace=targetdiffws, OutputWorkspace="Diff_%s"%(eventwsname))

	return


if __name__ == "__main__":
    numbanks = 6 # option: 1, 2, 6
    main(numbanks)
