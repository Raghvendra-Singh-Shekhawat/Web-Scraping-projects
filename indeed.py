# -*- coding: utf-8 -*-
"""
Created on Sat Jan 21 21:41:41 2023

@author: raghvendra singh
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Chrome('E:\web development\chromedriver.exe')
driver.get('https://in.indeed.com/')
time.sleep(3)

job_title = driver.find_element('xpath','//*[@id="text-input-what"]')
job_title.send_keys('data analyst')
job_title.send_keys(Keys.ENTER)
time.sleep(3)



df = pd.DataFrame({'Link':[''],'Title':[''],'Company':[''],'Location':[''], 'Salary':[''],'Days':['']})
while True:
    soup = BeautifulSoup(driver.page_source, 'lxml')

    posting = soup.findAll('div', class_='job_seen_beacon')
    
    for post in posting:
        link = post.find('a', class_= 'jcs-JobTitle css-jspxzf eu4oa1w0').get('href')
        links = 'https://in.indeed.com'+ link
        title = post.find('a', class_= 'jcs-JobTitle css-jspxzf eu4oa1w0').text
        company = post.find('span', class_= 'companyName').text
        location = post.find('div', class_= 'companyLocation').text
        days = post.find('span', class_= 'date').text
        try:
            salary = post.find('div', class_= 'metadata salary-snippet-container').text.strip() 
        except:
            salary = 'N/A'
        df = df.append({'Link': links,'Title': title,'Company': company,'Location': location, 'Salary': salary,'Days': days}, ignore_index=True)
    
    try:
        button = soup.find('a', attrs = {'aria-label': 'Next Page'}).get('href')
        driver.get('https://in.indeed.com'+button)
    except:
        break
    
#The code below just sorts the dataframe by posting date
df['Date_num'] = df['Days'].apply(lambda x: x[:2].strip())

def integer(x):
    try:
        return int(x)
    except:
        return x
    
df['Date_num2'] = df['Date_num'].apply(integer)
df.sort_values(by = ['Date_num2','Salary'], inplace = True)  

df = df[['Link', 'Title','Company','Location', 'Salary','Days']]

#exports the dataframe as a csv
df.to_csv('E:\web development\C Tutorial Notes/indeed_jobs.csv')


