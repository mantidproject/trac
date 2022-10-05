#!/bin/env python
"""
Fix frame wrapping events in powgen 

"""
import os, sys, struct
import numpy, math, fnmatch
from shutil import move, copy2 


__version__  = "0.3"

INSTRUMENT   = 'PG3'
TOP_DIR      = '.'
DSPACEMAP    = 'powgen_dspacemap_d1370_2010_09_12.dat'

PIX_MASK     = 0x000FFFFF  # PG3 "good" pixels  
FIX_MASK     = 0x00F00000  # PG3 mask for fixed pixels

TOF_FLAG     = 0x00100000  # 
RES_FLAG     = 0x00200000  #

MAX_PIXEL    = 300000      #

SNS_FREQ     = 60.0        # 60 Hz

MIN_EVENTS   = 4000        # need at least this many neutrons

NeutronEvent = numpy.dtype([('tof','uint32'),('pix','uint32')]) # event data format
DataChunk    = NeutronEvent.itemsize*1024L*1024L*24L            # read 24 Mevents at once, otherwise a small DFS might choke


fix_log = sys.stdout

def log_msg(*args):
	"Simple log - to the screen and to the file"
	for arg in args:
		fix_log.write(arg)
		if fix_log != sys.stdout:
			print arg,
	else:
		fix_log.write('\n')
		if fix_log != sys.stdout:
			print 
		
		

def find_prenexus(file_type='*neutron_event.dat', top_dir=TOP_DIR):
	"Find DAS files"
	for root, dirs, files in os.walk(top_dir):
		for file_name in files:
			if fnmatch.fnmatch(file_name, file_type):
				yield os.path.join(root, file_name)


def plot_dspace(data, file_name, log_scale=True):
	"""Here is some plotting just for purpose of seeing
	that selected neutrons not needed for fix"""
	base_file = os.path.basename(file_name)
	d_max =   20.0
	n_bin = 2000
	pylab.figure()
	pylab.title('%s All Modules' % file_name)
	for label, d in data:
		dhist,dbins = numpy.histogram(d,  bins=n_bin, range=(0.0,d_max), new=True)
		if log_scale:
			pylab.semilogy(dbins[:-1], dhist, marker='.', linestyle='steps', label=label)
		else:
			pylab.plot    (dbins[:-1], dhist, marker='.', linestyle='steps', label=label)
		
	pylab.xlabel('d [A]')
	pylab.legend()
	


def check_fixed(event_file, dspmap, do_plot=False):
	"""
	Test if file already fixed
	"""
	
	events_fd  = open(event_file, 'rb')
	events_buf = events_fd.read(NeutronEvent.itemsize)
	if not events_buf:
		return True
	events     = numpy.fromstring(events_buf, dtype=NeutronEvent)
	events_fd.close()
	
	if not (events[0]['pix'] & FIX_MASK):
		return False


	if do_plot:
		events_fd  = open(event_file, 'rb')
		events_buf = events_fd.read(DataChunk)
		if not events_buf:
			return True
		events     = numpy.fromstring(events_buf, dtype=NeutronEvent)
		events_fd.close()

		pix     = events['pix']
		tof     = events['tof']

		pix = pix & PIX_MASK
		d   = 2*dspmap[pix]*tof	
		plot_dspace([('Previously Fixed', d)], event_file)		
	return True 



