# Python wrapper for the HDRVDP image quality estimator
# REST API version, can be used on modern machine connected to a Ubuntu 14 server 
# Scientific Computing
# Elettra Sincrotrone Trieste
# August 2022

import numpy as np

import requests
from npyrequtils import NumpyArrayEncoder, nparray2requestdata, decodepostresponse2nparray

url = "http://localhost:8885"

def calchdrvdpremote(img1, img2, ur=url):
    totimg = np.asarray([img1, img2]).astype(np.float32)
    # encode array
    encodedNumpyData = nparray2requestdata(totimg)
    # get processed data as a post request
    x = requests.post(url, data=encodedNumpyData)
    # decode the post request reply
    finalNumpyArray = decodepostresponse2nparray(x)
    return finalNumpyArray


if __name__ == '__main__':
    from skimage import data, img_as_float
    import matplotlib.pyplot as plt

    img1 = (data.camera()).astype(np.float32)
    img2 = (img1**2).astype(np.float32)

    img1 = img1/img1.max()
    img2 = img2/img2.max()

    finalNumpyArray = calchdrvdpremote(img1, img2)
    
    print('end')
