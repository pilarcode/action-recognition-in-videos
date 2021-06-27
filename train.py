from src import *
from src.ar import ActionRecognition



if __name__ == "__main__":

	ar = ActionRecognition()
	ar.loadTrainDatasets()
	ar.createModel()
	ar.compile()
	history = ar.fit()
	ar.saveModel()
	
	loss = history['loss']
	val_loss = history['val_loss']
	accuracy = history['accuacy']
	val_accuracy = history['val_accuracy']
	print("[INFO TRAIN] loss:{} val_loss:{} acc:{} val_acc:{}".format(loss,val_loss, accuracy, val_accuracy))


	