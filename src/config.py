import yaml
import os


class Configuration:

    def __init__(self):
        self.variables = self.load()

    def load(self):
        # load yaml variables 
        dir = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.join(dir,'config.yaml')
        with open(filename) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
        return data

    def getLabels(self):
       return self.variables['labels']

    def getModel(self):
        return self.variables['model']

    def getFrameSequenceLength(self):
       return self.variables['seq_len']
    
    def getFrameDimension(self):
       return self.variables['img_height'],self.variables['img_width']
