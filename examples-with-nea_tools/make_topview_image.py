"""
Do simple control of topview camera.
1. Set zoom
2. Save high resolution screenshot as png on desktop
3. Get live stream image and save with matplotlib
"""

import os
from nea_tools import maincamera
import matplotlib.pyplot as plt

# Zoom
maincamera.change_zoom(1)

# Save high resolution image
fname = os.path.join(os.environ['HOME'],'Desktop','TopView_Image.png')
maincamera.save_big_picture(fname)

# Get camera live feed as RGBA and process with matplotlib
fname2 = os.path.join(os.environ['HOME'],'Desktop','TopView_Image_Stream.png')
with maincamera.CameraStream() as camera:
    plt.imsave(fname2,camera.image)