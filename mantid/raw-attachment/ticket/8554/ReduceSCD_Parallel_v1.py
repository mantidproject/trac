
# File: ReduceSCD_Parallel.py
#
# Version 2.0, modified to work with Mantid's new python interface.
#
# This script will run multiple instances of the script ReduceOneSCD_Run.py
# in parallel, using either local processes or a slurm partition.  After
# using the ReduceOneSCD_Run script to find, index and integrate peaks from
# multiple runs, this script merges the integrated peaks files and re-indexes
# them in a consistent way.  If desired, the indexing can also be changed to a
# specified conventional cell.
# Many intermediate files are generated and saved, so all output is written 
# to a specified output_directory.  This output directory must be created
# before running this script, and must be specified in the configuration file.
# The user should first make sure that all parameters are set properly in
# the configuration file for the ReduceOneSCD_Run.py script, and that that 
# script will properly reduce one scd run.  Once a single run can be properly
# reduced, set the additional parameters in the configuration file that specify 
# how the the list of runs will be processed in parallel. 
#

#
# _v1: December 3rd 2013. Mads Joergensen
# This version now includes the posibility to use the 1D cylindrical integration method
# and the posibility to load a UB matrix which will be used for integration of the individual
# runs and to index the combined file (Code from Xiapoing).
#

import os
import sys
import threading
import time
import ReduceDictionary

#sys.path.append("/opt/mantidnightly/bin")
sys.path.append("/opt/Mantid/bin")

from mantid.simpleapi import *

print "API Version"
print apiVersion()

start_time = time.time()

# -------------------------------------------------------------------------
# ProcessThread is a simple local class.  Each instance of ProcessThread is 
# a thread that starts a command line process to reduce one run.
#
class ProcessThread ( threading.Thread ):
   command = ""

   def setCommand( self, command="" ):
      self.command = command

   def run ( self ):
      print 'STARTING PROCESS: ' + self.command
      os.system( self.command )

# -------------------------------------------------------------------------

#
# Get the config file name from the command line
#
if (len(sys.argv) < 2):
  print "You MUST give the config file name on the command line"
  exit(0)

config_file_name = sys.argv[1]

#
# Load the parameter names and values from the specified configuration file 
# into a dictionary and set all the required parameters from the dictionary.
#

params_dictionary = ReduceDictionary.LoadDictionary( config_file_name )

exp_name              = params_dictionary[ "exp_name" ]
output_directory      = params_dictionary[ "output_directory" ]
reduce_one_run_script = params_dictionary[ "reduce_one_run_script" ]
slurm_queue_name      = params_dictionary[ "slurm_queue_name" ] 
max_processes         = int(params_dictionary[ "max_processes" ])
min_d                 = params_dictionary[ "min_d" ]
max_d                 = params_dictionary[ "max_d" ]
tolerance             = params_dictionary[ "tolerance" ]
cell_type             = params_dictionary[ "cell_type" ] 
centering             = params_dictionary[ "centering" ]
run_nums              = params_dictionary[ "run_nums" ]

use_cylindrical_integration = params_dictionary[ "use_cylindrical_integration" ]
instrument_name       = params_dictionary[ "instrument_name" ]

read_UB               = params_dictionary[ "read_UB" ]
UB_filename           = params_dictionary[ "UB_filename" ]

#
# Make the list of separate process commands.  If a slurm queue name
# was specified, run the processes using slurm, otherwise just use
# multiple processes on the local machine.
#
list=[]
index = 0
for r_num in run_nums:
  list.append( ProcessThread() )
  cmd = 'python ' + reduce_one_run_script + ' ' + config_file_name + ' ' + str(r_num)
  if slurm_queue_name is not None:
    console_file = output_directory + "/" + str(r_num) + "_output.txt"
    cmd =  'srun -p ' + slurm_queue_name + \
           ' --cpus-per-task=3 -J ReduceSCD_Parallel.py -o ' + console_file + ' ' + cmd
  list[index].setCommand( cmd )
  index = index + 1

#
# Now create and start a thread for each command to run the commands in parallel, 
# starting up to max_processes simultaneously.  
#
all_done = False
active_list=[]
while not all_done:
  if ( len(list) > 0 and len(active_list) < max_processes ):
    thread = list[0]
    list.remove(thread)
    active_list.append( thread ) 
    thread.start()
  time.sleep(2)
  for thread in active_list:
    if not thread.isAlive():
      active_list.remove( thread )
  if len(list) == 0 and len(active_list) == 0 :
    all_done = True

