from math import *
from mantid.simpleapi import *
from mantid.api import WorkspaceGroup
try:
  from mantidplot import *
except ImportError:
  pass

import numpy as n

def addRuns(runlist,wname):
  #DeleteWorkspace(str(wname))
  output=str(wname)
  if runlist[0] != "0":
    #nzeros=8-len(str(runlist[0]))
    #fpad=""
    #for i in range(nzeros):
    #  fpad+="0"
    #filename="offspec"+fpad+str(runlist[0])+".nxs"
    #fname=str(FileFinder.findRuns(filename))
    #fname=str.replace(fname,'\\','/')
    #fname=str.replace(fname,'[','')
    #fname=str.replace(fname,']','')
    #fname=str.replace(fname,'\'','')
    #fname=fname.lower()
    ##fname=str.replace(fname,'.nxs','.raw')
    #Load(fname,output)
	Load(str(runlist[0]),OutputWorkspace=output)
  else:
    #dae="ndx"+config['default.instrument'].lower()
    dae="ndxoffspec"
    LoadDAE(DAEname=dae,OutputWorkspace=output,SpectrumMin="1")
    #LoadLiveData(Instrument="OFFSPEC",AccumulationMethod="Replace",OutputWorkspace="output")
    if isinstance(mtd[output], WorkspaceGroup):
    	for k in mtd[output].getNames():
    		mtd[k].setYUnit('Counts')
    else:
    	mtd[output].setYUnit('Counts')

  if len(runlist) > 1:
    for i in range(1,len(runlist)):
      if runlist[i] != "0":
        #nzeros=8-len(str(runlist[i]))
        #fpad=""
        #for j in range(nzeros):
        #  fpad+="0"
        #filename="offspec"+fpad+str(runlist[i])+".nxs"
        #fname=str(FileFinder.findRuns(filename))
        #fname=str.replace(fname,'\\','/')
        #fname=str.replace(fname,'[','')
        #fname=str.replace(fname,']','')
        #fname=str.replace(fname,'\'','')
        #fname=fname.lower()
        ##fname=str.replace(fname,'.nxs','.raw')
        #Load(fname,"wtemp")
		Load(str(runlist[i]),OutputWorkspace="wtemp")
      else:
		#dae="ndx"+config['default.instrument'].lower()
		dae="ndxoffspec"
		LoadDAE(DAEname=dae,OutputWorkspace="wtemp",SpectrumMin="1")
		#LoadLiveData(Instrument="OFFSPEC",AccumulationMethod="Replace",OutputWorkspace="output")
		if isinstance(mtd['wtemp'], WorkspaceGroup):
			for k in mtd['wtemp'].getNames():
				mtd[k].setYUnit('Counts')
		else:
			mtd[output].setYUnit('Counts')
      Plus(output,"wtemp",OutputWorkspace=output)
      DeleteWorkspace("wtemp")

  #logger.notice("addRuns Completed")
#
#===================================================================================================================
#
'''
parse a text string of the format "1-6:2+8+9,10+11+12+13-19:3,20-24"
to return a structure containing the separated lists [1, 3, 5, 8, 9], 
[10, 11, 12, 13, 16, 19] and [20, 21, 22, 23, 24]
as integer lists that addRuns can handle.
'''
def parseRunList(istring):
	if len(istring) >0: 
		s1=istring.split(',')
		rlist1=[]
		for i in range(len(s1)):
			tstr=s1[i].strip()
			if len(tstr) > 0:
				rlist1.append(tstr)
		rlist=[]
		for i in range(len(rlist1)):
			rlist2=[]
			if rlist1[i].find('+') >= 0:
				tstr=rlist1[i].split('+')
				for j in range(len(tstr)):
					if tstr[j].find(':') >=0 and tstr[j].find('-') >=0:
						tstr[j].strip()
						tstr2=tstr[j].split('-')
						tstr3=tstr2[1].split(':')
						r1=range(int(tstr2[0]),int(tstr3[0])+1,int(tstr3[1]))
						for k in r1:
							rlist2.append(str(k))
					elif tstr[j].find('-') >=0:
						tstr[j].strip()
						tstr2=tstr[j].split('-')
						r1=range(int(tstr2[0]),int(tstr2[1])+1)
						for k in r1:
							rlist2.append(str(k))
					else:
						rlist2.append(tstr[j])
			else:
				if rlist1[i].find(':') >=0 and rlist1[i].find('-')>=0:
					rlist1[i].strip()
					tstr2=rlist1[i].split('-')
					tstr3=tstr2[1].split(':')
					r1=range(int(tstr2[0]),int(tstr3[0])+1,int(tstr3[1]))
					for k in r1:
						rlist2.append(str(k))
				elif rlist1[i].find('-')>=0:
					rlist1[i].strip()
					tstr2=rlist1[i].split('-')
					r1=range(int(tstr2[0]),int(tstr2[1])+1)
					for k in r1:
						rlist2.append(str(k))
				else:
					rlist2.append(rlist1[i])
			rlist.append(rlist2)
	return rlist
#
#===================================================================================================================
#
def parseNameList(istring):
	s1=istring.split(',')
	namelist=[]
	for i in range(len(s1)):
		tstr=s1[i].strip()
		namelist.append(tstr)	
	return namelist

#
#===================================================================================================================
#
def floodnorm(wkspName,floodfile):
   #
   # pixel by pixel efficiency correction for the linear detector
   #
   flood_wksp = "ld240flood"
   if  flood_wksp not in mtd:
	   LoadNexusProcessed(Filename=floodfile,OutputWorkspace=flood_wksp)

   Divide(LHSWorkspace=wkspName, RHSWorkspace=flood_wksp, OutputWorkspace=wkspName)
#
#===================================================================================================================
#
# Plot a bunch of workspaces as 2D maps
# using the supplied limits and log scale settings
#
def plot2D(wkspNames,limits,logScales):
	nplot=0
	workspace_mtx=[]
	wNames=parseNameList(wkspNames)
	for i in range(len(wNames)):
		w1=mtd[wNames[i]]
		if isinstance(w1, WorkspaceGroup):
			w1names=w1.getNames()
			for j in range(len(w1names)):
				#workspace_mtx.append(mantidplot.importMatrixWorkspace(w1names[j]))
				workspace_mtx.append(mantidplot.importMatrixWorkspace(w1names[j]))
				gr2d=workspace_mtx[nplot].plotGraph2D()
				nplot=nplot+1
				l=gr2d.activeLayer()
				if logScales[0]=="0":
					l.setAxisScale(mantidplot.Layer.Bottom,float(limits[0]),float(limits[1]))
				elif logScales[0]=="2":
					l.setAxisScale(mantidplot.Layer.Bottom,float(limits[0]),float(limits[1]),1)
				if logScales[1]=="0":
					l.setAxisScale(mantidplot.Layer.Left,float(limits[2]),float(limits[3]))
				elif logScales[1]=="2":
					l.setAxisScale(mantidplot.Layer.Left,float(limits[2]),float(limits[3]),1)
				if logScales[2]=="0":
					l.setAxisScale(mantidplot.Layer.Right,float(limits[4]),float(limits[5]))
				elif logScales[2]=="2":
					l.setAxisScale(mantidplot.Layer.Right,float(limits[4]),float(limits[5]),1)
		else:
			workspace_mtx.append(mantidplot.importMatrixWorkspace(wNames[i]))
			gr2d=workspace_mtx[nplot].plotGraph2D()
			nplot=nplot+1
			l=gr2d.activeLayer()
			if logScales[0]=="0":
				l.setAxisScale(mantidplot.Layer.Bottom,float(limits[0]),float(limits[1]))
			elif logScales[0]=="2":
				l.setAxisScale(mantidplot.Layer.Bottom,float(limits[0]),float(limits[1]),1)
			if logScales[1]=="0":
				l.setAxisScale(mantidplot.Layer.Left,float(limits[2]),float(limits[3]))
			elif logScales[1]=="2":
				l.setAxisScale(mantidplot.Layer.Left,float(limits[2]),float(limits[3]),1)
			if logScales[2]=="0":
				l.setAxisScale(mantidplot.Layer.Right,float(limits[4]),float(limits[5]))
			elif logScales[2]=="2":
				l.setAxisScale(mantidplot.Layer.Right,float(limits[4]),float(limits[5]),1)
		
	logger.notice("plot2D finished")
#
#===================================================================================================================
#
# Plot a bunch of workspaces as 2D maps
# using the supplied limits and log scale settings
#
def XYPlot(wkspNames,spectra,limits,logScales,errors,singleFigure):
	wNames=parseNameList(wkspNames)
	spec=parseNameList(spectra)
	ploterr=0
	xLog=0
	yLog=0
	if errors == "2":
		ploterr=1
	if logScales[0] == "2":
		xLog=1
	if logScales[1] == "2":
		yLog=1
		
	if singleFigure == "2":
		p1=plotSpectrum(wNames,spec,ploterr)
		l=p1.activeLayer()
		l.setAxisScale(mantidplot.Layer.Bottom,float(limits[0]),float(limits[1]),xLog)
		l.setAxisScale(mantidplot.Layer.Left,float(limits[2]),float(limits[3]),yLog)
	else:	
		for i in range(len(wNames)):
			p1=plotSpectrum(wNames[i],spec,ploterr)
			l=p1.activeLayer()
			l.setAxisScale(mantidplot.Layer.Bottom,float(limits[0]),float(limits[1]),xLog)
			l.setAxisScale(mantidplot.Layer.Left,float(limits[2]),float(limits[3]),yLog)
		
	logger.notice("XYPlot finished")
#
#===================================================================================================================
#
def nrtestfn(runlist,wnames):
	
	rlist=parseRunList(runlist)
	logger.notice("This is the runlist:"+str(rlist))
	namelist=parseNameList(wnames)
	logger.notice("This is the nameslist:"+str(namelist))
	for i in range(len(rlist)):
		addRuns(rlist[i],namelist[i])
		#Load(Filename="L:/RawData/cycle_10_1/OFFSPEC0000"+str(rlist[i][j])+".nxs",OutputWorkspace="w"+str(rlist[i][j]),LoaderName="LoadISISNexus")

	logger.notice("nrtestfn completed")
