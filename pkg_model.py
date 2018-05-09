from keras.models import Sequential
from keras.layers import Dense, Activation

def createModel(shape=27):

	model = Sequential([
    Dense(32, input_shape=(shape,)),
    Activation('relu'),
    Dense(10),
    Activation('softmax'),
	])
	
	model.compile(optimizer='rmsprop',
								loss='categorical_crossentropy',
								metrics=['accuracy'])
	
	return model