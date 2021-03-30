#!/usr/bin/env python
# coding=utf-8
'''
@author: Zuber
@date:  2021/2/26 11:56
'''
import pickle

from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

TIME_OUT = 12


class FireFoxBase(object):
    def __init__(self, url):
        self.url = url
        fp = webdriver.FirefoxProfile(
            r'C:/Users/Administrator/AppData/Roaming/Mozilla/Firefox/Profiles/gvavpdan.default')
        self.driver = webdriver.Firefox(firefox_profile=fp, executable_path='../driver/geckodriver.exe')
        self.driver.get(url)
        self.driver.refresh()

    def save_cookie(self):
        '''保存cookie'''
        # 将cookie序列化保存下来
        pickle.dump(self.driver.get_cookies(), open("cookies.pkl", "wb"))

    def set_cookie(self):
        '''往浏览器添加cookie'''
        '''利用pickle序列化后的cookie'''
        try:
            cookies = pickle.load(open("cookies.pkl", "rb"))
            for cookie in cookies:
                if isinstance(cookie.get('expiry'), float):
                    cookie['expiry'] = int(cookie['expiry'])
                self.driver.add_cookie(cookie)
        except Exception as e:
            print(e)

    def wait_on_element_text(self, by_type, element, text, timeout=0.01):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.text_to_be_present_in_element(
                    (by_type, element), text)
            )
        except:
            return False

    def wait_on_element_located(self, by_type, element, timeout=1):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((by_type, element)))
        except:
            pass

    def wait_on_element_to_be_clickable(self, by_type, element, timeout=1):
        try:
            return WebDriverWait(self.driver, timeout).until(
                EC.element_to_be_clickable((by_type, element)))
        except:
            pass

    def save_screenshot(self, element: WebElement, filename):
        screenshot = element.screenshot(filename)
        return screenshot


if __name__ == '__main__':
    base = FireFoxBase("http://data.10jqka.com.cn/funds/hyzjl/field/tradezdf/order/desc/page/1/ajax/1/free/1/")
    source = base.driver.page_source
    print(f'={source}')