'''
	output="w7503"
	plotper=[1,2]
	rebpars="0.5,0.025,14.5"
	spmin=0
	spmax=239
	Load(Filename="L:/RawData/cycle_10_1/OFFSPEC00007503.nxs",OutputWorkspace=output,LoaderName="LoadISISNexus")
	workspace_mtx=[]
	nplot=0
	for i in plotper:
		ConvertUnits(InputWorkspace=output+"_"+str(i),OutputWorkspace=output+"_"+str(i),Target="Wavelength",AlignBins="1")
		Rebin(InputWorkspace=output+"_"+str(i),OutputWorkspace=output+"_"+str(i),Params=rebpars)
		CropWorkspace(InputWorkspace=output+"_"+str(i),OutputWorkspace=output+"_"+str(i)+"m",StartWorkspaceIndex="1",EndWorkspaceIndex="1")
		CropWorkspace(InputWorkspace=output+"_"+str(i),OutputWorkspace=output+"_"+str(i)+"d",StartWorkspaceIndex=str(spmin+4),EndWorkspaceIndex=str(spmax+4))
		Divide(output+"_"+str(i)+"d",output+"_"+str(i)+"m",OutputWorkspace=output+"_"+str(i)+"n")
		workspace_mtx.append(mantidplot.importMatrixWorkspace(output+"_"+str(i)+"n"))
		gr2d=workspace_mtx[nplot].plotGraph2D()
		nplot=nplot+1
		l=gr2d.activeLayer()
	
	logger.notice("quickPlot Finished")
'''
def removeoutlayer(wksp):
	# remove counts from bins where there are so few counts it makes a mess of the polarisation
	# calculation
	a1=mtd[wksp]
	nspec=a1.getNumberHistograms()
	x=a1.readX(0)
	for i in range(nspec):
		for j in range(len(x)-1):
			y=a1.readY(i)[j]
			if (y<2):
				a1.dataY(i)[j]=0.0;
				a1.dataE(i)[j]=0.0;

def nrSESANSFn(runList,nameList,P0runList,P0nameList,minSpec,maxSpec,upPeriod,downPeriod,existingP0,SEConstants,gparams,convertToSEL,lnPOverLam,diagnostics="0",removeoutlayer="0",floodfile="none",):
	nlist=parseNameList(nameList)
	logger.notice("This is the sample nameslist:"+str(nlist))
	rlist=parseRunList(runList)
	logger.notice("This is the sample runlist:"+str(rlist))
	for i in range(len(rlist)):
		addRuns(rlist[i],nlist[i])

	P0nlist=parseNameList(P0nameList)
	logger.notice("This is the P0nameslist:"+str(P0nlist))
	if existingP0 != "2":
		P0rlist=parseRunList(P0runList)
		logger.notice("This is the P0runlist:"+str(P0rlist))
		for i in range(len(P0rlist)):
			addRuns(P0rlist[i],P0nlist[i])

	mon_spec=int(gparams[3])-1
	minSp=int(minSpec)-1
	maxSp=int(maxSpec)-1
	reb=gparams[0]+","+gparams[1]+","+gparams[2]
	if len(gparams) == 5:
		mapfile=gparams[4]
	
	for i in nlist:
		a1=mtd[i+"_1"]
		nspec=a1.getNumberHistograms()
		if nspec == 1030 and minSp != 3:
			GroupDetectors(InputWorkspace=i,OutputWorkspace=i,MapFile=mapfile)
		ConvertUnits(InputWorkspace=i,OutputWorkspace=i,Target="Wavelength",AlignBins=1)
		Rebin(i,reb,OutputWorkspace=i)
		if (removeoutlayer != "0"):
			removeoutlayer(i+"_1")
			removeoutlayer(i+"_2")
		CropWorkspace(InputWorkspace=i,OutputWorkspace=i+"mon",StartWorkspaceIndex=mon_spec,EndWorkspaceIndex=mon_spec)
		if nspec == 245:
			CropWorkspace(InputWorkspace=i,OutputWorkspace=i+"2ddet",StartWorkspaceIndex=4,EndWorkspaceIndex=243)
			if (floodfile != "none"):
				floodnorm(i+"2ddet",floodfile)
		if nspec == 1030:
			CropWorkspace(InputWorkspace=i,OutputWorkspace=i+"2ddet",StartWorkspaceIndex=3,EndWorkspaceIndex=124)
		if int(maxSpec) > int(minSpec):
			SumSpectra(InputWorkspace=i,OutputWorkspace=i+"det",StartWorkspaceIndex=minSp,EndWorkspaceIndex=maxSp)
		else:
			CropWorkspace(InputWorkspace=i,OutputWorkspace=i+"det",StartWorkspaceIndex=minSp,EndWorkspaceIndex=maxSp)

		Divide(LHSWorkspace=i+"det",RHSWorkspace=i+"mon",OutputWorkspace=i+"norm")
		if nspec > 4 and minSp != 3:
			Divide(LHSWorkspace=i+"2ddet",RHSWorkspace=i+"mon",OutputWorkspace=i+"2dnorm")
		DeleteWorkspace(i+"mon")
		if (diagnostics == "0"):
			DeleteWorkspace(i+"det")
		DeleteWorkspace(i)
		Minus(LHSWorkspace=i+"norm_"+upPeriod,RHSWorkspace=i+"norm_"+downPeriod,OutputWorkspace="num")
		Plus(LHSWorkspace=i+"norm_2",RHSWorkspace=i+"norm_1",OutputWorkspace="den")
		Divide(LHSWorkspace="num",RHSWorkspace="den",OutputWorkspace=i+"pol")
		ReplaceSpecialValues(InputWorkspace=i+"pol",OutputWorkspace=i+"pol",NanValue=0.0,NaNError=0.0,InfinityValue=0.0,InfinityError=0.0)
		if nspec >4 and minSp != 3:
			#print i+"2dnorm_"+upPeriod
			#print i+"2dnorm_"+downPeriod
			Minus(LHSWorkspace=i+"2dnorm_"+upPeriod,RHSWorkspace=i+"2dnorm_"+downPeriod,OutputWorkspace="num")
			Plus(LHSWorkspace=i+"2dnorm_2",RHSWorkspace=i+"2dnorm_1",OutputWorkspace="den")
			Divide(LHSWorkspace="num",RHSWorkspace="den",OutputWorkspace=i+"2dpol")
			ReplaceSpecialValues(InputWorkspace=i+"2dpol",OutputWorkspace=i+"2dpol",NanValue=0.0,NaNError=0.0,InfinityValue=0.0,InfinityError=0.0)
		#DeleteWorkspace(i+"norm_2")
		#DeleteWorkspace(i+"norm_1")
		DeleteWorkspace("num")
		DeleteWorkspace("den")
		
	if existingP0 != "2":
		for i in P0nlist:
			ConvertUnits(InputWorkspace=i,OutputWorkspace=i,Target="Wavelength",AlignBins=1)
			Rebin(InputWorkspace=i,OutputWorkspace=i,Params=reb)
			removeoutlayer(i+"_1")
			removeoutlayer(i+"_2")
			CropWorkspace(InputWorkspace=i,OutputWorkspace=i+"mon",StartWorkspaceIndex=mon_spec,EndWorkspaceIndex=mon_spec)
			if int(maxSpec) > int(minSpec):
				SumSpectra(InputWorkspace=i,OutputWorkspace=i+"det",StartWorkspaceIndex=minSp,EndWorkspaceIndex=maxSp)
			else:
				CropWorkspace(InputWorkspace=i,OutputWorkspace=i+"det",StartWorkspaceIndex=minSp,EndWorkspaceIndex=maxSp)
			Divide(LHSWorkspace=i+"det",RHSWorkspace=i+"mon",OutputWorkspace=i+"norm")
			DeleteWorkspace(i+"mon")
			DeleteWorkspace(i+"det")
			DeleteWorkspace(i)
			Minus(LHSWorkspace=i+"norm_"+upPeriod,RHSWorkspace=i+"norm_"+downPeriod,OutputWorkspace="num")
			Plus(LHSWorkspace=i+"norm_2",RHSWorkspace=i+"norm_1",OutputWorkspace="den")
			Divide(LHSWorkspace="num",RHSWorkspace="den",OutputWorkspace=i+"pol")
			ReplaceSpecialValues(InputWorkspace=i+"pol",OutputWorkspace=i+"pol",NanValue=0.0,NaNError=0.0,InfinityValue=0.0,InfinityError=0.0)
			DeleteWorkspace(i+"norm_2")
			DeleteWorkspace(i+"norm_1")
			DeleteWorkspace("num")
			DeleteWorkspace("den")
		
	for i in range(len(nlist)):
		if existingP0 != "2":
			Divide(LHSWorkspace=nlist[i]+"pol",RHSWorkspace=P0nlist[i]+"pol",OutputWorkspace=nlist[i]+"SESANS")
			if nspec > 4 and minSp != 3:
				Divide(LHSWorkspace=nlist[i]+"2dpol",RHSWorkspace=P0nlist[i]+"pol",OutputWorkspace=nlist[i]+"2dSESANS")
		else:
			Divide(LHSWorkspace=nlist[i]+"pol",RHSWorkspace=P0nlist[i],OutputWorkspace=nlist[i]+"SESANS")
			if nspec > 4 and minSp != 3:
				Divide(LHSWorkspace=nlist[i]+"2dpol",RHSWorkspace=P0nlist[i],OutputWorkspace=nlist[i]+"2dSESANS")
		ReplaceSpecialValues(InputWorkspace=nlist[i]+"SESANS",OutputWorkspace=nlist[i]+"SESANS",NanValue=0.0,NaNError=0.0,InfinityValue=0.0,InfinityError=0.0)
	
	SEConstList=parseNameList(SEConstants)
	k=0
	for i in nlist:
		if lnPOverLam == "2":
			CloneWorkspace(InputWorkspace=i+"SESANS",OutputWorkspace=i+"SESANS_P")
		a1=mtd[i+"SESANS"]
		x=numpy.array(a1.readX(0))
                new_y = numpy.array(a1.dataY(0))
                new_e = numpy.array(a1.dataE(0))

		for j in range(len(x)-1):
			lam=((a1.readX(0)[j]+a1.readX(0)[j+1])/2.0)/10.0
			p=a1.readY(0)[j]
			e=a1.readE(0)[j]
			if lnPOverLam == "2":
				if p > 0.0:
					new_y[j]=log(p)/((lam)**2)
					new_e(0)[j]=(e/p)/((lam)**2)
				else:
					new_y(0)[j]=0.0
					new_e(0)[j]=0.0
		for j in range(len(x)):
			if convertToSEL == "2":
				lam=a1.readX(0)[j]
				x[j]=1.0e-2*float(SEConstList[k])*lam*lam
				#print str(lam)+" "+str(1.0e-2*float(SEConstList[k])*lam*lam)
                a1.setY(0, new_y)
                a1.setE(0, new_e)
                a1.setX(0, x)
		k=k+1

	
	if nspec > 4 and minSp != 3:
		k=0
		for i in nlist:
			if lnPOverLam == "2":
				CloneWorkspace(InputWorkspace=i+"2dSESANS",OutputWorkspace=i+"2dSESANS_P")
			a1=mtd[i+"2dSESANS"]
			nspec=a1.getNumberHistograms()
			for l in range(nspec):
				x = numpy.array(a1.readX(l))
                                new_y = numpy.array(a1.readY(l))
                                new_e = numpy.array(a1.readE(l))
				for j in range(len(x)-1):
					lam=((a1.readX(l)[j]+a1.readX(l)[j+1])/2.0)/10.0
					p=a1.readY(l)[j]
					e=a1.readE(l)[j]
					if lnPOverLam == "2":
						if p > 0.0:
							new_y[j]=log(p)/((lam*1.0e-9)**2)
							new_e[j]=(e/p)/((lam*1.0e-9)**2)
						else:
							new_y[j]=0.0
							new_e[j]=0.0
				for j in range(len(x)):
					if convertToSEL == "2":
						lam=a1.readX(l)[j]                                                
						x[j]=1.0e-2*float(SEConstList[k])*lam*lam
						#print str(lam)+" "+str(1.0e-2*float(SEConstList[k])*lam*lam)
                        a1.setY(l, new_y)
                        a1.setE(l, new_e)
                        a1.setX(l, x)
			k=k+1