print "\n**************************************************************************************"
print   "************** Completed Individual Runs, Starting to Combine Results ****************"
print   "**************************************************************************************\n"

#
# First combine all of the integrated files, by reading the separate files and
# appending them to a combined output file.
#
niggli_name = output_directory + "/" + exp_name + "_Niggli"
niggli_integrate_file = niggli_name + ".integrate"
niggli_matrix_file = niggli_name + ".mat"

first_time = True
if not use_cylindrical_integration:
  for r_num in run_nums:
    one_run_file = output_directory + '/' + str(r_num) + '_Niggli.integrate'
    peaks_ws = LoadIsawPeaks( Filename=one_run_file )
    if first_time:
      SaveIsawPeaks( InputWorkspace=peaks_ws, AppendFile=False, Filename=niggli_integrate_file )
      first_time = False
    else:
      SaveIsawPeaks( InputWorkspace=peaks_ws, AppendFile=True, Filename=niggli_integrate_file )

#
# Load the combined file and re-index all of the peaks together. 
# Save them back to the combined Niggli file (Or selcted UB file if in use...)
#
  peaks_ws = LoadIsawPeaks( Filename=niggli_integrate_file )

#
# Find a Niggli UB matrix that indexes the peaks in this run
# Load UB instead of Using FFT
#Index peaks using UB from UB of initial orientation run/or combined runs from first iteration of crystal orientation refinement
  if read_UB:
    LoadIsawUB(InputWorkspace=peaks_ws, Filename=UB_filename)
  #OptimizeCrystalPlacement(PeaksWorkspace=peaks_ws,ModifiedPeaksWorkspace=peaks_ws,FitInfoTable='CrystalPlacement_info',MaxIndexingError=tolerance)
  else:
    FindUBUsingFFT( PeaksWorkspace=peaks_ws, MinD=min_d, MaxD=max_d, Tolerance=tolerance )

  IndexPeaks( PeaksWorkspace=peaks_ws, Tolerance=tolerance )
  SaveIsawPeaks( InputWorkspace=peaks_ws, AppendFile=False, Filename=niggli_integrate_file )
  SaveIsawUB( InputWorkspace=peaks_ws, Filename=niggli_matrix_file )

#
# If requested, also switch to the specified conventional cell and save the
# corresponding matrix and integrate file
#
if not use_cylindrical_integration:
  if (not cell_type is None) and (not centering is None) :
    conv_name = output_directory + "/" + exp_name + "_" + cell_type + "_" + centering
    conventional_integrate_file = conv_name + ".integrate"
    conventional_matrix_file = conv_name + ".mat"

    SelectCellOfType( PeaksWorkspace=peaks_ws, CellType=cell_type, Centering=centering,
                      Apply=True, Tolerance=tolerance )
    SaveIsawPeaks( InputWorkspace=peaks_ws, AppendFile=False, Filename=conventional_integrate_file )
    SaveIsawUB( InputWorkspace=peaks_ws, Filename=conventional_matrix_file )

if use_cylindrical_integration: 
  if (not cell_type is None) or (not centering is None):
    print "WARNING: Cylindrical profiles are NOT transformed!!!"
  # Combine *.profiles files
  filename = output_directory + '/' + exp_name + '.profiles'
  output = open( filename, 'w' )

  # Read and write the first run profile file with header.
  r_num = run_nums[0]
  filename = output_directory + '/' + instrument_name + '_' + r_num + '.profiles'
  input = open( filename, 'r' )
  file_all_lines = input.read()
  output.write(file_all_lines)
  input.close()
  os.remove(filename)

  # Read and write the rest of the runs without the header.
  for r_num in run_nums[1:]:
      filename = output_directory + '/' + instrument_name + '_' + r_num + '.profiles'
      input = open(filename, 'r')
      for line in input:
          if line[0] == '0': break
      output.write(line)
      for line in input:
          output.write(line)
      input.close()
      os.remove(filename)

  # Remove *.integrate file(s) ONLY USED FOR CYLINDRICAL INTEGRATION!
  for file in os.listdir(output_directory):
    if file.endswith('.integrate'):
      os.remove(file)

end_time = time.time()

print "\n**************************************************************************************"
print   "****************************** DONE PROCESSING ALL RUNS ******************************"
print   "**************************************************************************************\n"

print 'Total time:   ' + str(end_time - start_time) + ' sec'
print 'Connfig file: ' + config_file_name 
print 'Script file:  ' + reduce_one_run_script + '\n'
print
