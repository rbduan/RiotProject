from RiotAPI import RiotAPI
from collections import OrderedDict
import time
##order:
##    1. get first acct ID (in: ingamename, out: nameid)
##    2. look at his recent games (in: nameid, out: list of gameid (10))
##    3. add games to data (in: gameid, out: void)
##    4. look at teammates, add to list and remove duplicates (in: list of gameid, out: void)
##        a. put a size limit to gameid list
##    5. get one from gameid list (in: list of gameid, out: void)
##    6. repeat 2-5

user_api_key = '' # insert api key here
global_mid_list = []
global_sid_list = []
api = RiotAPI(user_api_key) 
mid_index = 0

def getFirstId(ingamename):
    resp = api.get_summoner_by_name(ingamename)[0]
    return resp[ingamename]['id']


def getRecentGames(summid):
    resp = api.get_matchlist_by_summid(summid)[0]
    return resp


def addMatchIdToData(mid_set):
    global global_mid_list
    for match in mid_set:
        if match['queue'] == 'TEAM_BUILDER_DRAFT_RANKED_5x5':
            global_mid_list.append(match['matchId'])
    global_mid_list = list(OrderedDict.fromkeys(global_mid_list))


def getMatchData(mid_index, write_file):
    match = api.get_match(global_mid_list[mid_index])[0]

    write_line = str(match['matchId']) + '^' + str(match['matchDuration'])
    write_line_b = ''
    for p in match['participants']:
        if p['stats']['winner']:
            write_line += '^' + str(p['stats']['minionsKilled']+p['stats']['neutralMinionsKilled']) + '^' + str(p['stats']['kills']) + '^' + str(p['stats']['deaths']) + '^' + str(p['stats']['assists'])
        else:
            write_line_b += '^' + str(p['stats']['minionsKilled']+p['stats']['neutralMinionsKilled']) + '^' + str(p['stats']['kills']) + '^' + str(p['stats']['deaths']) + '^' + str(p['stats']['assists'])
    write_line += write_line_b
        
    write_file.write(write_line+'\n')
    getSummId(match)
    

def getSummId(match):
    global global_sid_list
    for i in range(10):
        global_sid_list.append(match['participantIdentities'][i]['player']['summonerId'])
    global_sid_list = list(OrderedDict.fromkeys(global_sid_list))


def loop(write_file, initial_mid_index=0):
    global mid_index
    try:
        mid_index = initial_mid_index
        if mid_index==0:
            sid = getFirstId('swag4lyfe') # seed player
            mid_set = getRecentGames(sid)['matches']
            addMatchIdToData(mid_set)
        while mid_index<1500:
            if mid_index%5==0 and mid_index!=0:
                mid_set = getRecentGames(global_sid_list[mid_index/5])['matches']
                addMatchIdToData(mid_set)
            getMatchData(mid_index, write_file)
            mid_index += 1

    except KeyError:
        print "Key Error"
        time.sleep(15)
        loop(write_file, mid_index)
        

def main(initial_mid_index=0):
    try:
        write_file = open('RiotData.txt', 'a')
        loop(write_file)
    finally:
        write_file.close()
        print "done"
    
    
if __name__ == "__main__":
    main()