#
#===========================================================
#
def nrCalcSEConst(RFFrequency,poleShoeAngle):
	if (RFFrequency=="0.5"):
		B=0.53*34.288
	elif (RFFrequency=="1.0"):
		B=34.288
	else:
		B=2.0*34.288
	
	h=6.62607e-34
	m=1.67493e-27
	L=1.0
	Gl=1.83247e8
	#
	# correct the angle
	# calibration of th0 using gold grating Dec 2010
	#
	th0=float(poleShoeAngle)
	th0=-0.0000000467796*(th0**5)+0.0000195413*(th0**4)-0.00326229*(th0**3)+0.271767*(th0**2)-10.4269*th0+198.108
	c1=Gl*m*2.0*B*L/(2.0*pi*h*tan(th0*pi/180.0)*1.0e20)
	print c1*1e8
	return c1*1e8
#
#===========================================================
#
def nrSESANSP0Fn(P0runList,P0nameList,minSpec,maxSpec,upPeriod,downPeriod,gparams,diagnostics="0"):

	P0nlist=parseNameList(P0nameList)
	logger.notice("This is the P0nameslist:"+str(P0nlist))
	P0rlist=parseRunList(P0runList)
	logger.notice("This is the P0runlist:"+str(P0rlist))
	for i in range(len(P0rlist)):
		addRuns(P0rlist[i],P0nlist[i])

	mon_spec=int(gparams[3])-1
	minSp=int(minSpec)-1
	maxSp=int(maxSpec)-1
	reb=gparams[0]+","+gparams[1]+","+gparams[2]
	if len(gparams) == 5:
		mapfile=gparams[4]

	for i in P0nlist:
		a1=mtd[i+"_1"]
		nspec=a1.getNumberHistograms()
		if nspec == 1030 and minSp != 3:
			GroupDetectors(InputWorkspace=i,OutputWorkspace=i,MapFile=mapfile)
		ConvertUnits(InputWorkspace=i,OutputWorkspace=i,Target="Wavelength",AlignBins=1)
		Rebin(InputWorkspace=i,OutputWorkspace=i,Params=reb)
		CropWorkspace(InputWorkspace=i,OutputWorkspace=i+"mon",StartWorkspaceIndex=mon_spec,EndWorkspaceIndex=mon_spec)
		if int(maxSpec) > int(minSpec):
			SumSpectra(InputWorkspace=i,OutputWorkspace=i+"det",StartWorkspaceIndex=minSp,EndWorkspaceIndex=maxSp)
		else:
			CropWorkspace(InputWorkspace=i,OutputWorkspace=i+"det",StartWorkspaceIndex=minSp,EndWorkspaceIndex=maxSp)
		Divide(LHSWorkspace=i+"det",RHSWorkspace=i+"mon",OutputWorkspace=i+"norm")
		if (diagnostics=="0"):
			DeleteWorkspace(i+"mon")
			DeleteWorkspace(i+"det")
			DeleteWorkspace(i)
		Minus(LHSWorkspace=i+"norm_"+upPeriod,RHSWorkspace=i+"norm_"+downPeriod,OutputWorkspace="num")
		Plus(LHSWorkspace=i+"norm_2",RHSWorkspace=i+"norm_1",OutputWorkspace="den")
		Divide(LHSWorkspace="num",RHSWorkspace="den",OutputWorkspace=i+"pol")
		ReplaceSpecialValues(InputWorkspace=i+"pol",OutputWorkspace=i+"pol",NanValue=0.0,NaNError=0.0,InfinityValue=0.0,InfinityError=0.0)
		if (diagnostics=="0"):
			DeleteWorkspace(i+"norm_2")
			DeleteWorkspace(i+"norm_1")
			DeleteWorkspace("num")
			DeleteWorkspace("den")
#
#===========================================================
#
def nrSERGISFn(runList,nameList,P0runList,P0nameList,incidentAngles,SEConstants,specChan,minSpec,maxSpec,upPeriod,downPeriod,existingP0,gparams,lnPOverLam):
	nlist=parseNameList(nameList)
	logger.notice("This is the sample nameslist:"+str(nlist))
	rlist=parseRunList(runList)
	logger.notice("This is the sample runlist:"+str(rlist))
	incAngles=parseNameList(incidentAngles)
	logger.notice("This incident Angles are:"+str(incAngles))

	for i in range(len(rlist)):
		addRuns(rlist[i],nlist[i])

	P0nlist=parseNameList(P0nameList)
	logger.notice("This is the P0nameslist:"+str(P0nlist))
	if existingP0 != "2":
		P0rlist=parseRunList(P0runList)
		logger.notice("This is the P0runlist:"+str(P0rlist))
		for i in range(len(P0rlist)):
			addRuns(P0rlist[i],P0nlist[i])

	mon_spec=int(gparams[3])-1
	minSp=int(minSpec)-1
	maxSp=int(maxSpec)-1
	reb=gparams[0]+","+gparams[1]+","+gparams[2]
	
	k=0
	for i in nlist:
		for j in range(2):
			wksp=i+"_"+pnums[j]
			ConvertUnits(InputWorkspace=wksp,OutputWorkspace=wksp,Target="Wavelength",AlignBins=1)
			Rebin(InputWorkspace=wksp,OutputWorkspace=wksp,Params=reb)
			CropWorkspace(InputWorkspace=wksp,OutputWorkspace=wksp+"mon",StartWorkspaceIndex=mon_spec,EndWorkspaceIndex=mon_spec)
			a1=mtd[wksp]
			nspec=a1.getNumberHistograms()
			if nspec == 4:
				CropWorkspace(InputWorkspace=wksp,OutputWorkspace=wksp+"det",StartWorkspaceIndex=3,EndWorkspaceIndex=3)
				RotateInstrumentComponent(wksp+"det","DetectorBench",X="-1.0",Angle=str(2.0*float(incAngles[k])))
				Divide(LHSWorkspace=wksp+"det",RHSWorkspace=wksp+"mon",OutputWorkspace=wksp+"norm")
			else:
				CropWorkspace(InputWorkspace=wksp,OutputWorkspace=wksp+"det",StartWorkspaceIndex=4,EndWorkspaceIndex=243)
				# move the first spectrum in the list onto the beam centre so that when the bench is rotated it's in the right place
				MoveInstrumentComponent(wksp+"det","DetectorBench",Y=str((125.0-float(minSpec))*1.2e-3))
				# add a bit to the angle to put the first spectrum of the group in the right place
				a1=2.0*float(incAngles[k])+atan((float(minSpec)-float(specChan))*1.2e-3/3.53)*180.0/pi
				#print str(2.0*float(incAngles[k]))+" "+str(atan((float(minSpec)-float(specChan))*1.2e-3/3.63)*180.0/pi)+" "+str(a1)
				RotateInstrumentComponent(wksp+"det","DetectorBench",X="-1.0",Angle=str(a1))
				GroupDetectors(InputWorkspace=wksp+"det",OutputWorkspace=wksp+"sum",WorkspaceIndexList=range(int(minSpec)-5,int(maxSpec)-5+1),KeepUngroupedSpectra="0")
				Divide(LHSWorkspace=wksp+"sum",RHSWorkspace=wksp+"mon",OutputWorkspace=wksp+"norm")
				Divide(LHSWorkspace=wksp+"det",RHSWorkspace=wksp+"mon",OutputWorkspace=wksp+"detnorm")
				floodnorm(wksp+"detnorm",floodfile)
				DeleteWorkspace(wksp+"sum")

			DeleteWorkspace(wksp+"mon")
			DeleteWorkspace(wksp+"det")
			DeleteWorkspace(wksp)
			
		Minus(LHSWorkspace=i+"_"+upPeriod+"norm",RHSWorkspace=i+"_"+downPeriod+"norm",OutputWorkspace="num")
		Plus(LHSWorkspace=i+"_1norm",RHSWorkspace=i+"_2norm",OutputWorkspace="den")
		Divide(LHSWorkspace="num",RHSWorkspace="den",OutputWorkspace=i+"pol")
		ReplaceSpecialValues(InputWorkspace=i+"pol",OutputWorkspace=i+"pol",NanValue=0.0,NaNError=0.0,InfinityValue=0.0,InfinityError=0.0)
		DeleteWorkspace(i+"_1norm")
		DeleteWorkspace(i+"_2norm")
		DeleteWorkspace("num")
		DeleteWorkspace("den")

		if nspec != 4:
			Minus(LHSWorkspace=i+"_"+upPeriod+"detnorm",RHSWorkspace=i+"_"+downPeriod+"detnorm",OutputWorkspace="num")
			Plus(LHSWorkspace=i+"_1detnorm",RHSWorkspace=i+"_2detnorm",OutputWorkspace="den")
			Divide(LHSWorkspace="num",RHSWorkspace="den",OutputWorkspace=i+"2dpol")
			ReplaceSpecialValues(InputWorkspace=i+"2dpol",OutputWorkspace=i+"2dpol",NanValue=0.0,NaNError=0.0,InfinityValue=0.0,InfinityError=0.0)
			DeleteWorkspace(i+"_1detnorm")
			DeleteWorkspace(i+"_2detnorm")
			DeleteWorkspace("num")
			DeleteWorkspace("den")
		
	if existingP0 != "2":
		for i in P0nlist:
			ConvertUnits(InputWorkspace=i,OutputWorkspace=i,Target="Wavelength",AlignBins=1)
			Rebin(InputWorkspace=i,OutputWorkspace=i,Params=reb)
			CropWorkspace(InputWorkspace=i,OutputWorkspace=i+"mon",StartWorkspaceIndex=mon_spec,EndWorkspaceIndex=mon_spec)
			if int(maxSpec) > int(minSpec):
				SumSpectra(InputWorkspace=i,OutputWorkspace=i+"det",StartWorkspaceIndex=minSp,EndWorkspaceIndex=maxSp)
			else:
				CropWorkspace(InputWorkspace=i,OutputWorkspace=i+"det",StartWorkspaceIndex=minSp,EndWorkspaceIndex=maxSp)
			Divide(LHSWorkspace=i+"det",RHSWorkspace=i+"mon",OutputWorkspace=i+"norm")
			DeleteWorkspace(i+"mon")
			DeleteWorkspace(i+"det")
			DeleteWorkspace(i)
			Minus(LHSWorkspace=i+"norm_"+upPeriod,RHSWorkspace=i+"norm_"+downPeriod,OutputWorkspace="num")
			Plus(LHSWorkspace=i+"norm_2",RHSWorkspace=i+"norm_1",OutputWorkspace="den")
			Divide(LHSWorkspace="num",RHSWorkspace="den",OutputWorkspace=i+"pol")
			ReplaceSpecialValues(InputWorkspace=i+"pol",OutputWorkspace=i+"pol",NanValue=0.0,NaNError=0.0,InfinityValue=0.0,InfinityError=0.0)
			DeleteWorkspace(i+"norm_2")
			DeleteWorkspace(i+"norm_1")
			DeleteWorkspace("num")
			DeleteWorkspace("den")
		
	for i in range(len(nlist)):
		if existingP0 != "2":
			Divide(LHSWorkspace=nlist[i]+"pol",RHSWorkspace=P0nlist[i]+"pol",OutputWorkspace=nlist[i]+"SESANS")
		else:
			Divide(LHSWorkspace=nlist[i]+"pol",RHSWorkspace=P0nlist[i]+"pol",OutputWorkspace=nlist[i]+"SESANS")
		ReplaceSpecialValues(InputWorkspace=nlist[i]+"SESANS",OutputWorkspace=nlist[i]+"SESANS",NanValue=0.0,NaNError=0.0,InfinityValue=0.0,InfinityError=0.0)
	
	SEConstList=parseNameList(SEConstants)
	k=0
	for i in nlist:
		a1=mtd[i+"SESANS"]
		lam = ((a1.readX(0)[1:] + a1.readX(0)[:-1])/2.0)/10.0
		p = a1.readY(0)
		a1.setY(0, numpy.log(p)/((lam*1.0e-8)**2) )
		a1.setX(0, 1.0e-2*float(SEConstList[k])*lam*lam)
		k=k+1
