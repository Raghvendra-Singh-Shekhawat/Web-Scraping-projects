# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 16:30:40 2023

@author: raghvendra singh
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Chrome('E:\web development\chromedriver.exe')
driver.get('https://twitter.com/i/flow/login')
time.sleep(2)

celebrity = 'Ryan Renyolds'

driver.maximize_window() # I always maximize the window

login_username = driver.find_element('xpath','//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div/div/div/div[5]/label/div/div[2]/div/input')
login_username.send_keys('Raghven9')
login_username.send_keys(Keys.ENTER)

time.sleep(5)

password = driver.find_element(by = By.XPATH, value='//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div/label/div/div[2]/div[1]/input')
password.send_keys('qazwsxedc123@')
password.send_keys(Keys.ENTER)

time.sleep(10)

# WebDriverWait(driver, 10).until(EC, presence_of_element_located(By.XPATH, '//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input'))

search = driver.find_element('xpath','//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[2]/div/div[2]/div/div/div/div[1]/div/div/div/form/div[1]/div/div/div/label/div[2]/div/input')
search.send_keys(celebrity)
search.send_keys(Keys.ENTER)
time.sleep(2)

people = driver.find_element('xpath','//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[1]/div[1]/div[2]/nav/div/div[2]/div/div[3]/a/div/div/span').click()
time.sleep(2)

profile = driver.find_element(by = By.XPATH, value='//*[@id="react-root"]/div/div/div[2]/main/div/div/div/div[1]/div/div[3]/div/section/div/div/div[1]/div/div/div/div/div[2]/div[1]/div[1]/div/div[1]/a/div/div[1]/span/span').click()
time.sleep(2)

soup = BeautifulSoup(driver.page_source, 'lxml')
postings = soup.find_all('div', class_='css-1dbjc4n r-1igl3o0 r-qklmqi r-1adg3ll r-1ny4l3l')
tweets = []

while True:
    for post in postings:
        tweets.append(post.text)
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight)')
    time.sleep(1)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    postings = soup.find_all('div', class_='css-1dbjc4n r-1igl3o0 r-qklmqi r-1adg3ll r-1ny4l3l')
    tweets2 = list(set(tweets))
    if len(tweets2) >= 200:
        break
    
new_tweets = []
for i in tweets2:
    if 'free' in i:
        new_tweets.append(i)
