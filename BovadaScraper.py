'''
Created on Jan 9, 2021

@author: jacob
'''
import csv
import requests
import json
#Am I bad at JSON or is it dumb to have to put [0] after every elements name? Its gotta be me right?
r = requests.get('https://www.bovada.lv/services/sports/event/v2/events/A/description/esports/league-of-legends')
deserialized = json.loads(r.text)
allMoneyLines = [['Team','Opp','ML']]
for event in deserialized[0]['events']:
    teamA = event['competitors'][0]['name']
    teamB = event['competitors'][1]['name']
    for market in event['displayGroups'][0]['markets']:
        if market['description'] == 'Moneyline':
            for outcome in market['outcomes']:
                """"
                I wish I didnt have to do this, but Bovada goes full >Bovada and doesn't actually order  teams in a red side/blue side way. 
                Instead they just randomly assign one as the home team, so for easier processing later I'm storing things in the following format:
                Team,Opponent,Team MoneyLine
                
                And then I do that twice for each match, so it will be:
                Team A, Team B, Team A Moneyline
                Team B, Team A, Team B Moneyline
                """
                description = outcome['description']
                opp = teamB if (description == teamA) else teamA
                allMoneyLines.append([description,opp,outcome['price']['american']])
        break
    with open('BovadaLines.csv','wb') as result_file:
            wr = csv.writer(result_file, dialect='excel')
            wr.writerows(allMoneyLines)