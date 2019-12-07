'''
Created on Nov 28, 2019

@author: Elite-Intel
'''
import csv
import datetime
from time import sleep
from selenium import webdriver
from webdriver.common.by import By


URLS = ['https://www.oddsportal.com/esports/usa/league-of-legends-championship-series/results/#/',
        'https://www.oddsportal.com/esports/usa/league-of-legends-championship-series/results/#/page/2/']
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("--start-maximized")
browser = webdriver.Chrome(executable_path="D:\ChromeDriver\chromedriver.exe")
browser.maximize_window()
headerArr = ['blueTeam', 'redTeam', 'blueSeriesWins', 'redSeriesWins', 'blueML', 'redML', 'Date']   
rows = []
date = datetime.datetime.today()


#Parse a date written in plaintext to a datetime in the format we want     
def parseDateRow(row):
    rowArr = row.text.split()
    d = datetime.datetime.strptime("{0} {1} {2}".format(rowArr[0],rowArr[1],rowArr[2]),'%d %b %Y')
    return d

#This is messy but theres no way around it
#Data comes in in the format "HH:MM TEAMA - TEAMB ASCORE:BSCORE \nMLA MLB"
#We need to grab each individual piece, so we do a bunch of splitting
def parseMatchDataRow(row,date):
    rowArr  = row.text.split("\n")
    teams = rowArr[0].split("-")
    teamAWTime = teams[0].split()
    teamBWResult = teams[1].split()
    teamAWTime[1:len(teamAWTime)] = [' '.join(teamAWTime[1:len(teamAWTime)])]
    teamBWResult[0:len(teamBWResult)-1] =  [' '.join(teamBWResult[0:len(teamBWResult)-1])]
    blueTeam = teamAWTime[1]
    redTeam = teamBWResult[0]
    result = teamBWResult[1].split(":")
    date = date if (teamAWTime[0] != '00:00') else (date + datetime.timedelta(days=-1))
    toReturn = [blueTeam,redTeam,result[0],result[1],rowArr[1],rowArr[2],date.strftime('%Y-%m-%d')]
    return toReturn

def parseURL(url, browser):
    browser.get(url)
    sleep(4)
    table = browser.find_element(By.CLASS_NAME, 'table-main')
    for row in table.find_elements_by_xpath(".//tr"):
        rowType = row.get_attribute('class').strip()
        if("nob-border" in rowType):
            date = parseDateRow(row)
        elif("deactivate" in rowType):
            rows.append(parseMatchDataRow(row,date))
            
for URL in URLS:
    parseURL(URL,browser)

browser.quit()

with open('OddsData.csv','wb') as result_file:
        wr = csv.writer(result_file, dialect='excel')
        wr.writerow(headerArr)
        wr.writerows(rows)
