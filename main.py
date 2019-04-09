"""
SpectralOne
Live-feed NDVI using Sentera camera.
Note: Only works when connected to Sentera 066's wifi network.
Developed for Remote Sensing TIPs Project (2019)
Mark Scherer
"""

import sentera
import ndvi

import time
import os
import sys

# controls
session_name = "python_test"
image_directory = 'images'

# constants
sentera_url = "http://192.168.143.141/"
download_extension = "sdcard?path=/snapshots/"

# main
browser_main = sentera.selenium_start()
sentera.sentera_start(sentera_url, browser_main, session_name)

red_id = ""
nir_id = ""
rgb_img = None
nir_img = None
while True:
    new_session_name, new_red_id, new_nir_id = sentera.sentera_poll(browser_main)
    new_ndvi = True

    if new_session_name != "" and new_session_name != session_name:
        session_name = new_session_name

    if new_red_id != red_id:
        red_id = new_red_id
        filename = sentera.sentera_download(sentera_url + download_extension + session_name + "/" + red_id, red_id, image_directory)
        rgb_img = ndvi.read_img(filename)
    else:
        new_ndvi = False

    if new_nir_id != nir_id:
        nir_id = new_nir_id
        filename = sentera.sentera_download(sentera_url + download_extension + session_name + "/" + nir_id, nir_id, image_directory)
        nir_img = ndvi.read_img(filename)
    else:
        new_ndvi = False

    if new_ndvi:
        ndvi_filepath = 'images/NDVI/' + red_id[red_id.find('/')+1:]
        ndvi_img = ndvi.calc_ndvi(rgb_img, nir_img)
        ndvi.write_img(ndvi_img, ndvi_filepath)
        print("Wrote NDVI image to: {0}".format(ndvi_filepath))

    time.sleep(0.1)


sentera.sentera_stop(browser_main)
sentera.selenium_stop(browser_main)