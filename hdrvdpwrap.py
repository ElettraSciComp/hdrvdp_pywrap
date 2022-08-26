
"""
Python wrapper for the HDRVDP image quality estimator

Scientific Computing
Elettra Sincrotrone Trieste
August 2022

It requires:
Ubuntu 14.04, pfstools-1.8.5-1ubuntu3 (trusty), libpfs-1.2-0, pfstmo-1.4-1
hdrvdp-1.7.1 from sourceforce

"""


import tempfile
import numpy as np
import subprocess
import cv2
from skimage import io

# png color code from https://groups.google.com/g/hdrvdp/c/lXjqxkYLw0g
# <25% gray
# 50% green
# 62.5% yellow
# 100% magenta

def calchdrvdp(img1, img2,verbose=False):
    assert(img1.size == img2.size); assert(len(img1.shape) == 2); assert(len(img2.shape) == 2);

    with tempfile.TemporaryDirectory() as tmpdirname:
        img1path, img2path = f'{tmpdirname}/img1.hdr', f'{tmpdirname}/img2.hdr'
        outcsv, outraw, outpng = f'{tmpdirname}/outcsv.csv', f'{tmpdirname}/rawout.raw', f'{tmpdirname}/vdpout.png'

        cv2.imwrite(img1path, img1.astype(np.float32)); cv2.imwrite(img2path, img2.astype(np.float32))

        command = f"vdp {img1path} {img2path} -o {outraw} -s {outcsv}"
        try:
            output = subprocess.check_output(command, stderr=subprocess.STDOUT, cwd=tmpdirname, shell=True).decode()
            if verbose: print(output)

            # get color mapped mask
            png = io.imread(outpng)

            # get percentages
            perc = np.genfromtxt(outcsv, delimiter=',')

            # get raw map
            with open(outraw, "rb") as f:
                f.seek(-int(4*img1.size), 2)
                rawimg = np.fromfile(f, dtype=np.float32).reshape(img1.shape)
            
            return True, perc, png, rawimg

        except subprocess.CalledProcessError as e:
            output = e.output.decode()
            return False, output

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    from skimage import data, img_as_float

    img1 = (data.camera()).astype(np.float32)
    img2 = (img1**2).astype(np.float32)
    #img1 = img1[:345,:] # check also fancy shapes
    #img2 = img2[:345,:]

    out = calchdrvdp(img1, img2)

    plt.figure(dpi=300);
    plt.subplot(121); plt.imshow(out[-1]); plt.colorbar(fraction=0.046); plt.title('Raw mask')
    plt.subplot(122); plt.imshow(out[-2]); plt.colorbar(fraction=0.046); plt.title('Color coded mask')
    plt.suptitle('hdrvdp output'); plt.tight_layout(); plt.show()
    
    print('end')
