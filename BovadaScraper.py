'''
Created on Jan 9, 2021

@author: jacob
'''
import csv
import requests
import json
##Am I bad at JSON or is it dumb to have to put [0] after every elements name? Its gotta be me right?
r = requests.get('https://www.bovada.lv/services/sports/event/v2/events/A/description/esports/league-of-legends')
deserialized = json.loads(r.text)
allMoneyLines = [['Home','HomeML','Away','AwayML']]
for event in deserialized[0]['events']:
    for market in event['displayGroups'][0]['markets']:
        moneyLine = []
        if market['description'] == 'Moneyline':
            for outcome in market['outcomes']:
                moneyLine.append(outcome['description'])
                moneyLine.append(outcome['price']['american'])
        allMoneyLines.append(moneyLine)                 
        break
    with open('BovadaLines.csv','wb') as result_file:
            wr = csv.writer(result_file, dialect='excel')
            wr.writerows(allMoneyLines)