import os
import numpy as np
import matplotlib as plt
import tensorflow as tf
from tensorflow.keras.models import  Sequential
from tensorflow.keras.layers import Dropout, Flatten, Dense, ConvLSTM2D, GlobalAveragePooling2D,GlobalMaxPooling2D 
from keras.models import load_model
from keras.optimizers import SGD
from keras.callbacks import EarlyStopping
from src.config import Configuration
from src.utils import createDataset,downloadYouTube,getAllFrames,getSeqFrames,mostFrequent,highConfidence

class ActionRecognition:

    def __init__(self):
        self.config = Configuration()
     
    def loadTrainDatasets(self):
  
        labels = self.config.getLabels()
        seq = self.config.getFrameSequenceLength()

        print("loading trainning dataset")
        self.X_train, self.Y_train = createDataset(os.path.join(os.getcwd(),"dataset", "train"),seq,labels)
        print(self.X_train.shape)
        print(self.Y_train.shape)

        print("loading validation dataset")
        self.X_valid, self.Y_valid  = createDataset(os.path.join(os.getcwd(),"dataset", "valid"),seq,labels)
        print(self.X_valid.shape)
        print(self.Y_valid.shape)
    
    def loadTestDataset(self):
        labels = self.config.getLabels()
        seq = self.config.getFrameSequenceLength()

        print("loading test dataset")
        self.X_test, self.Y_test = createDataset(os.path.join(os.getcwd(),"dataset", "test"),seq,labels)
        print(self.X_test.shape)
        print(self.Y_test.shape)
        
    def createModel(self):
        print("creating the model")
        seq_len  = self.config.getFrameSequenceLength()
        img_height , img_width = self.config.getFrameDimension()
        N  = len(self.config.getLabels())
        model = Sequential()
        model.add(ConvLSTM2D(filters = 64, kernel_size = (3, 3), return_sequences = False, data_format = "channels_last", input_shape = (seq_len, img_height, img_width, 3))) 
        model.add(Dropout(0.2))   
        model.add(GlobalMaxPooling2D())  
        model.add(Flatten())
        model.add(Dense(256, activation="relu"))
        model.add(Dropout(0.2))
        model.add(Dense(N, activation = "softmax"))
        model.summary()
        self.model = model    
    
    def compile(self):
        print("Compiling the model")
        opt = SGD(learning_rate=0.001)
        self.model.compile(loss='binary_crossentropy', optimizer=opt, metrics=["accuracy"])

    def fit(self, epochs=5, batch_size=32):
        print("Fitting the model with train dataset")
        earlystop = EarlyStopping(patience=2)
        callback = [earlystop]
        return  self.model.fit(x = self.X_train, y = self.Y_train, validation_data=(self.X_valid, self.Y_valid),epochs= epochs, batch_size = batch_size, shuffle=True, callbacks=callback, verbose=1)
    
    def saveModel(self):
        print("Saving the model")
        filename =  self.config.getModel()
        path = os.path.join(os.getcwd(),"src",filename)
        self.model.save(path)

    def loadModel(self):
        print("Loading the model")
        filename =  self.config.getModel()
        path = os.path.join(os.getcwd(),"src",filename)
        loaded_model = load_model(path)
        self.model = loaded_model
     
    def evaluate(self):
        loss, accuracy = self.model.evaluate(self.X_test,self.Y_test, verbose=1)
        print("Restored model, accuracy: {:5.2f}%'.format(100 * accuracy)")
        return loss, accuracy

    def predict(self, url): 
        print("downloading video ")
        path = downloadYouTube(url)

        print("get Frames")
        seq = self.config.getFrameSequenceLength()
        img_height,img_width = self.config.getFrameDimension()
        frames = getSeqFrames(path,seq,img_height,img_width)
        frames = np.asarray(frames)
        clases = self.config.getLabels()
        
        print("making predictions")
        model_input = tf.constant(frames, dtype=tf.float32)[tf.newaxis, ...]
        logits = self.model(model_input)
       
        print("decoding results")
        label_id =  np.argmax(logits, axis=1).tolist()[0]
        probabilites = logits.numpy()[0].tolist()
        
        # build response      
        dic_probabilities = {}
        for index, class_name in enumerate(clases):
            dic_probabilities[class_name] = probabilites[index]
        return clases[label_id], probabilites[label_id],dic_probabilities

    def predictAvg(self, url, k=7): 

        print("downloading video ")
        path = downloadYouTube(url)

        seq = self.config.getFrameSequenceLength()
        print("get Frames")
        all = getAllFrames(path)
        all = np.asarray(all)
        clases = self.config.getLabels()

        data =[]
        k_label_id = []  
        print("Rolling averaging  k:{}".format(k))
        batches = int( len(all)  //seq )
        niters = 0
        while niters < k and niters < batches:
            #select sequence of frames 
            pos_ini = int(niters * seq)
            pos_fin = pos_ini + seq
            frames = all[pos_ini:pos_fin]
            # make the prediction of the sequence
            model_input = tf.constant(frames, dtype=tf.float32)[tf.newaxis, ...]
            logits = self.model(model_input)
            # decode the resultas of predicions for the sequence
            label_id =  np.argmax(logits, axis=1).tolist()[0]
            k_label_id.append(label_id)

            #storing extra info
            probabilites = logits.numpy()[0].tolist()
            dic_probabilities = {}
            for index, class_name in enumerate(clases):
                dic_probabilities[class_name] = probabilites[index]

            label = clases[label_id], 
            confidence = probabilites[label_id]     
            print("Rolling averaging  #k:{} says label:{} confidence:{}".format(niters, label, confidence))
            data.append( { "from":pos_ini , "to": pos_fin , "label": label, "confidence": confidence ,"probabilities" : dic_probabilities})
    
            niters+=1

        label_id = mostFrequent(k_label_id)
        confidence = highConfidence(data)
        return clases[label_id],confidence, data