import sys
import itertools
import operator
import copy
import os

import numpy
import scipy.special
from mantid.simpleapi import *
from mantidplot import *

import tube
from tube_spec import TubeSpec
from tube_calib_fit_params import TubeCalibFitParams
from tube_calib import getCalibration

def mean(a):
	return sum(a) / len(a)

def pairwise(iterable):
	"""Helper function from: http://docs.python.org/2/library/itertools.html:
	s -> (s0,s1), (s1,s2), (s2, s3), ..."""
	a, b = itertools.tee(iterable)
	next(b, None)
	return itertools.izip(a, b)

def edge_pairs_overlap(edges_pair_a, edges_pair_b):
	""""""
	if edges_pair_a[0] < edges_pair_b[0] < edges_pair_a[1]:
		return True
	if edges_pair_b[0] < edges_pair_a[0] < edges_pair_b[1]:
		return True
	return False

def sort_and_merge_overlapping_edge_pairs(edge_pairs):
	"""Algorithm from: http://stackoverflow.com/a/5679899/778572"""
	temp = edge_pairs[0]
	for start, end in sorted([sorted(edge_pair) for edge_pair in edge_pairs]):
		if start <= temp[1]:
			temp[1] = max(temp[1], end)
		else:
			yield tuple(temp)
			temp[0] = start
			temp[1] = end
	yield tuple(temp)

def set_counts_to_one_between_x_range(ws, x_1, x_2):
	""""""
	if x_1 > x_2: x_1, x_2 = x_2, x_1
	for wsIndex in range(ws.getNumberHistograms()):
		try:
			if x_1 < ws.getDetector(wsIndex).getPos().getX() < x_2:
				ws.dataY(wsIndex)[0] = 1
		except RuntimeError:
			break
			#pass # Ignore "Detector with ID _____ not found" errors.

def set_counts_to_one_outside_x_range(ws, x_1, x_2):
	""""""
	if x_1 > x_2: x_1, x_2 = x_2, x_1
	set_counts_to_one_between_x_range(ws, -INF, x_1)
	set_counts_to_one_between_x_range(ws, x_2, INF)

def get_merged_edge_pairs_and_boundaries(edge_pairs):
	boundaries = [-INF]
	edge_pairs_merged = []
	
	temp = edge_pairs[0]
	
	for start, end in sorted([sorted(edge_pair) for edge_pair in edge_pairs]):
		if start <= temp[1]:
			boundary = start + (temp[1] - start) / 2
			temp[1] = max(temp[1], end)
			if start != temp[0]:
				boundaries.append(boundary)
		else:
			boundaries.append(temp[1] + (start - temp[1]) / 2)
			edge_pairs_merged.append(tuple(temp))
			temp[0] = start
			temp[1] = end
	edge_pairs_merged.append(tuple(temp))
	boundaries.append(INF)
	
	return edge_pairs_merged, boundaries

def get_integrated_workspace(data_file):
	ws_name = os.path.splitext(data_file)[0]
	try:
		ws = mtd[ws_name]
	except:
		print "Loading and integrating data from %s." % data_file
		ws = Load(Filename=data_file, OutputWorkspace=ws_name)
		ws = Integration(ws, OutputWorkspace=ws_name)
	return ws

def multiply_ws_list(ws_list, output_ws_name):
	print "Multiplying workspaces together..."
	it = iter(ws_list)
	total = next(it)
	for element in it:
		total = Multiply(RHSWorkspace=total, LHSWorkspace=element, OutputWorkspace = output_ws_name)
	return total

def get_pixels_from_edges(edges):
	pixels = []
	for edge in edges:
		pixels.append(int((edge + 0.5207) * 512))
	return numpy.array(pixels)

def get_tube_name(tube_id):
	# Construct the name of the tube based on the id (0-119) given.
	side = TubeSide.getTubeSide(tube_id)
	tube_side_num = tube_id / 2
	return "rear-detector/" + side + str(tube_side_num)
	
def get_tube_data(tube_id, ws):
	tube_name = get_tube_name(tube_id)
	
	# Piggy-back the TubeSpec class from Karl's Calibration code so that dealing with tubes is easier than interrogating the IDF ourselves.
	tube_spec = TubeSpec(ws)
	tube_spec.setTubeSpecByString(tube_name)
	assert tube_spec.getNumTubes() == 1
	tube_ws_index_list = tube_spec.getTube(0)[0]
	assert len(tube_ws_index_list) == 512

	# Return an array of all counts for the tube.
	return numpy.array([ws.dataY(ws_index)[0] for ws_index in tube_ws_index_list])

