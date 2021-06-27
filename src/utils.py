import cv2
import os
import numpy as np
from pytube import YouTube


def getAllFrames(video_path,img_size=64):
    frames = []
    print("video_path:{}".format(video_path))
    cap = cv2.VideoCapture(video_path)
    count = 1
    while True:
        success, image = cap.read() 
        if success:
            image = cv2.resize(image, (img_size, img_size))
            frames.append(image)
            count += 1
        else:
            break
    #print("frames:{}".format(len(frames)))
    return frames


def getSeqFrames(video_path,seq_len,img_height,img_width):
    frames= []
    cap = cv2.VideoCapture(video_path)

    count = 1
    while count < seq_len: 
        success, image = cap.read() 
        if success:
            image = cv2.resize(image, (img_height, img_width))
            frames.append(image)
            count += 1
        else:
            break
    return frames


def createDataset(dir,seq,classes_list,IMG_SIZE=64,MAX_EXAMPLES_PER_VIDEO=20):
    X = [] # frames
    Y = [] # labels

    for c in classes_list:
        files = os.listdir(os.path.join(dir, c))
        
        for file in files: 
            frames = getAllFrames(os.path.join(os.path.join(dir, c), file)) 
          
            # more samples per video 
            batches = int( len(frames)  // seq)
            niters = 0
            while  niters < batches and niters < MAX_EXAMPLES_PER_VIDEO:
                pos_ini = int(niters * seq)
                pos_fin = pos_ini + seq
                X.append(frames[pos_ini:pos_fin])
          
                #labels to one-hot encoding
                y = [0]*len(classes_list)
                y[classes_list.index(c)] = 1
                Y.append(y)

                niters+=1
     
    X = np.asarray(X)
    Y = np.asarray(Y)
    return X, Y


def createExamples(frames,seq,classes_list):

    X = [] # frames
    Y = [] # labels

    batches = int( len(frames)  // seq)
    niters = 0
    while  niters < batches:
        pos_ini = int(niters * seq)
        pos_fin = pos_ini + seq
        X.append(frames[pos_ini:pos_fin])
    

        #labels to one-hot encoding
        y = [0]*len(classes_list)
        y[classes_list.index(c)] = 1



def downloadYouTube(url):
    destination =f'{os.getcwd()}\\tmp'
    try: 
        yt = YouTube(url) 
    except: 
        print("Connection Error") 
    try: 
        yt.streams.filter(progressive=True, file_extension='mp4').first().download(output_path=destination, filename='sample')
    except: 
        print("Some Error downloading!")  
    return os.path.join(destination,'sample.mp4')


def mostFrequent(List):
	counter = 0
	num = List[0]
	for i in List:
		curr_frequency = List.count(i)
		if(curr_frequency> counter):
			counter = curr_frequency
			num = i
	return num

def highConfidence( listOfDictionaries):
    max_confidence = 0
    for dictionary in listOfDictionaries:
        for x, y in dictionary.items():
            if x == "confidence" and y > max_confidence:
                max_confidence = y
    return max_confidence