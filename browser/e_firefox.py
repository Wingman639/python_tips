import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
import time

browser = webdriver.Firefox() # Get local session of firefox
browser.get("http://news.sina.com.cn/c/2013-07-11/175827642839.shtml ") # Load page
time.sleep(5) # Let the page load
try:
    element = browser.find_element_by_xpath("//span[contains(@class,'f_red')]") # get element on page
    print element.text # get element text
except NoSuchElementException:
    assert 0, "can't find f_red"
browser.close()