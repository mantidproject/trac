LoadVesuvio(Filename='14188-14190',OutputWorkspace='raw_ws',SpectrumList='135-140',Mode='SingleDifference',
                    InstrumentParFile=r'IP0005.dat')
		    
CropWorkspace(InputWorkspace='raw_ws',OutputWorkspace='raw_ws',XMin=50,XMax=562)
raw_ws = ScaleX('raw_ws',Factor=1e-6,Operation="Multiply")

model_str = \
    "composite=ComptonScatteringCountRate,NumDeriv=1,IntensityConstraints=\"Matrix(1|3)0|-1|3\",$domains=i;"\
    "name=GramCharlierComptonProfile,Mass=1.007940,HermiteCoeffs=1 0 1;"\
    "name=GaussianComptonProfile,Mass=27.000000;"\
    "name=GaussianComptonProfile,Mass=91.000000"

model_str += ";ties=(f1.Width=10.000000,f2.Width=25.000000,f0.FSECoeff=f0.Width*1.414/12)"
model_str += ";constraints=(2.000000 < f0.Width < 7.000000)"

function_str = 'composite=MultiDomainFunction;(%s);(%s);(%s);ties=(f2.f0.Width=f1.f0.Width=f0.f0.Width)' % (model_str,model_str,model_str)

kwargs = {
	'WorkspaceIndex':0,
	'InputWorkspace_1':'raw_ws',
	'WorkspaceIndex_1':1,
	'InputWorkspace_2':'raw_ws',
	'WorkspaceIndex_2':2,
	'Output':'fit1', 
	'CreateOutput':True,
	'OutputCompositeMembers':True,
	'MaxIterations':5000,
	'Minimizer':"Levenberg-MarquardtMD,AbsError=1e-08,RelError=1e-08",
}

Fit(function_str, 'raw_ws',**kwargs)