def fix_file_loop(event_file, dspace_file=None, verbose=True, do_force=False, do_plot=False):
	"Main function"

	log_msg("** processing file %s" % event_file)

	n_events = os.stat(event_file)[6]/NeutronEvent.itemsize # python 2.5 has better definition of os.stat
	if n_events < MIN_EVENTS :
		log_msg("!! event file too small, need at least %d events (got %d)" % (MIN_EVENTS, n_events))
		return


	dspmap  = numpy.memmap(dspace_file, dtype='float64'   , mode='r' )


	if check_fixed(event_file, dspmap, do_plot) and not do_force:
		log_msg('!! event file previously fixed; aborting fix of this file')
		return
		
	# copy files first
	# orig_file = event_file + '.orig'
	orig_file = os.path.join(os.path.dirname(event_file), os.path.basename(event_file).split('.')[0]) + '_orig.dat'

	
	if os.path.exists(orig_file) and do_force:
		log_msg('-- restoring original event file %s -> %s' % (orig_file, event_file))
		os.remove(event_file)
		copy2(orig_file, event_file)
	else:
		log_msg('-- making backup copy of the original event file %s <- %s' % (orig_file, event_file))
		copy2(event_file, orig_file)

	min_usperA = 15750.0
	DifCr      = 15000.0
	LDifCr     = math.log10(DifCr)
	K          = 3.22  # gradient of lin
	sns_frame  = 1e7/SNS_FREQ # convert to units of 100 ns

	usperAr    = numpy.zeros(MAX_PIXEL, dtype='float')  # microseconds per Agstrom
	fw_tof     = numpy.zeros(MAX_PIXEL, dtype='float')  # an array for the min_tof calculated for all pixels
	sqrtdmin   = numpy.zeros(MAX_PIXEL, dtype='float')  # sqrt(d_min)
	min_tofA   = numpy.zeros(MAX_PIXEL, dtype='float')  # A = array

	# two_sin_theta =        0.003 + (0.60507e-5/dspmap) + (0.00973e-10*dspmap**-2)
	usperAr = ((10.0*dspmap*(0.003 + (0.60507e-5/dspmap) + (0.00973e-10*dspmap**-2)))**-1)/min_usperA
	
	
	n_events       = 0
	n_events2fix_t = 0 
	n_events2fix_r = 0

	first_buf      = True
	events_inp = open(orig_file,  'rb')
	events_out = open(event_file, 'wb')
	while True:
		events_buf = events_inp.read(DataChunk)
		if not events_buf:
			break
		log_msg('-- read %.1f MB of data' % (len(events_buf)/1024.0/1024.0))
		events  = numpy.fromstring(events_buf, dtype=NeutronEvent)

		pix        = events['pix']
		tof        = events['tof']
		
		n_events  += numpy.size(pix)  # number of events

		if first_buf: # calculate things only on the first buffer
			min_tof     = min(tof[MIN_EVENTS/2:MIN_EVENTS]) 
			max_tof     = max(tof[MIN_EVENTS/2:MIN_EVENTS])
			d_tof       = max_tof - min_tof
			time_offset = int(sns_frame*int(d_tof/sns_frame+0.49)) # get the time offset
			log_msg('-- %f < TOFs < %f   & Delta_TOF = %f' %(0.1*min_tof,0.1*max_tof,0.1*d_tof))
			log_msg('-- using time offset of %f usec' % time_offset)

			# calculate the min_tof for each pixel
			fw_tof = (usperAr * max_tof *0.99284) - d_tof  #0.99284 is because end of lambda band is not at end of TOF band

			# calculate the min_tof for each pixel
			sqrtdminr = (0.1*min_tof/DifCr)**0.5  #reference point

			sqrtdmin  = sqrtdminr + (K*(LDifCr-numpy.log10(0.1/dspmap)))  #expression for calculating d_min allowed for all pixels

			# calculate min TOF for each pixel
			min_tofA  = sqrtdmin/dspmap
			min_tofA *= (min_tofA > 0.0)

			min_tofA *= sqrtdmin

			if verbose:
				log_msg( "-- usperAr: %s" % usperAr[230000:230050] )
				log_msg( "-- usperAr: %s" % usperAr[55001:55005] )
				log_msg( "-- usperAr: %s" % usperAr[231051:231055] )
			
				log_msg( "-- fw_tof: %s" % (0.1*fw_tof[55001:55005] ))
				log_msg( "-- fw_tof: %s" % (0.1*fw_tof[231051:231055]))

				log_msg( "-- min_tofA: %s" % (0.1*min_tofA[55001:55005]   ))
				log_msg( "-- min_tofA: %s" % (0.1*min_tofA[231051:231055] ))



	        # correct any bad pixel ids in case thre are errors
		pix = pix * (pix < PIX_MASK)

                #create mask: events2fix
		events2fix_t   = (tof < fw_tof[pix])
		events2fix_r   = (tof < min_tofA[pix])
		n_events2fix_t += events2fix_t.sum()
		n_events2fix_r += events2fix_r.sum()
	
		# ----------------------------------------------------------------------------------------
                # fixing of events 
		tof_new = tof + events2fix_t * time_offset
		pix_new = pix | events2fix_t * TOF_FLAG    | events2fix_r*RES_FLAG
		# ----------------------------------------------------------------------------------------

		if do_plot and first_buf:
			do  = 2*dspmap[pix]*tof      # original d-plot
			df  = 2*dspmap[pix]*tof_new  # fixed d-plot
			histograms = [
				('Original'       ,  do                    ),
				('Bad TOF'        ,  do[events2fix_t]      ),			
				('Fixed'          ,  df                    ),
				('Bad TOF (fixed)',  df[events2fix_t]      ),
				]
			plot_dspace(histograms , event_file)


		events['tof'] = tof_new
		events['pix'] = pix_new
		if first_buf:
			events[0]['pix'] = events[0]['pix'] | FIX_MASK
			first_buf = False
			if verbose:
				log_msg( "-- event[0]: PIX=0x%08X TOF=%d" % (events[0]['pix'], events[0]['tof']))
		events.tofile(events_out)

		
	log_msg('-- %8d/%d events [%5.3f %%] are flagged with TOF_FLAG=0x%08x' % (n_events2fix_t, n_events, 100.0*n_events2fix_t/n_events, TOF_FLAG))
	log_msg('-- %8d/%d events [%5.3f %%] are flagged with RES_FLAG=0x%08x' % (n_events2fix_r, n_events, 100.0*n_events2fix_r/n_events, RES_FLAG))
	log_msg('-- event file %s is fixed' % event_file)
	events_out.close()
	events_inp.close()




if __name__ == "__main__":
	import optparse

	usage   = "%prog [options] run_number" #% argv0
	version = "%%prog %s" % __version__

	opt = optparse.OptionParser(usage=usage, version=version) 

	opt.add_option("-D", "--dspace", dest="dspace" , default=DSPACEMAP)
	opt.add_option("-d", "--dir"   , dest="top_dir", default='.')
	opt.add_option("-p", "--plot",
		       action="store_true", dest="plot", default=False,
		       help="plot diagnostic plots")
	opt.add_option("-v", "--verbose",
		       action="store_true", dest="verbose", default=False,
		       help="don't print status messages")

	opt.add_option("-l", "--log", dest="logfile",
		       help="print messages to a log file")
	opt.add_option("-f", "--force", action="store_true", dest="force" , default=False)


			   
	options, args = opt.parse_args()
	if options.logfile:
		fix_log = open(options.logfile, 'at+')

	if options.plot:
		import pylab
	
	if not args:
		args = ['']
	for arg in args:
		file_type="*%s*neutron_event.dat" % arg
		for file_name in find_prenexus(top_dir=options.top_dir, file_type=file_type):
			fix_file_loop(file_name, dspace_file=options.dspace,
				 verbose=options.verbose, do_plot=options.plot,
				 do_force=options.force)
	if options.plot:
		pylab.show()
