"""
dev
useful fo debugging things
Developed for Remote Sensing TIPs Project (2019)
Mark Scherer
"""

import ndvi

rgb_filepath = 'images/RGB/IMG_00001.jpg'
nir_filepath = 'images/NIR/IMG_00001.jpg'
ndvi_filepath = 'images/ndvi.jpg'

# read images from file
rgb_img = ndvi.read_img(rgb_filepath)
nir_img = ndvi.read_img(nir_filepath)

# calculate ndvi
ndvi_img = ndvi.calc_ndvi(rgb_img, nir_img)

# save ndvi img
ndvi.write_img(ndvi_img, ndvi_filepath)