#
#===========================================================
#
def nrNRFn(runList,nameList,incidentAngles,DBList,specChan,minSpec,maxSpec,gparams,floodfile,subbgd=0,qgroup=0,dofloodnorm=1,diagnostics=0):
	nlist=parseNameList(nameList)
	#logger.notice("This is the sample nameslist:"+str(nlist))
	rlist=parseRunList(runList)
	#logger.notice("This is the sample runlist:"+str(rlist))
	dlist=parseNameList(DBList)
	#logger.notice("This is the Direct Beam nameslist:"+str(dlist))
	incAngles=parseNameList(incidentAngles)
	#logger.notice("This incident Angles are:"+str(incAngles))

	for i in range(len(rlist)):
		addRuns(rlist[i],nlist[i])
	
	mon_spec=int(gparams[3])-1
	reb=gparams[0]+","+gparams[1]+","+gparams[2]
	
	k=0
	for i in nlist:
		if isinstance(mtd[i], WorkspaceGroup):
			#RenameWorkspace(i+"_1",i)
			snames=mtd[i].getNames()
			Plus(LHSWorkspace=i+"_1",RHSWorkspace=i+"_2",OutputWorkspace="wtemp")
			if len(snames) > 2:
				for j in range(2,len(snames)-1):
					Plus(LHSWorkspace="wtemp",RHSWorkspace=snames[j],OutputWorkspace="wtemp")
			for j in snames:
				DeleteWorkspace(j)
			RenameWorkspace(InputWorkspace="wtemp",OutputWorkspace=i)
		ConvertUnits(InputWorkspace=i,OutputWorkspace=i,Target="Wavelength",AlignBins="1")
		a1=mtd[i]
		nspec=a1.getNumberHistograms()
		if nspec == 4:
			Rebin(InputWorkspace=i,OutputWorkspace=i,Params=reb)
			CropWorkspace(InputWorkspace=i,OutputWorkspace=i+"mon",StartWorkspaceIndex=mon_spec,EndWorkspaceIndex=mon_spec)
			CropWorkspace(InputWorkspace=i,OutputWorkspace=i+"det",StartWorkspaceIndex=3,EndWorkspaceIndex=3)
			RotateInstrumentComponent(i+"det","DetectorBench",X="-1.0",Angle=str(2.0*float(incAngles[k])))
			Divide(LHSWorkspace=i+"det",RHSWorkspace=i+"mon",OutputWorkspace=i+"norm")
			if dlist[k] != "none":
				Divide(LHSWorkspace=i+"norm",RHSWorkspace=dlist[k],OutputWorkspace=i+"norm")
				ReplaceSpecialValues(InputWorkspace=i+"norm",OutputWorkspace=i+"norm",NanValue=0.0,NaNError=0.0,InfinityValue=0.0,InfinityError=0.0)
			ConvertUnits(InputWorkspace=i+"norm",OutputWorkspace=i+"RvQ",Target="MomentumTransfer")
		else:
			# Rebin using internal parameters to avoid problems with summing in Q
			#internalreb=gparams[0]+",0.01,"+gparams[2]
			#Rebin(InputWorkspace=i,OutputWorkspace=i,Params=internalreb)
			minSp=int(minSpec)
			maxSp=int(maxSpec)
			CropWorkspace(InputWorkspace=i,OutputWorkspace=i+"det",StartWorkspaceIndex=4,EndWorkspaceIndex=243)
			if(dofloodnorm==1):
				floodnorm(i+"det",floodfile)
			# move the first spectrum in the list onto the beam centre so that when the bench is rotated it's in the right place
			MoveInstrumentComponent(i+"det","DetectorBench",Y=str((125.0-float(minSpec))*1.2e-3))
			# add a bit to the angle to put the first spectrum of the group in the right place
			a1=2.0*float(incAngles[k])+atan((float(minSpec)-float(specChan))*1.2e-3/3.53)*180.0/pi
			#print str(2.0*float(incAngles[k]))+" "+str(atan((float(minSpec)-float(specChan))*1.2e-3/3.63)*180.0/pi)+" "+str(a1)
			RotateInstrumentComponent(i+"det","DetectorBench",X="-1.0",Angle=str(a1))
			if (subbgd==1):
				# Calculate a background correction
				GroupDetectors(i+"det",OutputWorkspace=i+"bgd2",WorkspaceIndexList=range(0,50),KeepUngroupedSpectra="0")
				GroupDetectors(i+"det",OutputWorkspace=i+"bgd1",WorkspaceIndexList=range(160,240),KeepUngroupedSpectra="0")
				Plus(i+"bgd1",i+"bgd2",OutputWorkspace=i+"bgd")
				wbgdtemp=mtd[i+"bgd"]/130.0
				DeleteWorkspace(i+"bgd1")
				DeleteWorkspace(i+"bgd2")
				DeleteWorkspace(i+"bgd")
				# Subract a per spectrum background
				Minus(i+"det",wbgdtemp,OutputWorkspace=i+"det")
				if(diagnostics==0):
					DeleteWorkspace("wbgdtemp")
# Experimental convert to Q before summing 
			if (qgroup==1):
				Rebin(InputWorkspace=i+"det",OutputWorkspace=i+"det",Params=reb)
				CropWorkspace(InputWorkspace=i+"det",OutputWorkspace=i+"detQ",StartWorkspaceIndex=int(minSpec)-5,EndWorkspaceIndex=int(maxSpec)-5+1)
				ConvertUnits(InputWorkspace=i+"detQ",OutputWorkspace=i+"detQ",Target="MomentumTransfer",AlignBins="1")
				GroupDetectors(i+"detQ",OutputWorkspace=i+"sum",WorkspaceIndexList=range(0,int(maxSpec)-int(minSpec)),KeepUngroupedSpectra="0")
				ConvertUnits(InputWorkspace=i+"sum",OutputWorkspace=i+"sum",Target="Wavelength",AlignBins="1")
				Rebin(InputWorkspace=i+"sum",OutputWorkspace=i+"sum",Params=reb)
				CropWorkspace(InputWorkspace=i,OutputWorkspace=i+"mon",StartWorkspaceIndex=mon_spec,EndWorkspaceIndex=mon_spec)
				Rebin(InputWorkspace=i+"mon",OutputWorkspace=i+"mon",Params=reb)
				Rebin(InputWorkspace=i+"det",OutputWorkspace=i+"det",Params=reb)
				DeleteWorkspace(i+"detQ")
			else:
				CropWorkspace(InputWorkspace=i,OutputWorkspace=i+"mon",StartWorkspaceIndex=mon_spec,EndWorkspaceIndex=mon_spec)
				Rebin(InputWorkspace=i+"mon",OutputWorkspace=i+"mon",Params=reb)
				Rebin(InputWorkspace=i+"det",OutputWorkspace=i+"det",Params=reb)
				GroupDetectors(InputWorkspace=i+"det",OutputWorkspace=i+"sum",WorkspaceIndexList=range(int(minSpec)-5,int(maxSpec)-5+1),KeepUngroupedSpectra="0")
			Divide(LHSWorkspace=i+"sum",RHSWorkspace=i+"mon",OutputWorkspace=i+"norm")
			Divide(LHSWorkspace=i+"det",RHSWorkspace=i+"mon",OutputWorkspace=i+"detnorm")
			if dlist[k]  == "none":
				a1=0
			elif dlist[k] == "function":
				# polynomial + power law corrections based on Run numbers 8291 and 8292
				Divide(LHSWorkspace=i+'norm',RHSWorkspace=i+'norm',OutputWorkspace=i+'normt1')
				PolynomialCorrection(InputWorkspace=i+'normt1',OutputWorkspace=i+'normPC',Coefficients='-0.0177398,0.00101695,0.0',Operation='Multiply')
				PowerLawCorrection(InputWorkspace=i+'normt1',OutputWorkspace=i+'normPLC',C0='2.01332',C1='-1.8188')
				Plus(LHSWorkspace=i+'normPC',RHSWorkspace=i+'normPLC',OutputWorkspace=i+'normt1')
				Divide(LHSWorkspace=i+'norm',RHSWorkspace=i+'normt1',OutputWorkspace=i+'norm')
				ReplaceSpecialValues(InputWorkspace=i+'norm',OutputWorkspace=i+'norm',NanValue=0.0,NaNError=0.0,InfinityValue=0.0,InfinityError=0.0)
				DeleteWorkspace(i+'normPC')
				DeleteWorkspace(i+'normPLC')
				DeleteWorkspace(i+'normt1')
			else:
				Divide(LHSWorkspace=i+"norm",RHSWorkspace=dlist[k],OutputWorkspace=i+"norm")
				ReplaceSpecialValues(InputWorkspace=i+"norm",OutputWorkspace=i+"norm",NanValue=0.0,NaNError=0.0,InfinityValue=0.0,InfinityError=0.0)
				Divide(LHSWorkspace=i+"detnorm",RHSWorkspace=dlist[k],OutputWorkspace=i+"detnorm")
				ReplaceSpecialValues(InputWorkspace=i+"detnorm",OutputWorkspace=i+"detnorm",NanValue=0.0,NaNError=0.0,InfinityValue=0.0,InfinityError=0.0)
			ConvertUnits(InputWorkspace=i+"norm",OutputWorkspace=i+"RvQ",Target="MomentumTransfer")
			#floodnorm(i+"detnorm",floodfile)
			DeleteWorkspace(i+"sum")
			
		k=k+1
		DeleteWorkspace(i)
		if(diagnostics==0):
			DeleteWorkspace(i+"mon")
			DeleteWorkspace(i+"det")

