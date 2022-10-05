import numpy as np
import math

n_dims = 3
n_bins = 4

def make_nd_array(n_dims, n_bins):
	base_array = np.arange(0, int(math.pow(n_bins, n_dims)))
	
	shape = []
	for i in range(0, n_dims):
		shape.append(n_bins)
	as_grid = base_array.reshape(shape)
	return as_grid
	

def get_indexes_from_linear(index, grid):
	out_indexes = list()
	shape = grid.shape
	nBins  = shape[0]
	# first index
	ind    = index%nBins
	
	out_indexes.append(ind)
	
	#what left in linear index after first was removed
	
	rest = index/nBins;
	for d in range(1, len(shape)):
		nBins = shape[d]
	        ind  = rest%nBins;
		out_indexes.append( ind )
	        rest = rest/nBins
		
	return out_indexes

#as_grid = np.array([[0, 1, 2, 3], [4,5,6,7], [8,9,10,11], [12, 13, 14, 15]]) # 2D

#as_grid = as_grid.flatten() # 1D

as_grid = make_nd_array(n_dims, n_bins)


def get_neighbours(grid, i):
	
	n_dims = len(grid.shape)
	offset = 1
	back =  i - offset
	forward =i + offset
	
	
	if forward/grid.shape[0] == i/grid.shape[0]:
			print forward
	if back >= 0 and back/grid.shape[0] == i/grid.shape[0]:
			print back
	
	
	for j in range(1, n_dims):
		offset = offset * grid.shape[j-1]
		
		offset_next = offset * grid.shape[j]
		
		back = i - offset
		forward =  i + offset
		
		
		if forward/offset_next == i/offset_next:
			print forward
		if back >= 0 and back/offset_next == i/offset_next:
			print back

	
def is_within_boundaries(neigh_index, current_indexes, grid):
	neigh_indexes  = get_indexes_from_linear(neigh_index, grid)
	for index in range(len(current_indexes)):
		i = current_indexes[index]
		j = neigh_indexes[index]
		abs_diff = math.fabs(i-j) 
		if abs_diff < 0 or abs_diff > 1 :
			return False
	return True
				
		
def get_neighbours_all_touching(grid, i):
	
	n_dims = len(grid.shape)
	offset = 1
	
	
	back =  i - offset
	forward =i + offset

	indexes = get_indexes_from_linear(i, grid)
	
	permitations = list()
	permitations.append(0)
	
	dim_min = [None]
	dim_max = [None]
	
	permitations.append(1)
	permitations.append(-1)

	if forward/grid.shape[0] != i/grid.shape[0]:
			dim_max[0] = indexes[0]
	if back >= 0 and back/grid.shape[0] != i/grid.shape[0]:
			dim_min[0] = indexes[0]
	
	
	for j in range(1, n_dims):
		
		dim_min.append(None)
		dim_max.append(None)
		
		offset = offset * grid.shape[j-1]
		offset_next = offset * grid.shape[j]
		
		back = i - offset
		forward =  i + offset
		
		if forward/offset_next != i/offset_next:
			dim_max[j] = indexes[j]
		if back >= 0 and back/offset_next != i/offset_next:
			dim_min[j] = indexes[j]
		
		
		
		extended_perms = list()
	        for perm in permitations:
			
			extended_perms.append(perm + offset)
			extended_perms.append(-1*(perm+offset))
			
		permitations.extend(extended_perms)
		
		print "n perms", len(permitations)
		print permitations
		
			   
	for perm in permitations:
		if perm == 0:
			continue
		
		neigh_index = i + perm
		
		if is_within_boundaries(neigh_index, indexes, grid):
			print neigh_index
		
		
		
index = 1

print as_grid

get_neighbours_all_touching(as_grid, index)





		
		


