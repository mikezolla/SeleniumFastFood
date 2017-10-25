

__author__ = 'Michael'

#The sys module provides access to some variables used or maintained by the interpreter and to functions that interact 
#strongly with the interpreter. It is always available. sys.exit from Python. This is implemented by raising the SystemExit 
#exception, so cleanup actions specified by finally clauses of try statements are honored, and it is possible to intercept
#the exit attempt at an outer level.
 
import sys

#Pickling is a way to convert a python object (list, dict, etc.) into a character stream.  It is used for serializing 
#and de-serializing a Python object structure.
import pickle

# The signal module provides mechanisms to use signal handlers in Python. The signal.signal() function allows defining
# custom handlers to be executed when a signal is received.
import signal

from bs4 import BeautifulSoup

#urllib is a package that collects several modules for working with URLs
import urllib
# The CookieJar class stores HTTP cookies. It extracts cookies from HTTP requests, and returns them in HTTP responses
import http.cookiejar

from selenium import webdriver

# Set of supported locator strategies.
from selenium.webdriver.common.by import By


# An explicit wait is a code you define to wait for a certain condition
# to occur before proceeding further in the code. The extreme case of this is time.sleep(), 
# which sets the condition to an exact time period to wait. There are some convenience methods
# provided that help you write code that will wait only as long as required. WebDriverWait in 
# combination with ExpectedCondition is one way this can be accomplished.
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# WebDriver’s support classes include one called a “Select”. In this instance, it's important
# “toggle” the state of the drop down, and you can use “setSelected” to set something like an OPTION tag selected.
from selenium.webdriver.support.ui import Select

# Thrown when a reference to an element is now "stale".
# Stale means the element no longer appears on the DOM of the page. 
# In this instance an element may have been removed and re-added to the screen, since it was located.
from selenium.common.exceptions import StaleElementReferenceException


import time
import csv

driver = webdriver.Chrome()

driver. get("http://www.fastfoodmenuprices.com/papa-johns-prices/")
options = webdriver.ChromeOptions()
options.add_argument("--user-agent=New User Agent")
driver = webdriver.Chrome(chrome_options=options)

#csv_file = open("pizza_price.csv", "wb")
#writer = csv.writer(csv_file)
#writer.writerow(['Medium', 'Large', 'Extra_Large'])

output_dir='/Users/michaelzolla/Desktop/FastFood_Scrape/PapaJohnsData/'





hdr = {
#    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
    'Accept-Encoding': 'none',
    'Accept-Language': 'en-US,en;q=0.8',
    'Connection': 'keep-alive'}
#page=urllib.Request(url, headers=hdr)

#Pizza Hut
#keywords=['Personal$','Medium$','Large$']

#Domino's
#keywords=['Small (10")$','Medium (12")$','Large (14")$','X-Large (16")$']
keywords=['Medium$','Large$','Extra Large$']
def sigint(signal, frame):
    sys.exit(0)

class Scraper(object):
    def __init__(self):
        self.url = 'http://www.fastfoodmenuprices.com/papa-johns-prices/'
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1120, 550)

    #--- STATE -----------------------------------------------------
    def get_state_select(self):
        path = '//select[@id="variation-tablepress-31"]'
        state_select_elem = self.driver.find_element_by_xpath(path)
        state_select = Select(state_select_elem)
        return state_select

    def select_state_option(self, value, dowait=True):
        '''
        Select state value from dropdown. Wait until district dropdown
        has loaded before returning.
        '''
        #path = '//select[@id="variation-tablepress-32"]'
        path = '//select[@id="variation-tablepress-31"]'
        district_select_elem = self.driver.find_element_by_xpath(path)

        def district_select_updated(driver):
            try:
                district_select_elem.text
            except StaleElementReferenceException:
                return True
            except:
                pass

            return False

        state_select = self.get_state_select()
        state_select.select_by_value(value)

        return self.get_state_select()





    def load_page(self):
        self.driver.get(self.url)

        def page_loaded(driver):
            path = '//select[@id="variation-tablepress-31"]'
            return driver.find_element_by_xpath(path)

        wait = WebDriverWait(self.driver, 10)
        wait.until(page_loaded)

    def scrape(self):
        def states():
            state_select = self.get_state_select()
            state_select_option_values = [
                '%s' % o.get_attribute('value')
                for o
                in state_select.options[1:]
            ]

            for v in state_select_option_values:
                state_select = self.select_state_option(v)
                self.driver.page_source
                text=BeautifulSoup(self.driver.page_source, "html.parser").get_text()
                meta_prices=[]
                for keyword in keywords:
                    prices = []
                    counter=text.count(keyword)
                    for z in range(counter):
                        prices.append(text.rsplit(keyword, z+1)[1].splitlines()[0])
                    prices=[float(price) for price in prices]
                    meta_prices.append(prices)
                yield (state_select.first_selected_option.text,meta_prices)



        self.load_page()

       

        for j,state in enumerate(states()):
            w = open(output_dir+str(j)+'.pkl', "wb")
            pickle.dump(state, w)
            w.close()
            print(state)
        #print(states)
        #csv_file.close()
        #driver.close()

        #w.close()

if __name__ == '__main__':
    signal.signal(signal.SIGINT, sigint)
    scraper = Scraper()
    scraper.scrape()