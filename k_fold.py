from sklearn.model_selection import StratifiedKFold
import pkg_model
import keras
from generate import generateCM

def cross_validate(data, labels, sensor_num=27, act_num=10, epochs=200, folds=3):

	nn_model = pkg_model.createModel(shape=sensor_num)
	
	skf = StratifiedKFold(n_splits=folds)
	for train_index, test_index in skf.split(data, labels):
		X_train, X_test = data[train_index], data[test_index]
		y_train, y_test = labels[train_index], labels[test_index]
		y_train = keras.utils.to_categorical(y_train, num_classes=act_num)
		y_test = keras.utils.to_categorical(y_test, num_classes=act_num)
		#nn_model = pkg_model.createModel(shape=sensor_num)
		his = nn_model.fit(X_train, y_train, epochs=epochs,validation_data=(X_test, y_test), batch_size=10)
		confusion_matrix = generateCM(nn_model.predict(data), keras.utils.to_categorical(labels, num_classes=act_num)) 
		for i in range(len(confusion_matrix)):
			print(confusion_matrix[i])