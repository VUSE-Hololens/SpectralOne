"""
NDVI
Calculates NDVI
Developed for Remote Sensing TIPs Project (2019)
Mark Scherer
"""

import numpy as np
from PIL import Image

# returns img object given filepath
def read_img(filepath):
    return Image.open(filepath)

# given img object returns tuple of pixels, exif data
def parse_img_data(img):
    pixels = list(img.getdata())
    exif = img._getexif()
    return pixels, exif

# creates grayscale img object from 8-bit array
def create_img_grayscale(width, height, data):
    img = Image.new('L', (width, height))
    img.putdata(data)
    return img

# given img object, writes to filepath
def write_img(img, filepath):
    img.save(filepath)

# shows passed image in window
def show_img(img):
    img.show()

# given exif tag as string, returns tag number
def exif_key(tag):
    if tag == 'width':
        return 0x0100
    if tag == 'height':
        return 0x0101
    if tag == 'iso':
        return 0x8827
    if tag == 'ev':
        return 0x829a
    return None

# given rgb & nir img objects, returns ndvi img object
def calc_ndvi(rgb_img, nir_img):
    # parse img data
    rgb_pixels, rgb_exif = parse_img_data(rgb_img)
    nir_pixels, nir_exif = parse_img_data(nir_img)
    
    if (len(rgb_pixels) != len(nir_pixels)):
        print('Error calculating NDVI: image pixels counts not equal.')
        return None
    
    # calculate ndvi
    ndvi = [None] * len(rgb_pixels)
    i = 0
    while i < len(ndvi):
        r = float(rgb_pixels[i][0])
        g = float(rgb_pixels[i][1])
        b = float(rgb_pixels[i][2])
        nir1 = float(nir_pixels[i][0])
        nir2 = float(nir_pixels[i][2])

        r_sep = 1.150*r - 0.110*g - 0.034*b
        nir_sep = -0.341*nir1 + 2.436*nir2

        if r_sep < 0:
            r_sep = 0
        if nir_sep < 0:
            nir_sep = 0

        r_norm = r_sep * rgb_exif[exif_key('ev')][1] / (rgb_exif[exif_key('iso')] / 100);
        nir_norm = nir_sep * nir_exif[exif_key('ev')][1] / (nir_exif[exif_key('iso')] / 100);

        if nir_norm == 0 and r_norm == 0:
            ndvi_tmp = 0
        else:
            ndvi_tmp = (2.700*nir_norm - r_norm) / (2.700*nir_norm + r_norm);
        ndvi[i] = (ndvi_tmp + 1) / 2 * 255
        i += 1

    return create_img_grayscale(rgb_img.size[0], rgb_img.size[1], ndvi)