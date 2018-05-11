from __future__ import division
def normalization(input_array):
	array = input_array.astype(float)
	if array.size != 0:
		row_size = array[0].size
		row_count = int(array.size/array[0].size)
		
		for col in range(row_size):
			col_max = 0
			# find max in this loop
			for row in range(row_count):
				if array[row][col] > col_max:
					col_max = array[row][col]
			#print(col_max)
			
			# divide by max
			if col_max != 0:
				for row in range(row_count):
					if array[row][col] != 0:
						#print(array[row][col])
						array[row][col] /= float(col_max)
						#print(array[row][col])
	return array

def square(input_array):
	array = input_array.astype(float)

	if array.size != 0:
		row_size = array[0].size
		row_count = int(array.size/array[0].size)
	
	for col in range(row_size):
		for row in range(row_count):
			array[row][col] *= array[row][col]

	return array
