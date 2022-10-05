raw_wksp = LoadRaw('C:/Mantid/trunk/Test/Data/HRP39191.raw','hrpd39191').workspace()
ConvertUnits(raw_wksp,raw_wksp, 'Wavelength')
samplePos = raw_wksp.getInstrument().getSample().getPos()

slabWidthInCM = 1.8
slabHeightInCM = 2.3
slabThicknessInCM = 1.5

slabWidthInM = slabWidthInCM * 0.01
slabHeightInM = slabHeightInCM * 0.01
slabThicknessInM = slabThicknessInCM * 0.01

szX = (slabWidthInM/2) + samplePos.getX()
szY = (slabHeightInM/2) + samplePos.getY()
szZ = (slabThicknessInM/2) + samplePos.getZ()

sampleXML = " <cuboid id=\"sample-shape\"> " + \
"<left-front-bottom-point x=\"" + str(szX) + "\" y=\"" + str(-szY) + "\" z=\"" + str(-szZ) + "\"  /> "  + \
"<left-front-top-point  x=\"" +str(szX) + "\" y=\"" + str(szY) + "\" z=\"" + str(-szZ) + "\"  /> " + \
"<left-back-bottom-point  x=\"" + str(szX) + "\" y=\"" + str(-szY) + "\" z=\"" + str(szZ) + "\"  /> " + \
"<right-front-bottom-point  x=\"" + str(-szX) + "\" y=\"" + str(-szY) + "\" z=\"" + str(-szZ) + "\"  /> " +\
"</cuboid>"

gaugeWidthInCM = 1.3
gaugeHeightInCM = 2.1 
gaugeThicknessInCM = 1.2

gaugeWidthInM = gaugeWidthInCM * 0.01
gaugeHeightInM = gaugeHeightInCM * 0.01
gaugeThicknessInM = gaugeThicknessInCM * 0.01

gzX = (gaugeWidthInM/2) + samplePos.getX()
gzY = (gaugeHeightInM/2) + samplePos.getY()
gzZ = (gaugeThicknessInM/2) + samplePos.getZ()
	
gaugeXML = " <cuboid id=\"gauge-shape\"> " + \
"<left-front-bottom-point x=\"" + str(gzX) + "\" y=\"" + str(-gzY) + "\" z=\"" + str(-gzZ) + "\"  /> "  + \
"<left-front-top-point  x=\"" +str(gzX) + "\" y=\"" + str(gzY) + "\" z=\"" + str(-gzZ) + "\"  /> " + \
"<left-back-bottom-point  x=\"" + str(gzX) + "\" y=\"" + str(-gzY) + "\" z=\"" + str(gzZ) + "\"  /> " + \
"<right-front-bottom-point  x=\"" + str(-gzX) + "\" y=\"" + str(-gzY) + "\" z=\"" + str(-gzZ) + "\"  /> " +\
"</cuboid>"

# Define the sample shape and gauge volume on the workspace
CreateSampleShape(raw_wksp, sampleXML)
DefineGaugeVolume(raw_wksp, gaugeXML)

attenXsec = 6.52
scatterXsec = 19.876
numberDensity = 0.0093
npoints = 100

AbsorptionCorrection(raw_wksp, 'anyshape_correction', attenXsec,scatterXsec,numberDensity,npoints)

# Should equal CuboidGaugeVolumeAbsorption with same shape = FlatPlateAbsorption
CuboidGaugeVolumeAbsorption(raw_wksp, 'cuboidgauge_correction', attenXsec,scatterXsec,numberDensity,gaugeHeightInCM,gaugeWidthInCM,gaugeThicknessInCM,npoints)

checker = CheckWorkspacesMatch('anyshape_correction', 'cuboidgauge_correction', Tolerance=0.001)
match = checker.getPropertyValue('Result')
print 'Checking AnyShape against CuboidGaugeVolume:',match

FlatPlateAbsorption(raw_wksp, 'flatplate_correction', attenXsec,scatterXsec,numberDensity,slabHeightInCM,slabWidthInCM,slabThicknessInCM,npoints)
checker = CheckWorkspacesMatch('flatplate_correction', 'cuboidgauge_correction', Tolerance=0.001)
match = checker.getPropertyValue('Result')
print 'Checking FlatPlate against CuboidGaugeVolume:',match

checker = CheckWorkspacesMatch('flatplate_correction', 'anyshape_correction', Tolerance=0.001)
match = checker.getPropertyValue('Result')
print 'Checking FlatPlate against AnyShape:',match