def get_tube_edge_pixels(tube_id, ws, cutoff, first_pixel=0, last_pixel=sys.maxint):
	count_data = get_tube_data(tube_id, ws)
	
	if count_data[first_pixel] < cutoff:
		up_edge = True
	else:
		up_edge = False
	
	for i, count in enumerate(count_data[first_pixel:last_pixel+1]):
		pixel = first_pixel + i
		if pixel > last_pixel:
			break
		if up_edge:
			if count >= cutoff:
				up_edge = False
				yield pixel
		else:
			if count < cutoff:
				up_edge = True
				yield pixel

def compile_param_table(tube_id, peaks):
	# Dirty hack we need to replace with something better.
	full_table = CreateEmptyTableWorkspace(OutputWorkspace="ParamTable_Tube" + str(tube_id))
	full_table.addColumn("int", "Peak #")
	full_table.addColumn("float", "A")
	full_table.addColumn("float", "B")
	full_table.addColumn("float", "C")
	full_table.addColumn("float", "D")
	base_name = "CalibPoint_Parameters_tube%i_peak_%i"
	table_names = [base_name % (tube_id, peak) for peak in range(peaks)]
	for peak, table_name in enumerate(table_names):
		table = mtd[table_name]
		row = [
			peak,
			table.cell("Value", 0),
			table.cell("Value", 1),
			table.cell("Value", 2),
			table.cell("Value", 3)
		]
		full_table.addRow(row)

def cleanup_param_tables(tube_id, peaks):
	# Dirty hack we need to replace with something better.
	base_name = "CalibPoint_Parameters_tube%i_peak_%i"
	table_names = [base_name % (tube_id, peak) for peak in range(peaks)]
	for table_name in table_names:
		table = mtd[table_name]
		table.delete()

BACKGROUND = 10

class SANS2DEndErfc(IFunction1D):
	def init(self):
		self.declareParameter("A", 350.0)
		self.declareParameter("B", 50.0)
		self.declareParameter("C", 6.0)
		self.declareParameter("D", BACKGROUND)

	def function1D(self, xvals):
		a = self.getParameterValue("A")
		b = self.getParameterValue("B")
		c = self.getParameterValue("C")
		d = self.getParameterValue("D")
		
		out = a * scipy.special.erfc((b - xvals) / c) + d
		if a < 0:
			out = -2*a * out
		
		return out

	def setActiveParameter(self, index, value):
		# Heavy-handed way to constrain background.
		if self.parameterName(index) == "D" and value < 0.0:
			self.setParameter(index, 0.0, False)
		elif self.parameterName(index) == "D" and value > BACKGROUND:
			self.setParameter(index, BACKGROUND, False)
		else:
			self.setParameter(index, value, False)

# Required to have Mantid recognise the new function
FunctionFactory.subscribe(SANS2DEndErfc)

INF = sys.float_info.max
TUBE_OFFSET = 0.003

# The number of counts past which we class something as an edge.  This is quite sensitive to change, since we sometimes end up picking
# up edges more than once, (e.g. we might see an edge at pixels 207 and 209, obviously due to the counts dipping back down below the
# threshold at pixel 206) which we then have to remove using ignore_guesses.  So, if THRESHOLD is changed you're probably going
# to have to change the contents of ignore_guesses for any affected tubes.
THRESHOLD = 500

class TubeSide:
	LEFT = "left"
	RIGHT = "right"
	@classmethod
	def getTubeSide(cls, tube_id):
		if tube_id % 2 == 0:
			return TubeSide.LEFT
		else:
			return TubeSide.RIGHT

# second runs, mostly with M4 removed
# 23088-add really was added, the hst files are single runs converted to histogram, so can merge with the added file
data_files = ["SANS2D00023098-hst.nxs","SANS2D00023097-hst.nxs","SANS2D00023096-hst.nxs","SANS2D00023095-hst.nxs","SANS2D00023094-hst.nxs",
                      "SANS2D00023093-hst.nxs","SANS2D00023092-hst.nxs","SANS2D00023091-hst.nxs",
                     "SANS2D00023088-add.nxs",
		     "SANS2D00023084-hst.nxs"]

known_edge_pairs = [
	[-0.415366832,	-0.377084653],
	[-0.334772772,	-0.296490594],
	[-0.254178713,	-0.215896535],
	[-0.163510396,	-0.125228218],
	[-0.082916337,	-0.044634158],
	[0.00775198,	0.046034158],
	[0.098420297,	0.136702475],
	[0.189088614,	0.227370792],
	[0.279756931,	0.318039109],
	[0.370425248,	0.408707426]
]

assert len(known_edge_pairs) == len(data_files)

