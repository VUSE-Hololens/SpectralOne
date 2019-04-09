"""
Sentera
Interfaces with Sentera.
Currently scrapes web interface with chromium browser.
Developed for Remote Sensing TIPs Project (2019)
Mark Scherer
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import wget_custom

# starts Sentera session
def sentera_start(sentera_ip, browser, session_name):
    browser.get(sentera_ip)

    session_name_field = browser.find_element_by_id('session_name')
    session_name_field.clear()
    session_name_field.send_keys(session_name)

    start_button = browser.find_element_by_id('btnStart')
    start_button.click()

# stops Sentera session
def sentera_stop(browser):
    stop_button = browser.find_element_by_id('btnStop')
    stop_button.click()

# returns name of most recent R and NIR images
# note: Sentera session should already be started
def sentera_poll(browser):
    soup = selenium_get(browser)

    session_name = soup.find(id="session").get_text()
    red_id = soup.find(id="recent_0").get_text()
    nir_id = soup.find(id="recent_1").get_text()

    return session_name, red_id, nir_id

# downloads url to local folder
def sentera_download(url, filename, directory=None):
    return wget_custom.download(url, filename, out=directory, bar=None)
    



#  ----------  Helper Methods  ----------  #

# return selenium browser to pass to other methods
def selenium_start():
    return webdriver.Chrome()

def selenium_stop(browser):
    browser.quit()

# selenium: uses chromium browser
def selenium_get(browser, url=None):
    if url is not None:
        browser.get(url)
    return BeautifulSoup(browser.page_source, 'html.parser')