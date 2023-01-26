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

#####################################################################################

#Code below sends an email to whomever through python
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email import encoders

#Input the email account that will send the email and who will receiving it
sender = 'account@gmail.com'
receiver = 'account@gmail.com'

#Creates the Message, Subject line, From and To
msg = MIMEMultipart()
msg['Subject'] = 'New Jobs on Indeed'
msg['From'] = sender
msg['To'] = ','.join(receiver)

#Adds a csv file as an attachment to the email (indeed_jobs.csv is our attahced csv in this case)
part = MIMEBase('application', 'octet-stream')
part.set_payload(open('A/File/Path/indeed_jobs.csv', 'rb').read())
encoders.encode_base64(part)
part.add_header('Content-Disposition', 'attachment; filename ="indeed_jobs.csv"')
msg.attach(part)

#Will login to your email and actually send the message above to the receiver
s = smtplib.SMTP_SSL(host = 'smtp.gmail.com', port = 465)
s.login(user = 'account@gmail.com', password = 'input your password')
s.sendmail(sender, receiver, msg.as_string())
s.quit()