#
#===========================================================
#
def findbin(wksp,val):
	a1=mtd[wksp]
	x1=a1.readX(0)
	bnum=-1
	for i in range(len(x1)-1):
		if x1[i] > val:
			break
	return i-1
#
#===========================================================
#
def nrDBFn(runListShort,nameListShort,runListLong,nameListLong,nameListComb,minSpec,maxSpec,minWavelength,gparams,floodfile="",diagnostics="0"):
	nlistS=parseNameList(nameListShort)
	rlistS=parseRunList(runListShort)
	nlistL=parseNameList(nameListLong)
	rlistL=parseRunList(runListLong)
	nlistComb=parseNameList(nameListComb)

	for i in range(len(rlistS)):
		addRuns(rlistS[i],nlistS[i])
	for i in range(len(rlistL)):
		addRuns(rlistL[i],nlistL[i])
	
	mon_spec=int(gparams[3])-1
	minSp=int(minSpec)-1
	maxSp=int(maxSpec)-1
	reb=gparams[0]+","+gparams[1]+","+gparams[2]
	
	for i in nlistS:
		ConvertUnits(InputWorkspace=i,OutputWorkspace=i,Target="Wavelength",AlignBins="1")
		Rebin(InputWorkspace=i,OutputWorkspace=i,Params=reb)
		CropWorkspace(InputWorkspace=i,OutputWorkspace=i+"mon",StartWorkspaceIndex=mon_spec,EndWorkspaceIndex=mon_spec)
		if isinstance(mtd[i], GroupWorkspace):
			snames=mtd[i].getNames()
			a1=mtd[snames[0]]
		else:
			a1=mtd[i]
		
		nspec=a1.getNumberHistograms()
		
		if nspec == 4:
			CropWorkspace(InputWorkspace=i,OutputWorkspace=i+"det",StartWorkspaceIndex=3,EndWorkspaceIndex=3)
			Divide(i+"det",i+"mon",OutputWorkspace=i+"norm")
			ReplaceSpecialValues(i+"norm","0.0","0.0","0.0","0.0",OutputWorkspace=i+"norm")
		else:
			CropWorkspace(InputWorkspace=i,OutputWorkspace=i+"det",StartWorkspaceIndex=4,EndWorkspaceIndex=243)
			floodnorm(i+"det",floodfile)
			GroupDetectors(i+"det",OutputWorkspace=i+"sum",WorkspaceIndexList=range(int(minSpec)-5,int(maxSpec)-5+1),KeepUngroupedSpectra="0")
			Divide(i+"sum",i+"mon",OutputWorkspace=i+"norm")
			ReplaceSpecialValues(i+"norm","0.0","0.0","0.0","0.0", OutputWorkspace=i+"norm")
			
	for i in nlistL:
		ConvertUnits(InputWorkspace=i,OutputWorkspace=i,Target="Wavelength",AlignBins="1")
		Rebin(InputWorkspace=i,OutputWorkspace=i,Params=reb)
		CropWorkspace(InputWorkspace=i,OutputWorkspace=i+"mon",StartWorkspaceIndex=mon_spec,EndWorkspaceIndex=mon_spec)
		if isinstance(mtd[i], GroupWorkspace):
			lnames=mtd[i].getNames()
			a1=mtd[lnames[0]]
		else:
			a1=mtd[i]

		nspec=a1.getNumberHistograms()

		if nspec == 4:
			CropWorkspace(InputWorkspace=i,OutputWorkspace=i+"det",StartWorkspaceIndex=3,EndWorkspaceIndex=3)
			Divide(i+"det",i+"mon",OutputWorkspace=i+"norm")
			ReplaceSpecialValues(i+"norm","0.0","0.0","0.0","0.0",OutputWorkspace=i+"norm")
		else:
			CropWorkspace(InputWorkspace=i,OutputWorkspace=i+"det",StartWorkspaceIndex=4,EndWorkspaceIndex=243)
			floodnorm(i+"det",floodfile)
			GroupDetectors(i+"det",OutputWorkspace=i+"sum",WorkspaceIndexList=range(int(minSpec)-5,int(maxSpec)-5+1),KeepUngroupedSpectra="0")
			Divide(i+"sum",i+"mon",OutputWorkspace=i+"norm")
			ReplaceSpecialValues(i+"norm","0.0","0.0","0.0","0.0",OutputWorkspace=i+"norm")
		
	for i in range(len(nlistS)):
		if isinstance(mtd[nlistS[i]+"norm"], GroupWorkspace):
			snames=mtd[nlistS[i]+"norm"].getNames()
			lnames=mtd[nlistL[i]+"norm"].getNames()
			for k in range(len(snames)):
				Integration(snames[k],minWavelength,gparams[2], OutputWorkspace=snames[k]+"int")
				Integration(lnames[k],minWavelength,gparams[2], OutputWorkspace=lnames[k]+"int")
				Multiply(snames[k],lnames[k]+"int",OutputWorkspace=snames[k])
				Divide(snames[k],snames[k]+"int",OutputWorkspace=snames[k])
				a1=findbin(lnames[k],float(minWavelength))
				MultiplyRange(lnames[k],"0",str(a1),"0.0",OutputWorkspace=lnames[k])
				WeightedMean(snames[k],nlistComb[i]+"_"+str(k+1),OutputWorkspace=lnames[k])
				if (diagnostics=="0"):
					DeleteWorkspace(snames[k]+"int")
					DeleteWorkspace(lnames[k]+"int")
		else:
			Integration(nlistS[i]+"norm",minWavelength,gparams[2],OutputWorkspace=nlistS[i]+"int")
			Integration(nlistL[i]+"norm",minWavelength,gparams[2],OutputWorkspace=nlistL[i]+"int")
			Multiply(nlistS[i]+"norm",nlistL[i]+"int",OutputWorkspace=nlistS[i]+"norm")
			Divide(nlistS[i]+"norm",nlistS[i]+"int",OutputWorkspace=nlistS[i]+"norm")
			a1=findbin(nlistL[i]+"norm",float(minWavelength))
			MultiplyRange(nlistL[i]+"norm","0",str(a1),"0.0", OutputWorkspace=nlistL[i]+"norm")
			WeightedMean(nlistS[i]+"norm",nlistL[i]+"norm", OutputWorkspace=nlistComb[i])
			if (diagnostics=="0"):
				DeleteWorkspace(nlistS[i]+"int")
				DeleteWorkspace(nlistL[i]+"int")

			if (diagnostics=="0"):
				DeleteWorkspace(nlistS[i]+"mon")
				DeleteWorkspace(nlistS[i]+"det")
				if nspec != 4:
					DeleteWorkspace(nlistS[i]+"sum")
				DeleteWorkspace(nlistS[i]+"norm")
				DeleteWorkspace(nlistS[i])
				DeleteWorkspace(nlistL[i]+"mon")
				DeleteWorkspace(nlistL[i]+"det")
				if nspec != 4:
					DeleteWorkspace(nlistL[i]+"sum")
				DeleteWorkspace(nlistL[i]+"norm")
				DeleteWorkspace(nlistL[i])
		
#
#===========================================================
#
def numberofbins(wksp):
	a1=mtd[wksp]
	y1=a1.readY(0)
	return len(y1)-1
#
#===========================================================
#
def maskbin(wksp,val):
	a1=mtd[wksp]
	x1=a1.readX(0)
	for i in range(len(x1)-1):
		if x1[i] > val:
			break
	a1.dataY(0)[i-1]=0.0
	a1.dataE(0)[i-1]=0.0
#
#===========================================================
#
def arr2list(iarray):
	# convert array of strings to a single string with commas
	res=""
	for i in range(len(iarray)-1):
		res=res+iarray[i]+","
	res=res+iarray[len(iarray)-1]
	return res
#
#===========================================================
#
def NRCombineDatafn(RunsNameList,CombNameList,applySFs,SFList,SFError,scaleOption,bparams,globalSF,applyGlobalSF,diagnostics=0):
	qmin=bparams[0]
	bin=bparams[1]
	qmax=bparams[2]
	rlist=parseNameList(RunsNameList)
	listsfs=parseNameList(SFList)
	listsfserr=parseNameList(SFError)
	sfs=[]
	sferrs=[]
	for i in rlist:
		Rebin(i,qmin+","+bin+","+qmax,OutputWorkspace=i+"reb")
	# find the overlap ranges
	bol=[] #beginning of overlaps
	eol=[] #end of overlaps
	for i in range(len(rlist)-1):
		a1=mtd[rlist[i+1]]
		x=a1.readX(0)
		bol.append(x[0])
		a1=mtd[rlist[i]]
		x=a1.readX(0)
		eol.append(x[len(x)-1])
	# set the edges of the rebinned data to 0.0 to avoid partial bin problems
	maskbin(rlist[0]+"reb",eol[0])
	if len(rlist) > 2:
		for i in range(1,len(rlist)-1):
			maskbin(rlist[i]+"reb",bol[i-1])
			maskbin(rlist[i]+"reb",eol[i])
	maskbin(rlist[len(rlist)-1]+"reb",bol[len(rlist)-2])
	# Now find the various scale factors and store in temp workspaces
	for i in range(len(rlist)-1):
		Integration(rlist[i]+"reb",str(bol[i]),str(eol[i]), OutputWorkspace="i"+str(i)+"1temp")
		Integration(rlist[i+1]+"reb",str(bol[i]),str(eol[i]), OutputWorkspace="i"+str(i)+"2temp")
		if scaleOption != "2":
			Divide("i"+str(i)+"1temp","i"+str(i)+"2temp",OutputWorkspace="sf"+str(i))
			a1=mtd["sf"+str(i)]
			print "sf"+str(i)+"="+str(a1.readY(0))+" +/- "+str(a1.readE(0))
			sfs.append(str(a1.readY(0)[0]))
			sferrs.append(str(a1.readE(0)[0]))
		else:
			Divide("i"+str(i)+"2temp","i"+str(i)+"1temp",OutputWorkspace="sf"+str(i))
			print "sf"+str(i)+"="+str(a1.readY(0))+" +/- "+str(a1.readE(0))
			sfs.append(str(a1.readY(0)[0]))
			sferrs.append(str(a1.readE(0)[0]))
		DeleteWorkspace("i"+str(i)+"1temp")
		DeleteWorkspace("i"+str(i)+"2temp")
	# if applying pre-defined scale factors substitute the given values now 
	# Note the errors are now set to 0
	if applySFs == "2":
		for i in range(len(rlist)-1):
			a1=mtd["sf"+str(i)]
			a1.setY(0, float(listsfs[i]))
			a1.setE(0, float(listsfserr[i]))
	# Now scale the various data sets in the correct order
	if scaleOption != "2":
		for i in range(len(rlist)-1):
			for j in range(i+1,len(rlist)):
				Multiply(rlist[j]+"reb","sf"+str(i),OutputWorkspace=rlist[j]+"reb")
	else:
		for i in range(len(rlist)-1,0,-1):
			for j in range(i,0,-1):
				Multiply(rlist[j]+"reb","sf"+str(i-1),OutputWorkspace=rlist[j]+"reb")

	WeightedMean(rlist[0]+"reb",rlist[1]+"reb",OutputWorkspace="currentSum")
	if len(rlist) > 2:
		for i in range(2,len(rlist)):
			WeightedMean("currentSum",rlist[i]+"reb",OutputWorkspace="currentSum")
	
	# if applying a global scale factor do it here
	if applyGlobalSF == "2":
		scaledData=mtd['currentSum']/float(globalSF)
		RenameWorkspace('scaledData',OutputWorkspace=CombNameList)
		DeleteWorkspace('currentSum')
	else:
		RenameWorkspace('currentSum',OutputWorkspace=CombNameList)
	for i in range(len(rlist)-1):
		DeleteWorkspace("sf"+str(i))
	if (diagnostics==0):
		for i in range(len(rlist)):
			DeleteWorkspace(rlist[i]+"reb")
	return [arr2list(sfs),arr2list(sferrs)] 
	
