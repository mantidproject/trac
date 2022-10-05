# Algorithm to start Bayes programs
from mantid.simpleapi import *
from mantid.kernel import StringListValidator, StringMandatoryValidator
from mantid.api import PythonAlgorithm, AlgorithmFactory
from mantid import config
import os

from IndirectImport import run_f2py_compatibility_test, is_supported_f2py_platform

if is_supported_f2py_platform():
	import IndirectBayes as Main

run_f2py_compatibility_test()
		
prog = 'QLwat'
nbins = [1, 1]
sname = 'irs26176_graphite002_red'
rname = 'irs26173_graphite002_res'
rsname = ''
wfile = ''
erange = [-0.5,0.5]
fitOp = [False, 'Sloping', False, False]
loopOp = True
verbOp = False
plotOp = 'None'
saveOp = True

workdir = config['defaultsave.directory']
spath = os.path.join(workdir, sname+'.nxs')		# path name for sample nxs file
LoadNexusProcessed(Filename=spath, OutputWorkspace=sname)
rpath = os.path.join(workdir, rname+'.nxs')		# path name for res nxs file
LoadNexusProcessed(Filename=rpath, OutputWorkspace=rname)
Main.QLRun(prog,sname,rname,rsname,erange,nbins,fitOp,wfile,loopOp,verbOp,plotOp,saveOp)
