from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

def visualize(data, label):
    draw_data = []
    for i in range(10):
        draw_data.append([])
    for i in range(len(label)):
        draw_data[label[i]].append(data[i])

    
    return_val = []
    for i in range(10):
        
        sub_sum = 0
        return_val.append([])
        for k in range(27):
            for j in range(len(draw_data[i])):
                #print(''+str(i)+' '+str(j)+' '+str(k))
                sub_sum += draw_data[i][j][k]
            
            return_val[i].append(sub_sum/27.0) 
            sub_sum = 0
    
    
    x = np.arange(0, 27, 1)
    for i in range(10):
        plt.plot(x, return_val[i])
    plt.legend(['act1', 'act2', 'act3', 'act4', 'act5', 'act6', 'act7', 'act8', 'act9', 'act10'], loc='upper left')
    plt.show()

    return return_val