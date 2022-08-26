# Python wrapper for the HDRVDP image quality estimator
# REST API version, the computation server
# Scientific Computing
# Elettra Sincrotrone Trieste
# August 2022

from flask import Flask, request, jsonify
import numpy as np

from hdrvdpwrap import calchdrvdp
from npyrequtils import NumpyArrayEncoder, nparray2requestdata, requestdata2nparray


app = Flask(__name__)

@app.route('/', methods=['POST'])
def processpost():
    request_data = request.get_data()
    
    # get data from the client
    inputarray = requestdata2nparray(request_data)
    print('rx array shape', inputarray.shape)

    # calc hdrvdp index
    out = calchdrvdp(inputarray[0], inputarray[1],verbose=True)

    # encode processed data
    encodedNumpyData = nparray2requestdata((out[-1]).astype(np.float32))

    return encodedNumpyData

if __name__ == "__main__":
    app.run(debug=True, host="localhost", port=8885)
