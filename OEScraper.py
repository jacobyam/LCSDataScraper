'''
Created on Nov 26, 2019

@author: Elite-Intel
'''
import csv
from selenium import webdriver
from webdriver.common.by import By


numTeams = 10
options = webdriver.ChromeOptions()
options.add_argument('headless')
options.add_argument("--start-maximized")
browser = webdriver.Chrome(executable_path="D:\ChromeDriver\chromedriver.exe")
browser.maximize_window()
browser.get('http://oracleselixir.com/statistics/eu/lec-2019-summer-regular-season-team-statistics/')

#This is a super hacky workaround, but the browser cant read text that isnt on screen and the table needs to be fully scrolled over.
#Instead of scrolling over column by column we just change the css to show the entire table even if it overflows the page
browser.execute_script("document.getElementsByClassName('dataTables_scrollHead')[0].style = \"overflow: none; position: relative; border: 0px; width: 100%;\"")
browser.execute_script("document.getElementsByClassName('dataTables_scrollBody')[0].style = \"position: relative; overflow: none; width: 100%;\"")
header = browser.find_element(By.CLASS_NAME, 'row-1')
headerArr = header.text.split()
rows = []
for i in range(1,numTeams):
    row = browser.find_element(By.CLASS_NAME, 'row-{}'.format(i+1)).text.split()
    #Sometimes team names have spaces in them, so we join the words into one column
    while(len(row) > len(headerArr)):
        row[0:2] = [' '.join(row[0:2])]
    rows.append(row)
    
browser.quit()

with open('EUTeamData.csv','wb') as result_file:
        wr = csv.writer(result_file, dialect='excel')
        wr.writerow(headerArr)
        wr.writerows(rows)

