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

class SpectralControl:

    def __init__(self):
        # controls
        self.session_name = "python_test"
        self.image_directory = 'images'

        # constants
        self.sentera_url = "http://192.168.43.1:8080/"
        self.download_extension = "sdcard?path=/snapshots/"

        # main
        self.browser_main = sentera.selenium_start()
        sentera.sentera_start(self.sentera_url, self.browser_main, self.session_name)

        self.red_id = ""
        self.nir_id = ""
        self.rgb_img = None
        self.nir_img = None

    def __del__(self):
        sentera.sentera_stop(self.browser_main)
        sentera.selenium_stop(self.browser_main)

    def getImg(self):
        new_session_name, new_red_id, new_nir_id = sentera.sentera_poll(self.browser_main)
        new_ndvi = True

        if new_session_name != "" and new_session_name != self.session_name:
            self.session_name = new_session_name

        if new_red_id != self.red_id:
            self.red_id = new_red_id
            filename = sentera.sentera_download(self.sentera_url + self.download_extension + self.session_name + "/" + self.red_id, self.red_id, self.image_directory)
            self.rgb_img = ndvi.read_img(filename)
        else:
            new_ndvi = False

        if new_nir_id != self.nir_id:
            self.nir_id = new_nir_id
            filename = sentera.sentera_download(self.sentera_url + self.download_extension + self.session_name + "/" + self.nir_id, self.nir_id, self.image_directory)
            self.nir_img = ndvi.read_img(filename)
        else:
            new_ndvi = False

        if new_ndvi:
            ndvi_filepath = ndvi_filepath = 'images/NDVI/' + self.red_id[self.red_id.find('/')+1:]
            ndvi_img = ndvi.calc_ndvi(self.rgb_img, self.nir_img)
            ndvi.write_img(ndvi_img, ndvi_filepath)
            print("Wrote NDVI image to: {0}".format(ndvi_filepath))
            return ndvi_filepath

        return ""
