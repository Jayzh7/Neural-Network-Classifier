'''
read from cairo dataset and return 3-splited data and labels for 3-fold cross validation
'''

import numpy as np
import keras
from random import shuffle
'''
27 Sensors are used in total. Their data will be 
stored in a list with index being id. 
i.e. M001 will be store in index 1
'''
def readData(split=[0.33, 0.66]): 
    read_file = open("datasets/cairo.data")

    next = read_file.readline()
    # print the line num in debug mode
    line_num = 1
    activity_on = False
    activity_map = {0: 'Bed_to_toilet', 1: 'Breakfast', 2: 'Bed', 3: 'C_work', 
                        4: 'Dinner', 5: 'Laundry', 6: 'Leave_home', 7: 'Lunch',
                        8: 'Night_wandering', 9: 'R_medicine'}
												
    number_of_activities = len(activity_map)
    number_of_sensors    = 27

    # dict to store all sensor active level of all activities.
    sensor_freq = {}
    # init
    for i in range(0,number_of_activities):
        sensor_freq[activity_map[i]] = []

    # cursor to record number of each activities that have been processed
    num_act = {}
    # init all value to be 0
    for i in range(0, number_of_activities):
        num_act[activity_map[i]] = -1

    # replace this dict by using int(sensor_no[-2:])
    #sensor_map = {'M001': 0,'M002': 1,'M003': 2,'M004': 3,'M005': 4,'M006': 5,'M007': 6,'M008': 7,'M009': 8,'M010': 9,'M011': 10,'M012': 11,
    #'M013': 0,'M001': 0,'M001': 0,'M001': 0,'M001': 0,'M001': 0,'M001': 0,'M001': 0,'M001': 0,'M001': 0,'M001': 0,'M001': 0,'M001': 0,


    while next:
        status = next[-3:-1]

        # last two letters of begin, indicating start of an activity
        if "in" in status:
            activity_on = True;
            date, time, sensor_no, sensor_status, activity_name, activity_status = next.split(' ')

            if activity_name in sensor_freq.keys():	
                # Start of an activity, increment the cursor
                num_act[activity_name] += 1		
                sensor_freq[activity_name].append([])
                for j in range(0, number_of_sensors):
                    sensor_freq[activity_name][num_act[activity_name]].append(0)

            else:
                print('unrecognized activity')
                exit()

        else:
            if "nd" in status:
                date, time, sensor_no, sensor_status, activity_name, activity_status = next.split(' ')
            else:
                date, time, sensor_no, sensor_status = next.split(' ')

        # only counts when inside an activity			
        if activity_on:
            # sensor switching status
            if "ON" in sensor_status: 
                #print("num_act:"+str(num_act[activity_name]))
                #print("sensor_no:"+str(int(sensor_no[-2:])))
                if sensor_no[0] != 'T':
                  sensor_freq[activity_name][num_act[activity_name]][int(sensor_no[-2:])-1] += 1
            elif "FF" in sensor_status:
                # do nothing
                x = 1

            # non annotated data, ignore

        # last two letters of end, indicating end of an activity
        if "nd" in status:
            activity_on = False;

        next = read_file.readline()
        #print("lline:"+str(line_num))
        line_num += 1
    for k in num_act:
        num_act[k] += 1


    X1_data = []
    X1_label = []
    X2_data = []
    X2_label = []
    X3_data = []
    X3_label = []
		
    for key, value in activity_map.items():
        shuffle(sensor_freq[value])
      
        for j in range(int(num_act[value]*(split[0]))):
            X1_data.append(sensor_freq[value][j])
            X1_label.append(key)
        for j in range(int(num_act[value]*split[0])+1,int(num_act[value]*split[1])):
            X2_data.append(sensor_freq[value][j])
            X2_label.append(key)
        for j in range(int(num_act[value]*split[1])+1, num_act[value]):
            X3_data.append(sensor_freq[value][j])
            X3_label.append(key)
    X1_data = np.array(X1_data)
    X1_label = np.array(X1_label)
    X2_data = np.array(X2_data)
    X2_label = np.array(X2_label)
    X3_data = np.array(X3_data)
    X3_label = np.array(X3_label)
   
    return [X1_data, X2_data, X3_data], [X1_label, X2_label, X3_label]
'''
for j in range(0, 10):
	for i in range(0, num_act[activity_map[j]]+1):
		print(sensor_freq[activity_map[j]][i])

for i in range(0, 10):
    num_act[activity_map[i]] += 1
#        
for act_no in range(0, 10):
    # This list is used to calc average
    sensor_freq[activity_map[act_no]].append([])
    for sen_no in range(0, 27):
        sensor_freq[activity_map[act_no]][num_act[activity_map[act_no]]].append(0.0)
        tmp = 0
        for  rec_no in range(0, num_act[activity_map[act_no]]):
            tmp += sensor_freq[activity_map[act_no]][rec_no][sen_no]
    
    sensor_freq[activity_map[act_no]][num_act[activity_map[act_no]]][sen_no] = (float)tmp/(float)num_act[activity_map[act_no]]

'''