#
#===========================================================
#
def nrWriteXYE(wksp,fname):
	a1=mtd[wksp]
	x1=a1.readX(0)
	X1=n.zeros((len(x1)-1))
	for i in range(0,len(x1)-1):
		X1[i]=(x1[i]+x1[i+1])/2.0
	y1=a1.readY(0)
	e1=a1.readE(0)
	f=open(fname,'w')
	for i in range(len(X1)):
		s=""
		s+="%f," % X1[i]
		s+="%f," % y1[i]
		s+="%f\n" % e1[i]  
		f.write(s)
	f.close()
#
#===========================================================
#
def nrPNRCorrection(UpWksp,DownWksp,calibration=0):
#	crho=[0.941893,0.0234006,-0.00210536,0.0]
#	calpha=[0.945088,0.0242861,-0.00213624,0.0]
#	cAp=[1.00079,-0.0186778,0.00131546,0.0]
#	cPp=[1.01649,-0.0228172,0.00214626,0.0]
	# Constants Based on Runs 18350+18355 and 18351+18356 analyser theta at -0.1deg 
	# 2 RF Flippers as the polarising system
	if (calibration == 0):
		crho=[1.006831,-0.011467,0.002244,-0.000095]
		calpha=[1.017526,-0.017183,0.003136,-0.000140]
		cAp=[0.917940,0.038265,-0.006645,0.000282]
		cPp=[0.972762,0.001828,-0.000261,0.0]
	elif (calibration == 1):
	# Constants Based on Runs 19438-19458 and 19439+19459 
	# Drabkin on incident side RF Flipper on analyser side, Dec 2012
		crho=[0.970257,0.016127,-0.002318,0.000090]
		calpha=[0.975722,0.012464,-0.002408,0.000105]
		cAp=[1.030894,-0.040847,0.006069,-0.000247]
		cPp=[0.961900,-0.003722,0.001094,-0.000057]
	elif (calibration == 2):
	# Constants Based on Runs 19628-19656 and 19660-19670 analyser -0.2deg
	# RF Flippers on polariser and analyser side Feb 2013
		crho=[0.945927,0.025421,-0.003647,0.000156]
		calpha=[0.940769,0.027250,-0.003848,0.000164]
		cAp=[0.974374,-0.005334,0.001313,-0.000115]
		cPp=[1.023141,-0.024548,0.003398,-0.000134]
	elif (calibration == 3):
	# Constants Based on Runs 19628-19656 and 19660-19670 analyser -0.1deg
	# RF Flippers on polariser and analyser side Feb 2013
		crho=[0.955384,0.021501,-0.002962,0.000112]
		calpha=[0.957789,0.019995,-0.002697,0.000099]
		cAp=[0.986906,-0.013945,0.002480,-0.000161]
		cPp=[0.999517,-0.013878,0.001680,-0.000043]

	Ip = mtd[UpWksp]
	Ia = mtd[DownWksp]
	CloneWorkspace(Ip,OutputWorkspace="PCalpha")
	CropWorkspace(InputWorkspace="PCalpha",OutputWorkspace="PCalpha",StartWorkspaceIndex="0",EndWorkspaceIndex="0")
	PCalpha=(mtd['PCalpha']*0.0)+1.0
	alpha=mtd['PCalpha']
	# a1=alpha.readY(0)
	# for i in range(0,len(a1)):
		# alpha.dataY(0)[i]=0.0
		# alpha.dataE(0)[i]=0.0
	CloneWorkspace("PCalpha",OutputWorkspace="PCrho")
	CloneWorkspace("PCalpha",OutputWorkspace="PCAp")
	CloneWorkspace("PCalpha",OutputWorkspace="PCPp")
	rho=mtd['PCrho']
	Ap=mtd['PCAp']
	Pp=mtd['PCPp']
	# for i in range(0,len(a1)):
		# x=(alpha.dataX(0)[i]+alpha.dataX(0)[i])/2.0
		# for j in range(0,4):
			# alpha.dataY(0)[i]=alpha.dataY(0)[i]+calpha[j]*x**j
			# rho.dataY(0)[i]=rho.dataY(0)[i]+crho[j]*x**j
			# Ap.dataY(0)[i]=Ap.dataY(0)[i]+cAp[j]*x**j
			# Pp.dataY(0)[i]=Pp.dataY(0)[i]+cPp[j]*x**j
	PolynomialCorrection(InputWorkspace="PCalpha",OutputWorkspace="PCalpha",Coefficients=calpha,Operation="Multiply")
	PolynomialCorrection(InputWorkspace="PCrho",OutputWorkspace="PCrho",Coefficients=crho,Operation="Multiply")
	PolynomialCorrection(InputWorkspace="PCAp",OutputWorkspace="PCAp",Coefficients=cAp,Operation="Multiply")
	PolynomialCorrection(InputWorkspace="PCPp",OutputWorkspace="PCPp",Coefficients=cPp,Operation="Multiply")
	D=Pp*(1.0+rho)
	nIp=(Ip*(rho*Pp+1.0)+Ia*(Pp-1.0))/D
	nIa=(Ip*(rho*Pp-1.0)+Ia*(Pp+1.0))/D
	RenameWorkspace(nIp,OutputWorkspace=str(Ip)+"corr")
	RenameWorkspace(nIa,OutputWorkspace=str(Ia)+"corr")
	iwksp=mtd.getObjectNames()
	list_n=[str(Ip),str(Ia),"PCalpha","PCrho","PCAp","PCPp","1_p"]
	for i in range(len(iwksp)):
		for j in list_n:
			lname=len(j)
			if iwksp[i] [0:lname+1] == j+"_":
				DeleteWorkspace(iwksp[i])
	DeleteWorkspace("PCalpha")
	DeleteWorkspace("PCrho")
	DeleteWorkspace("PCAp")
	DeleteWorkspace("PCPp")
	DeleteWorkspace("D")
