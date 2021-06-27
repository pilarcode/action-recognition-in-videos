from src import *
from src.ar import ActionRecognition



if __name__ == "__main__":

	ar = ActionRecognition()
	ar.loadTestDataset()
	ar.loadModel()
	loss, accuracy = ar.evaluate()
	print("[ INFO TEST] loss:{} acc:{}".format(loss, accuracy))


	