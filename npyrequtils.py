# library for REST API numpy data handling
# Scientific Computing
# Elettra Sincrotrone Trieste
# August 2022

import numpy as np
import json


class NumpyArrayEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(NumpyArrayEncoder, self).default(obj)


def nparray2requestdata(dataarray):
    numpyData = {"array": dataarray}
    return json.dumps(numpyData, cls=NumpyArrayEncoder)


def requestdata2nparray(request_data):
    decodedArrays = json.loads(request_data)
    return np.asarray(decodedArrays["array"])


def decodepostresponse2nparray(x):
    return np.asarray(json.loads(x._content)['array'])