#
#===========================================================
#
def nrPACorrection(UpUpWksp,UpDownWksp,DownUpWksp,DownDownWksp,calibration=0):
#	crho=[0.941893,0.0234006,-0.00210536,0.0]
#	calpha=[0.945088,0.0242861,-0.00213624,0.0]
#	cAp=[1.00079,-0.0186778,0.00131546,0.0]
#	cPp=[1.01649,-0.0228172,0.00214626,0.0]
	# Constants Based on Runs 18350+18355 and 18351+18356 analyser theta at -0.1deg 
	# 2 RF Flippers as the polarising system
	if (calibration == 0):
		crho=[1.006831,-0.011467,0.002244,-0.000095]
		calpha=[1.017526,-0.017183,0.003136,-0.000140]
		cAp=[0.917940,0.038265,-0.006645,0.000282]
		cPp=[0.972762,0.001828,-0.000261,0.0]
	elif (calibration == 1):
	# Constants Based on Runs 19438-19458 and 19439+19459 
	# Drabkin on incident side RF Flipper on analyser side Dec 2012
		crho=[0.970257,0.016127,-0.002318,0.000090]
		calpha=[0.975722,0.012464,-0.002408,0.000105]
		cAp=[1.030894,-0.040847,0.006069,-0.000247]
		cPp=[0.961900,-0.003722,0.001094,-0.000057]
	elif (calibration == 2):
	# Constants Based on Runs 19628-19656 and 19660-19670 analyser -0.2deg
	# RF Flippers on polariser and analyser side Feb 2013
		crho=[0.945927,0.025421,-0.003647,0.000156]
		calpha=[0.940769,0.027250,-0.003848,0.000164]
		cAp=[0.974374,-0.005334,0.001313,-0.000115]
		cPp=[1.023141,-0.024548,0.003398,-0.000134]
	elif (calibration == 3):
	# Constants Based on Runs 19628-19656 and 19660-19670 analyser -0.1deg
	# RF Flippers on polariser and analyser side Feb 2013
		crho=[0.955384,0.021501,-0.002962,0.000112]
		calpha=[0.957789,0.019995,-0.002697,0.000099]
		cAp=[0.986906,-0.013945,0.002480,-0.000161]
		cPp=[0.999517,-0.013878,0.001680,-0.000043]
	
	Ipp = mtd[UpUpWksp]
	Ipa = mtd[UpDownWksp]
	Iap = mtd[DownUpWksp]
	Iaa = mtd[DownDownWksp]
	CloneWorkspace(Ipp,OutputWorkspace="PCalpha")
	CropWorkspace(InputWorkspace="PCalpha",OutputWorkspace="PCalpha",StartWorkspaceIndex="0",EndWorkspaceIndex="0")
	PCalpha=(mtd['PCalpha']*0.0)+1.0
	alpha=mtd['PCalpha']
	# a1=alpha.readY(0)
	# for i in range(0,len(a1)):
		# alpha.dataY(0)[i]=0.0
		# alpha.dataE(0)[i]=0.0
	CloneWorkspace("PCalpha",OutputWorkspace="PCrho")
	CloneWorkspace("PCalpha",OutputWorkspace="PCAp")
	CloneWorkspace("PCalpha",OutputWorkspace="PCPp")
	rho=mtd['PCrho']
	Ap=mtd['PCAp']
	Pp=mtd['PCPp']
	# for i in range(0,len(a1)):
		# x=(alpha.dataX(0)[i]+alpha.dataX(0)[i])/2.0
		# for j in range(0,4):
			# alpha.dataY(0)[i]=alpha.dataY(0)[i]+calpha[j]*x**j
			# rho.dataY(0)[i]=rho.dataY(0)[i]+crho[j]*x**j
			# Ap.dataY(0)[i]=Ap.dataY(0)[i]+cAp[j]*x**j
			# Pp.dataY(0)[i]=Pp.dataY(0)[i]+cPp[j]*x**j
	# Use the polynomial corretion fn instead
	PolynomialCorrection(InputWorkspace="PCalpha",OutputWorkspace="PCalpha",Coefficients=calpha,Operation="Multiply")
	PolynomialCorrection(InputWorkspace="PCrho",OutputWorkspace="PCrho",Coefficients=crho,Operation="Multiply")
	PolynomialCorrection(InputWorkspace="PCAp",OutputWorkspace="PCAp",Coefficients=cAp,Operation="Multiply")
	PolynomialCorrection(InputWorkspace="PCPp",OutputWorkspace="PCPp",Coefficients=cPp,Operation="Multiply")
	
	A0 = (Iaa * Pp * Ap) + (Ap * Ipa * rho * Pp) + (Ap * Iap * Pp * alpha) + (Ipp * Ap * alpha * rho * Pp)
	A1 = Pp * Iaa
	A2 = Pp * Iap
	A3 = Ap * Iaa
	A4 = Ap * Ipa
	A5 = Ap * alpha * Ipp
	A6 = Ap * alpha * Iap
	A7 = Pp * rho  * Ipp
	A8 = Pp * rho  * Ipa
	D = Pp * Ap *( 1.0 + rho + alpha + (rho * alpha) )  
	nIpp = (A0 - A1 + A2 - A3 + A4 + A5 - A6 + A7 - A8 + Ipp + Iaa - Ipa - Iap) / D
	nIaa = (A0 + A1 - A2 + A3 - A4 - A5 + A6 - A7 + A8 + Ipp + Iaa - Ipa - Iap) / D
	nIpa = (A0 - A1 + A2 + A3 - A4 - A5 + A6 + A7 - A8 - Ipp - Iaa + Ipa + Iap) / D
	nIap = (A0 + A1 - A2 - A3 + A4 + A5 - A6 - A7 + A8 - Ipp - Iaa + Ipa + Iap) / D
	RenameWorkspace(nIpp,OutputWorkspace=str(Ipp)+"corr")
	RenameWorkspace(nIpa,OutputWorkspace=str(Ipa)+"corr")
	RenameWorkspace(nIap,OutputWorkspace=str(Iap)+"corr")
	RenameWorkspace(nIaa,OutputWorkspace=str(Iaa)+"corr")
	ReplaceSpecialValues(str(Ipp)+"corr",OutputWorkspace=str(Ipp)+"corr",NaNValue="0.0",NaNError="0.0",InfinityValue="0.0",InfinityError="0.0")
	ReplaceSpecialValues(str(Ipp)+"corr",OutputWorkspace=str(Ipp)+"corr",NaNValue="0.0",NaNError="0.0",InfinityValue="0.0",InfinityError="0.0")
	ReplaceSpecialValues(str(Ipp)+"corr",OutputWorkspace=str(Ipp)+"corr",NaNValue="0.0",NaNError="0.0",InfinityValue="0.0",InfinityError="0.0")
	ReplaceSpecialValues(str(Ipp)+"corr",OutputWorkspace=str(Ipp)+"corr",NaNValue="0.0",NaNError="0.0",InfinityValue="0.0",InfinityError="0.0")
	iwksp=mtd.getObjectNames()
	list_n=[str(Ipp),str(Ipa),str(Iap),str(Iaa),"PCalpha","PCrho","PCAp","PCPp","1_p"]
	for i in range(len(iwksp)):
		for j in list_n:
			lname=len(j)
			if iwksp[i] [0:lname+1] == j+"_":
				DeleteWorkspace(iwksp[i])
	DeleteWorkspace("PCalpha")
	DeleteWorkspace("PCrho")
	DeleteWorkspace("PCAp")
	DeleteWorkspace("PCPp")
	DeleteWorkspace('A0')
	DeleteWorkspace('A1')
	DeleteWorkspace('A2')
	DeleteWorkspace('A3')
	DeleteWorkspace('A4')
	DeleteWorkspace('A5')
	DeleteWorkspace('A6')
	DeleteWorkspace('A7')
	DeleteWorkspace('A8')
	DeleteWorkspace('D')
#
#===========================================================
#
def nrPNRFn(runList,nameList,incidentAngles,DBList,specChan,minSpec,maxSpec,gparams,floodfile,PNRwithPA,pnums,doCorrs,doLDCorrs="0",subbgd=0,calibration=0,diagnostics=0):
	nlist=parseNameList(nameList)
	logger.notice("This is the sample nameslist:"+str(nlist))
	rlist=parseRunList(runList)
	logger.notice("This is the sample runlist:"+str(rlist))
	dlist=parseNameList(DBList)
	logger.notice("This is the Direct Beam nameslist:"+str(dlist))
	incAngles=parseNameList(incidentAngles)
	logger.notice("This incident Angles are:"+str(incAngles))
	
	if PNRwithPA == "2":
		nper=4
		logger.notice("PNRwithPA="+str(PNRwithPA))
		logger.notice(str(pnums))
	else:
		nper=2
	
	for i in range(len(rlist)):
		addRuns(rlist[i],nlist[i])
	
	mon_spec=int(gparams[3])-1
	minSp=int(minSpec)
	maxSp=int(maxSpec)
	reb=gparams[0]+","+gparams[1]+","+gparams[2]
	
	k=0
	for i in nlist:
		a1=mtd[i+"_1"]
		nspec=a1.getNumberHistograms()
		if (subbgd==1 and nspec!=4):
			# If a background subtraction is required sum the bgd outside the 
			# area of the detector that is visible through the analyser over all periods and average
			CloneWorkspace(i, OutputWorkspace="bgdtemp")
			ConvertUnits(InputWorkspace="bgdtemp",OutputWorkspace="bgdtemp",Target="Wavelength",AlignBins="1")
			Rebin(InputWorkspace="bgdtemp",OutputWorkspace="bgdtemp",Params=reb)
			CropWorkspace(InputWorkspace="bgdtemp",OutputWorkspace="bgdtemp",StartWorkspaceIndex=4,EndWorkspaceIndex=243)
			Plus("bgdtemp"+"_"+pnums[0],"bgdtemp"+"_"+pnums[1],OutputWorkspace="wbgdsum")
			if (nper>2):
				for j in range(2,nper):
					Plus("wbgdsum","bgdtemp"+"_"+pnums[j],OutputWorkspace="wbgdsum")
			GroupDetectors("wbgdsum",OutputWorkspace="bgd2",WorkspaceIndexList=range(0,50),KeepUngroupedSpectra="0")
			GroupDetectors("wbgdsum",OutputWorkspace="bgd1",WorkspaceIndexList=range(160,240),KeepUngroupedSpectra="0")
			Plus("bgd1","bgd2",OutputWorkspace="bgd")
			wbgdtemp=mtd["bgd"]/(130.0*nper)
			DeleteWorkspace("bgdtemp")
			DeleteWorkspace("wbgdsum")
			DeleteWorkspace("bgd1")
			DeleteWorkspace("bgd2")
			DeleteWorkspace("bgd")
			
		wksp=i
		ConvertUnits(InputWorkspace=wksp,OutputWorkspace=wksp,Target="Wavelength",AlignBins="1")
		Rebin(InputWorkspace=wksp,OutputWorkspace=wksp,Params=reb)
		CropWorkspace(InputWorkspace=wksp,OutputWorkspace=wksp+"mon",StartWorkspaceIndex=mon_spec,EndWorkspaceIndex=mon_spec)
		if nspec == 4:
			CropWorkspace(InputWorkspace=wksp,OutputWorkspace=wksp+"det",StartWorkspaceIndex=3,EndWorkspaceIndex=3)
			RotateInstrumentComponent(wksp+"det","DetectorBench",X="-1.0",Angle=str(2.0*float(incAngles[k])))
			Divide(LHSWorkspace=wksp+"det",RHSWorkspace=wksp+"mon",OutputWorkspace=wksp+"norm")
			if dlist[k] != "none":
				Divide(LHSWorkspace=wksp+"norm",RHSWorkspace=dlist[k],OutputWorkspace=wksp+"norm")
				ReplaceSpecialValues(wksp+"norm","0.0","0.0","0.0","0.0",OutputWorkspace=wksp+"norm")
				ConvertUnits(wksp+"norm",Target="MomentumTransfer",OutputWorkspace=wksp+"RvQ")
			if(diagnostics==0):
				DeleteWorkspace(wksp+"mon")
				DeleteWorkspace(wksp+"det")
		else:
			CropWorkspace(InputWorkspace=wksp,OutputWorkspace=wksp+"det",StartWorkspaceIndex=4,EndWorkspaceIndex=243)
			# move the first spectrum in the list onto the beam centre so that when the bench is rotated it's in the right place
			MoveInstrumentComponent(wksp+"det","DetectorBench",Y=str((125.0-float(minSpec))*1.2e-3))
			# add a bit to the angle to put the first spectrum of the group in the right place
			a1=2.0*float(incAngles[k])+atan((float(minSpec)-float(specChan))*1.2e-3/3.53)*180.0/pi
			#print str(2.0*float(incAngles[k]))+" "+str(atan((float(minSpec)-float(specChan))*1.2e-3/3.63)*180.0/pi)+" "+str(a1)
			RotateInstrumentComponent(wksp+"det","DetectorBench",X="-1.0",Angle=str(a1))
			floodnorm(wksp+"det",floodfile)
			if (subbgd==1):
				# Subract a per spectrum background
				Minus(wksp+"det",wbgdtemp,OutputWorkspace=wksp+"det")
				ResetNegatives(InputWorkspace=wksp+"det",OutputWorkspace=wksp+"det",AddMinimum='0',ResetValue="0.0")
				GroupDetectors(wksp+"det",OutputWorkspace=wksp+"sum",WorkspaceIndexList=range(int(minSpec)-5,int(maxSpec)-5+1),KeepUngroupedSpectra="0")
			else:
				GroupDetectors(wksp+"det",OutputWorkspace=wksp+"sum",WorkspaceIndexList=range(int(minSpec)-5,int(maxSpec)-5+1),KeepUngroupedSpectra="0")
			RebinToWorkspace(WorkspaceToRebin=wksp+"sum",WorkspaceToMatch=wksp+"mon",OutputWorkspace=wksp+"sum")
			Divide(LHSWorkspace=wksp+"sum",RHSWorkspace=wksp+"mon",OutputWorkspace=wksp+"norm")
			RebinToWorkspace(WorkspaceToRebin=wksp+"det",WorkspaceToMatch=wksp+"mon",OutputWorkspace=wksp+"det")
			Divide(LHSWorkspace=wksp+"det",RHSWorkspace=wksp+"mon",OutputWorkspace=wksp+"detnorm")
			if dlist[k]  != "none":
				Divide(LHSWorkspace=wksp+"norm",RHSWorkspace=dlist[k],OutputWorkspace=wksp+"norm")
				ReplaceSpecialValues(wksp+"norm","0.0","0.0","0.0","0.0",OutputWorkspace=wksp+"norm")
				Divide(LHSWorkspace=wksp+"detnorm",RHSWorkspace=dlist[k],OutputWorkspace=wksp+"detnorm")
				ReplaceSpecialValues(wksp+"detnorm","0.0","0.0","0.0","0.0",OutputWorkspace=wksp+"detnorm")
			ConvertUnits(wksp+"norm",OutputWorkspace=wksp+"RvQ",Target="MomentumTransfer")
			if(diagnostics == 0):
				DeleteWorkspace(wksp+"sum")
				DeleteWorkspace(wksp+"mon")
				DeleteWorkspace(wksp+"det")
		if doCorrs != "0":
			if nper == 2:
				nrPNRCorrection(i+"norm_"+pnums[0],i+"norm_"+pnums[1],calibration=calibration)
				for j in range(2):
					RenameWorkspace(InputWorkspace=i+"norm"+"_"+pnums[j]+"corr",OutputWorkspace=i+"normcorr"+"_"+pnums[j])
				GroupWorkspaces(InputWorkspaces=i+"normcorr_"+pnums[0]+","+i+"normcorr_"+pnums[1],OutputWorkspace=i+"normcorr")
				ConvertUnits(InputWorkspace=i+"normcorr",OutputWorkspace=i+"normcorrRvQ",Target="MomentumTransfer")
				if (nspec > 4 and doLDCorrs != "0"):
					nrPNRCorrection(i+"detnorm_"+pnums[0],i+"detnorm_"+pnums[1],calibration=calibration)
					for j in range(4):
						RenameWorkspace(InputWorkspace=i+"detnorm"+"_"+pnums[j]+"corr",OutputWorkspace=i+"detnormcorr"+"_"+pnums[j])
					GroupWorkspaces(InputWorkspaces=i+"detnormcorr_"+pnums[0]+","+i+"detnormcorr_"+pnums[1],OutputWorkspace=i+"detnormcorr")
			else:
				nrPACorrection(i+"norm"+"_"+pnums[0],i+"norm"+"_"+pnums[1],i+"norm"+"_"+pnums[2],i+"norm"+"_"+pnums[3],calibration=calibration)
				for j in range(4):
					RenameWorkspace(InputWorkspace=i+"norm"+"_"+pnums[j]+"corr",OutputWorkspace=i+"normcorr"+"_"+pnums[j])
				GroupWorkspaces(InputWorkspaces=i+"normcorr_"+pnums[0]+","+i+"normcorr_"+pnums[1]+","+i+"normcorr_"+pnums[2]+","+i+"normcorr_"+pnums[3]+"",OutputWorkspace=i+"normcorr")
				ConvertUnits(InputWorkspace=i+"normcorr",OutputWorkspace=i+"normcorrRvQ",Target="MomentumTransfer")
				if (nspec > 4 and doLDCorrs != "0"):
					nrPACorrection(i+"detnorm_"+pnums[0],i+"detnorm_"+pnums[1],i+"detnorm_"+pnums[2],i+"detnorm_"+pnums[3],calibration=calibration)
					for j in range(4):
						RenameWorkspace(InputWorkspace=i+"detnorm"+"_"+pnums[j]+"corr",OutputWorkspace=i+"detnormcorr"+"_"+pnums[j])
					GroupWorkspaces(InputWorkspaces=i+"detnormcorr_"+pnums[0]+","+i+"detnormcorr_"+pnums[1]+","+i+"detnormcorr_"+pnums[2]+","+i+"detnormcorr_"+pnums[3]+"",OutputWorkspace=i+"detnormcorr")
			if (diagnostics == 0 and doCorrs != "0"):
				DeleteWorkspace(i+"norm")
				#DeleteWorkspace(i+"RvQ")
			if (diagnostics == 0 and doLDCorrs != "0"):
				DeleteWorkspace(i+"detnorm")
		k=k+1
		DeleteWorkspace(i)
		if (subbgd==1):
			DeleteWorkspace("wbgdtemp")
