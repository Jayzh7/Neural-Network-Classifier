def train_eval_model(model, train_data, train_label, test_data, test_label, epochs=50, batch_size=32):
	model.fit(train_data, train_label, epochs=epochs, validation_data=(test_data, test_label), batch_size = batch_size)
	