'''
Created on Jul 21, 2020

@author: jacob
'''
import csv
import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
#Major Regions
url = 'https://lolesports.com/schedule?leagues=lcs,lec,lck,lpl'
#Minor Regions
# url= 'https://watch.lolesports.com/schedule?leagues=lcs-academy,turkiye-sampiyonluk-ligi,cblol-brazil,lla,oce-opl,ljl-japan'
offset =1
#0 = today, 1 = tomorrow, etc.
date = datetime.datetime.today() + datetime.timedelta(days = offset)
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("--start-maximized")
browser = webdriver.Chrome(executable_path="C:\ChromeDriver\chromedriver.exe")
browser.get('chrome://settings/')
#Team names get abbreviated if your browser window is too small, so just zoom so far out that this issue cant happen
browser.execute_script('chrome.settingsPrivate.setDefaultZoom(.01);')
browser.get(url)
table = browser.find_element(By.CLASS_NAME, 'EventDate')
elements = browser.find_elements_by_xpath('//*/text()[.="{}"]/following::div'.format(date.strftime("%B %#d")))
matches = [['Blue','Red','League']]
for e in elements:
    if(e.get_attribute('class') == 'EventDate'):
        with open('Matchups.csv','wb') as result_file:
            wr = csv.writer(result_file, dialect='excel')
            wr.writerows(matches)
            browser.quit()
        exit()
    if(e.get_attribute('class') == 'EventMatch'):
        teams = e.find_elements_by_xpath('.//div[@class="team-info"]')
        league = e.find_elements_by_xpath('.//div[@class="league"]')
        match = [teams[0].text, teams[1].text, league[0].text]
        matches.append(match)
