import numpy as np
'''
27 Sensors are used in total. Their data will be 
stored in a list with index being id. 
i.e. M001 will be store in index 1
'''
def readData(): 
    read_file = open("cairo.data")

    next = read_file.readline()
    # print the line num in debug mode
    line_num = 1
    activity_on = False
    activity_map = {0: 'Bed_to_toilet', 1: 'Breakfast', 2: 'Bed', 3: 'C_work', 
                        4: 'Dinner', 5: 'Laundry', 6: 'Leave_home', 7: 'Lunch',
                        8: 'Night_wandering', 9: 'R_medicine'}

    # dict to store all sensor active level of all activities.
    sensor_freq = {}
    # init
    for i in range(0,10):
        sensor_freq[activity_map[i]] = []

    # cursor to record number of each activities that have been processed
    num_act = {}
    # init all value to be 0
    for i in range(0, 10):
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
                for j in range(0, 27):
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


    X_data = []
    X_label = []
		
    for key, value in activity_map.items():
        for j in range(num_act[value]):
            X_data.append(sensor_freq[value][j])
            X_label.append(key)
    data = np.array(X_data)
    label = np.array(X_label)
		
    return data, label

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