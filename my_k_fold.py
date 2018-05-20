import read5
import process
import pkg_model
import keras
import numpy as np
from sklearn.model_selection import StratifiedKFold
from importlib import reload
import matplotlib.pyplot as plt

def __main__():
    reload(read5)
    data, label = read5.readData()

    for i in range(len(data)):
        data[i] = process.normalization(data[i])

    # for selecting folds to train or validate
    index = [[1,2,0], [0,2,1],[0,1,2]]
    
    f, axarr = plt.subplots(3, sharex=True)
    f.suptitle('model accuracy')
    # f.xlabel('epochs')
    # f.ylabel('accuracy')
    f.legend(['acc', 'val_acc'], loc='lower right')
    model = pkg_model.createModel(shape=27) 
    for i in range(3):
        X_train = np.concatenate((data[index[i][0]], data[index[i][1]]))
        y_train = keras.utils.to_categorical(np.concatenate((label[index[i][0]], label[index[i][1]])), num_classes=10)
        X_test = data[index[i][2]]
        y_test =keras.utils.to_categorical(label[index[i][2]], num_classes=10)
        his = model.fit(X_train, y_train, epochs=200, validation_data=(X_test, y_test), batch_size=10)
        
        axarr[i].plot(his.history['acc'])
        axarr[i].plot(his.history['val_acc'])
        
        # plt.ylabel('accuracy')
        # plt.xlabel('epochs')
        # plt.legend(['acc', 'val_acc'], loc='lower right')
        # plt.show()