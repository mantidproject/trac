#Ref test for DOS
import os
import numpy as np

#location of perl script on disk
dos_file_path = '/home/chs18285/Documents/dos/dos.pl'
#location of input file on disk
input_file_path = '/home/chs18285/Documents/dos/squaricn.phonon'

def readLogFile(wsName):
	fname = "log.txt"
	dataX, dataY = np.loadtxt(fname, unpack=True)
	return CreateWorkspace(DataX=dataX, DataY=dataY, OutputWorkspace=wsName + "_refdata")

os.system("perl %s %s > log.txt" % (dos_file_path, input_file_path))
ws = readLogFile("DOS")

os.system("perl %s -ir %s > log.txt" % (dos_file_path, input_file_path))
ws = readLogFile("IR")

os.system("perl %s -raman %s > log.txt" % (dos_file_path, input_file_path))
ws = readLogFile("Raman")
