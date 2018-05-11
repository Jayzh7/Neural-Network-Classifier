def generateCM(predict, label):
	row_cnt = predict.shape[0]
	col_cnt = predict.shape[1]
	
	# Initialize a col_cnt*col_cnt matrix
	confusionMatrix = [[0 for x in range(col_cnt)] for y in range(col_cnt)]
	for index in range(row_cnt):
		single_predict = predict[index]
		
		# find the largest number which refers to the predict result
		largest_num = 0
		largest_num_index = 0
		for j in range(col_cnt):
			if single_predict[j] > largest_num:
				largest_num = single_predict[j]
				largest_num_index = j
		
		# find the actual activity
		actual_act = 0
		for j in range(col_cnt):
			if label[index][j] == 1:
				actual_act = j
				break
		
		# assgin value to confusion matrix
		confusionMatrix[actual_act][largest_num_index] += 1
		
	
	return confusionMatrix
		