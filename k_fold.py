from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import StandardScaler
from keras.callbacks import EarlyStopping
import pkg_model
import keras
from generate import generateCM
import matplotlib.pyplot as plt

def cross_validate(data, labels, sensor_num=27, act_num=10, epochs=200, folds=3):

	nn_model = pkg_model.createModel(shape=sensor_num)

	# input scaling
	# scaler = StandardScaler()
	# data = scaler.fit_transform(data)

	# Early stopping  
	#early_stop = EarlyStopping(monitor='val_acc', min_delta=0, patience=100, verbose=1, mode='auto')


	sp = []
	i = 0
	skf = StratifiedKFold(n_splits=folds)
	f, axarr = plt.subplots(3, sharex=True, sharey=True)
	f.suptitle('model accuracy')
	f.legend(['acc', 'val_acc'], loc='lower right')
	for train_index, test_index in skf.split(data, labels):
		X_train, X_test = data[train_index], data[test_index]
		y_train, y_test = labels[train_index], labels[test_index]
		y_train = keras.utils.to_categorical(y_train, num_classes=act_num)
		y_test = keras.utils.to_categorical(y_test, num_classes=act_num)
		#nn_model = pkg_model.createModel(shape=sensor_num)
		his = nn_model.fit(X_train, y_train, epochs=epochs,validation_data=(X_test, y_test), batch_size=10)#, callbacks=[early_stop])
		confusion_matrix = generateCM(nn_model.predict(X_test), y_test) 
		for k in range(len(confusion_matrix)):
			print(confusion_matrix[k])
		axarr[i].plot(his.history['acc'])
		axarr[i].plot(his.history['val_acc'])
		# plt.title('model accuracy')
		# plt.ylabel('accuracy')
		# plt.xlabel('epochs')
		# plt.legend(['train1', 'validate1', 'train2', 'validate2', 'train3', 'validate3'], loc='lower right')
		# plt.ylim(ymin=0, ymax=1)
		#sp[i].show
		i += 1
	