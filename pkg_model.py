from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras import regularizers
from keras.optimizers import sgd

def createModel(shape=27):

	model = Sequential([
    Dense(32, input_shape=(shape,), activity_regularizer=regularizers.l2(0.01)),
                
    Activation('relu'),
	# Dropout(0.5),
	# Dense(64),
	# Activation('relu'),
	# Dropout(0.5),
    Dense(10),
    Activation('softmax'),
	# Dropout(0.5),
	])
	
	# model = Sequential()
	# # Dense(64) is a fully-connected layer with 64 hidden units.
	# # in the first layer, you must specify the expected input data shape:
	# # here, 20-dimensional vectors.
	# model.add(Dense(32, activation='relu', input_shape=(shape,)))
	# model.add(Dropout(0.5))
	# model.add(Dense(64, activation='relu'))
	# model.add(Dropout(0.5))
	# model.add(Dense(10, activation='softmax'))

	model.compile(optimizer='sgd',
				loss='categorical_crossentropy',
				metrics=['accuracy'])
	
	return model