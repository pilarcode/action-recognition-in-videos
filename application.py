from tensorflow.python.ops.gen_lookup_ops import lookup_table_export
from src import *
from flask import Flask, jsonify,request
from src.ar import ActionRecognition

application =  Flask(__name__)

@application.route('/',methods=['GET'])
def main():
	return "Serivice is up",200


@application.route('/api/v1/predict',methods=['POST'])
def predict():
	params = request.get_json()
	url = params['url']

	ar = ActionRecognition()
	ar.loadModel()
	label, confidence, probabilities= ar.predict(url)
	result = {}
	result['confidence'] = confidence
	result['label'] = label
	result['probabilities'] = probabilities
	result['url'] = url
	return jsonify(result),200



@application.route('/api/v2/predict',methods=['POST'])
def predictAvg():
	params = request.get_json()
	url = params['url']
	ar = ActionRecognition()
	ar.loadModel()
	label, confidence, probabilities= ar.predictAvg(url)
	result = {}
	result['confidence'] = confidence
	result['label'] = label
	result['probabilities'] = probabilities
	result['url'] = url
	return jsonify(result),200



if __name__ == "__main__":
	application.run(host="0.0.0.0", port=80, debug = True)

	