#
#===========================================================
#
def tl(wksp,th0,schan):
	pixel=1.2
	dist=3630
	ThetaInc=th0*pi/180.0
	a1=mtd[wksp]
	y=a1.readY(0)
	ntc=len(y)
	nspec=a1.getNumberHistograms()
	x1=n.zeros((nspec+1,ntc+1))
	theta=n.zeros((nspec+1,ntc+1))
	y1=n.zeros((nspec,ntc))
	e1=n.zeros((nspec,ntc))
	for i in range(0,nspec):
		x=a1.readX(i)
		y=a1.readY(i)
		e=a1.readE(i)
		x1[i,0:ntc+1]=x[0:ntc+1]
		theta[i,:]=atan2( (i - schan-0.5) * pixel + dist * tan(ThetaInc) , dist)*180/pi
		y1[i,0:ntc]=y[0:ntc]
		e1[i,0:ntc]=e[0:ntc]
	x1[nspec,:]=x1[nspec-1,:]
	theta[nspec,:]=atan2( (nspec - schan-0.5) * pixel + dist * tan(ThetaInc) , dist)*180/pi
	d1=[x1,theta,y1,e1]
	return d1
#
#===========================================================
#
def writemap_tab(dat,th0,spchan,fname):
	a1=tl(dat,th0,spchan)
	f=open(fname,'w')
	x=a1[0]
	y=a1[1]
	z=a1[2]
	e=a1[3]
	s="\t"
	for i in range(0,n.shape(z)[1]-1):
		s+="%g\t" % ((x[0][i]+x[0][i+1])/2.0)
		s+="%g\t" % ((x[0][i]+x[0][i+1])/2.0)
	s+="\n"
	f.write(s)
	for i in range(0,n.shape(y)[0]-1):
		s=""
		s+="%g\t" % ((y[i][0]+y[i+1][0])/2.0)
		for j in range(0,n.shape(z)[1]-1):
			s+="%g\t" % z[i][j]
			s+="%g\t" % e[i][j]
		s+="\n"
		f.write(s)
	f.close()
#
#===========================================================
#
def xye(wksp):
	a1=mtd[wksp]
	x1=a1.readX(0)
	X1=n.zeros((len(x1)-1))
	for i in range(0,len(x1)-1):
		X1[i]=(x1[i]+x1[i+1])/2.0
	y1=a1.readY(0)
	e1=a1.readE(0)
	d1=[X1,y1,e1]
	return d1
#
#======================================================================================
#
def writeXYE_tab(dat,fname):
	a1=xye(dat)
	f=open(fname,'w')
	x=a1[0]
	y=a1[1]
	e=a1[2]		
	s=""
	s+="x\ty\te\n"
	f.write(s)
	for i in range(len(x)):
		s=""
		s+="%f\t" % x[i]
		s+="%f\t" % y[i]
		s+="%f\n" % e[i]  
		f.write(s)
	f.close()


'''
def quickPlot(runlist,dataDir,lmin,reb,lmax,spmin,spmax,output,plotper,polper,zmin,zmax,zlog):

	isisDataDir=dataDir
	logger.notice("setting dataDir="+dataDir+" "+isisDataDir)
	deleteFromRootName(output)
	addruns(runlist,output)
	nper=nperFromList(output)
	rebpars=str(lmin)+","+str(reb)+","+str(lmax)
		
	if nper == 1:
		ConvertUnits(InputWorkspace=output,OutputWorkspace=output,Target="Wavelength",AlignBins="1")
		Rebin(InputWorkspace=output,OutputWorkspace=output,Params=rebpars)
		CropWorkspace(InputWorkspace=output,OutputWorkspace=output+"m",StartWorkspaceIndex="1",EndWorkspaceIndex="1")
		CropWorkspace(InputWorkspace=output,OutputWorkspace=output+"d",StartWorkspaceIndex=str(spmin+4),EndWorkspaceIndex=str(spmax+4))
		Divide(output+"d",output+"m",OutputWorkspace=output+"n")
		workspace_mtx=mantidplot.importMatrixWorkspace(output+"n")
		gr2d=workspace_mtx.plotGraph2D()
		l=gr2d.activeLayer()
		if zlog == 0:
			l.setAxisScale(1,zmin,zmax,0)
		else:
			l.setAxisScale(1,zmin,zmax,1)
	else:
		workspace_mtx=[]
		nplot=0
		for i in plotper:
			ConvertUnits(InputWorkspace=output+"_"+str(i),OutputWorkspace=output+"_"+str(i),Target="Wavelength",AlignBins="1")
			Rebin(InputWorkspace=output+"_"+str(i),OutputWorkspace=output+"_"+str(i),Params=rebpars)
			CropWorkspace(InputWorkspace=output+"_"+str(i),OutputWorkspace=output+"_"+str(i)+"m",StartWorkspaceIndex="1",EndWorkspaceIndex="1")
			CropWorkspace(InputWorkspace=output+"_"+str(i),OutputWorkspace=output+"_"+str(i)+"d",StartWorkspaceIndex=str(spmin+4),EndWorkspaceIndex=str(spmax+4))
			Divide(output+"_"+str(i)+"d",output+"_"+str(i)+"m",OutputWorkspace=output+"_"+str(i)+"n")
			workspace_mtx.append(mantidplot.importMatrixWorkspace(output+"_"+str(i)+"n"))
			gr2d=workspace_mtx[nplot].plotGraph2D()
			nplot=nplot+1
			l=gr2d.activeLayer()
			if zlog == 0:
				l.setAxisScale(1,zmin,zmax,0)
			else:
				l.setAxisScale(1,zmin,zmax,1)
		
		up=mtd[output+"_2d"]
		down=mtd[output+"_1d"]
		asym=(up-down)/(down+up)
		RenameWorkspace(asym,OutputWorkspace=output+"_asym")
		ReplaceSpecialValues(output+"_asym",OutputWorkspace=output+"_asym","0.0","0.0","0.0","0.0")
		workspace_mtx.append(mantidplot.importMatrixWorkspace(output+"_asym"))
		gr2d=workspace_mtx[nplot].plotGraph2D()
		l=gr2d.activeLayer()
		l.setAxisScale(1,-1.0,1.0,0)


	logger.notice("quickPlot Finished)
'''