ignore_guesses = {
	69 : [20, 21], # right34
	68 : [20, 21], # left34
	70 : [20], # left35
	118 : [12, 13], # left59
}
edges_not_to_fit = {
	47 : [10, 11], # right23
	49 : [10, 11], # right24
	51 : [10, 11], # right25
	53 : [10, 11], # right26
	
	67 : [19], # right33
	
	44 : [10, 11], # left22
	46 : [10, 11], # left23
	48 : [10, 11], # left24
	50 : [10, 11], # left25
	52 : [10, 11], # left26
	
	68 : [19], # left34
}

# Array indices of shadows (edge pairs) to remove.
shadows_to_remove = []

for shadow in reversed(sorted(shadows_to_remove)):
	del known_edge_pairs[shadow]
	del data_files[shadow]

known_edge_pairs = numpy.array(known_edge_pairs)

ws_list = [get_integrated_workspace(data_file) for data_file in data_files]

known_left_edge_pairs = copy.copy(known_edge_pairs)
known_right_edge_pairs = copy.copy(known_edge_pairs + TUBE_OFFSET)

_, boundaries = get_merged_edge_pairs_and_boundaries(known_edge_pairs)
known_left_edges, _ = get_merged_edge_pairs_and_boundaries(known_left_edge_pairs)
known_right_edges, _ = get_merged_edge_pairs_and_boundaries(known_right_edge_pairs)

for ws, (boundary_start, boundary_end) in zip(ws_list, pairwise(boundaries)):
	print "Isolating shadow in %s between boundaries %g and %g." % (str(ws), boundary_start, boundary_end)
	set_counts_to_one_outside_x_range(ws, boundary_start, boundary_end)

result_ws_name = "result"

multiply_ws_list(ws_list, result_ws_name)

result = mtd[result_ws_name]
original = CloneWorkspace(InputWorkspace=result_ws_name, OutputWorkspace="original")

known_edges_left = list(itertools.chain.from_iterable(known_left_edges))
known_edges_right = list(itertools.chain.from_iterable(known_right_edges))

margin=10

caltable = None

failed_pixel_guesses = []
pixel_guesses = []

for tube_id in range(120):
	tube_name = get_tube_name(tube_id)
	print "\n=================================================="
	print "ID = %i, Name = \"%s\"" % (tube_id, tube_name)
	if TubeSide.getTubeSide(tube_id) == TubeSide.LEFT:
		known_edges = copy.copy(known_edges_left)
	else:
		known_edges = copy.copy(known_edges_right)
		
	guessed_pixels = list(get_tube_edge_pixels(tube_id, result, THRESHOLD, 20, 482))
	
	print guessed_pixels
	print known_edges
	
	# Remove the pixel guesses that don't correspond to Cd shadows:
	if tube_id in ignore_guesses:
		print "Removing guesses", list(reversed(sorted(ignore_guesses[tube_id])))
		for index in reversed(sorted(ignore_guesses[tube_id])):
			del guessed_pixels[index]

	assert len(guessed_pixels) == len(known_edges)
	
	# Store the guesses for printing out later, along with the tube id and name.
	pixel_guesses.append(guessed_pixels)
	
	# Remove the edges that have been altered by the presence of the beam stop and arm.
	if tube_id in edges_not_to_fit:
		for index in reversed(sorted(edges_not_to_fit[tube_id])):
			del guessed_pixels[index]
			del known_edges[index]

	fitPar = TubeCalibFitParams(guessed_pixels, outEdge=10.0, inEdge=10.0)
	funcForm = [2]*len(guessed_pixels)
	
	if caltable:
		caltable = tube.calibrate(
		result,
		tube_name,
		numpy.array(known_edges),
		funcForm,
		rangeList=[0],
		plotTube=[0],
		margin=margin,
		fitPar=fitPar,
		calibTable=caltable)
	else:
		caltable = tube.calibrate(
		result,
		tube_name,
		numpy.array(known_edges),
		funcForm,
		rangeList=[0],
		plotTube=[0],
		margin=margin,
		fitPar=fitPar)
	
	#compile_param_table(tube_id, len(known_edges))
	#cleanup_param_tables(tube_id, len(known_edges))

ApplyCalibration(result, caltable)

# Show result in instrument view. (See http://www.mantidproject.org/MantidPlot:_Instrument_View)
inst_win = getInstrumentView(result_ws_name)
inst_win.show()

render = inst_win.getTab(InstrumentWindow.RENDER)
render.setSurfaceType(InstrumentWindow.CYLINDRICAL_Y)
render.setRange(0.0,900.0)

tree = inst_win.getTab(InstrumentWindow.TREE)
tree.selectComponentByName("rear-detector")

left = pixel_guesses[0::2]
right = pixel_guesses[1::2]

left_avg = numpy.array(map(mean, zip(*left)))
right_avg = numpy.array(map(mean, zip(*right)))

print left_avg
print right_avg
print right_avg - left_avg

