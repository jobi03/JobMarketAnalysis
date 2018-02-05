#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  2 13:36:27 2018

@author: jobi03
"""
#%%
from selenium import webdriver
from time import sleep
from timeit import default_timer
from bs4 import BeautifulSoup
import pandas as pd
import re
#%%
start = default_timer()
driver = webdriver.Chrome(executable_path="./chromedriver/chromedriver")
curWindowHndl = driver.current_window_handle
#change main_page depends on the job u search
#main_page = 'https://au.indeed.com/jobs?q=business+analyst&l=Australia'
main_page = 'https://au.indeed.com/jobs?q=business+analyst&l=Australia&start=490'
#main_page = 'https://au.indeed.com/jobs?q=machine+learning&l=Australia'
#main_page = 'https://au.indeed.com/jobs?q=data+analyst&l=Australia'
#main_page = 'https://au.indeed.com/jobs?q=data%20science&l=Australia&start=590'
#main_page = 'https://au.indeed.com/jobs?q=data+scientist&l=Australia'
#main_page = 'https://au.indeed.com/jobs?q=data+engineer&l=Australia'
classes = ['snip','columnField','careerSite','job','events','job-description',
           'cs-atscs-jobdet-rtpane','detail-item','clearfix jobDetailsMainDiv ng-scope',
           'cp_page']
result_page = 1

#%%
jobs = []
locations = []
companies = []
salaries = []
next_btn = []
summaries = []
links = []
timers = []
pages_links = []
#%%
def delete_cookies():
    try:
        driver.delete_all_cookies()
    except:
        pass
    

#%%
def make_soup(page): 
    delete_cookies()
    driver.get(page)
    sleep(2)
    html = driver.page_source
    soups = BeautifulSoup(html, 'html.parser', from_encoding="utf-8")
    return soups
        
           
#%%
def html_to_text(data):        
    # remove the newlines
    data = data.replace("\n", " ")
    data = data.replace("\r", " ")
   
    # replace consecutive spaces into a single one
    data = " ".join(data.split())   
   
    # get only the body content
    bodyPat = re.compile(r'< body[^<>]*?>(.*?)< / body >', re.I)
    for result in re.findall(bodyPat, data):
        data = result
   
    # now remove the java script
    p = re.compile(r'< script[^<>]*?>.*?< / script >')
    data = p.sub('', data)
   
    # remove the css styles
    p = re.compile(r'< style[^<>]*?>.*?< / style >')
    data = p.sub('', data)
   
    # remove html comments
    p = re.compile(r'')
    data = p.sub('', data)
   
    # remove all the tags
    p = re.compile(r'<[^<]*?>')
    data = p.sub('', data)
   
    return data
    
#%%
#scraping summary
def scrape_summary(rows):
    delete_cookies()
    try:
        a = rows.find_element_by_css_selector('a')
        a_id = '#' + a.get_property('id')
        driver.find_element_by_css_selector(a_id).click()
        sleep(1)
        #link = a.get_property('href')
    except: 
        h2 = rows.find_element_by_css_selector('h2')
        h2_id = '#' + h2.get_property('id')
        driver.find_element_by_css_selector(h2_id).click()
        sleep(1)
        #link = a.get_property('href')
    
    driver.switch_to_window(driver.window_handles[1])
    
    
    try:
        h1 = driver.find_element_by_css_selector('h1')
        if h1.text == 'An error has occurred.':
            summ = h1.text
  
    except:       
        try:
            for clas in classes:
                m = driver.find_element_by_class_name(clas)
                summ = html_to_text(m.text)
                break
        except:
            summ = 'Failed to scrape'

        
        
    driver.close()
    driver.switch_to_window(driver.window_handles[0])
    

    return summ
#%%
def check_driver():    
    try:
        if len(driver.switch_to_window(driver.window_handles)) != 1:
            driver.close()
            driver.switch_to_window(driver.window_handles[0])
            
    except:
        pass    

#%%
def scrape_results(soup):
    check_driver()
    for rows in driver.find_elements_by_class_name('row'):
        
        
        try:
            summary = scrape_summary(rows)
            summaries.append(summary)
        except:
            summary = 'Failed to scrape'
            summaries.append(summary)
     
        a = rows.find_element_by_css_selector('a')
        try:
            jobs.append(a.get_property('title'))
        except:
            jobs.append('No Job Title')
        try:
            companies.append(rows.find_element_by_class_name('company').text)
        except:
            companies.append('No Company')
        try:
            locations.append(rows.find_element_by_class_name('location').text)
        except:
            locations.append('No Location')
        try:
            salaries.append(rows.find_element_by_class_name('no-wrap').text)
        except:
            salaries.append('Nothing Found')
        try:
            links.append(a.get_property('href'))
        except:
            links.append('Nothing Found')
            
            
            
            
        delete_cookies()
        

       
#%% Main
soup = make_soup(main_page)

while main_page != 'Last Page':
    page_timer = default_timer()
    pages_links.append(main_page)
    delete_cookies()
    try:
        driver.find_element_by_css_selector('#popover-close-link').click()
        sleep(2)
        main_page = driver.current_url
    except:
        scrape_results(soup)
        try:
            driver.find_element_by_partial_link_text('Next').click()
            sleep(1)
            main_page = driver.current_url
        except:
            main_page = 'Last Page'
    

               
    page_timer_end = (default_timer() - page_timer)/60
    timers.append(page_timer_end)
    
    print('Finished page: '+ str(result_page) + ' with jobs of: ' + str(len(jobs)) + ' in ' + str(page_timer_end))
    result_page = result_page+1
    
end = (default_timer() - start)/60
#%%
#print timers
print('-----------------Totals---------------------')  
print('Minutes from the program starts to end: ' + str(end)) 
print('Scraped Total jobs of ' + str(len(jobs)))      

#%% creating dataframe
df = pd.DataFrame()
    
#%%
df['Jobs'] = jobs
df['Companies'] = companies
df['Locations'] = locations
df['Salaries'] = salaries
df['Summaries'] = summaries
df['Link_Page'] = links


#%% change filename and export to csv files
df.to_csv('Indeed_Business Analyst1.csv',encoding="utf-8")
