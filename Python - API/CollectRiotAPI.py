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

user_api_key = '737ac1b1-254c-49a7-b540-6457248982c2' # insert api key here
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
    rank_tier = [0, 0, 0, 0, 0, 0] # challenger(master) diamond platinum gold silver(unranked) bronze
    matchDuration = match['matchDuration']
    inhib_kills = match['teams'][0]['inhibitorKills'] + match['teams'][1]['inhibitorKills']
    write_line = str(match['matchId']) + '^' + str(matchDuration)
    if inhib_kills > 0: # ff'ed?
        write_line += '^0' # false (probably)
    else:
        write_line +=  '^1' # true -- gave up early
    write_line_b = ''
    for p in match['participants']:
        if p['highestAchievedSeasonTier'] == 'CHALLENGER' or p['highestAchievedSeasonTier'] == 'MASTER':
            rank_tier[0] += 1
        elif p['highestAchievedSeasonTier'] == 'DIAMOND':
            rank_tier[1] += 1
        elif p['highestAchievedSeasonTier'] == 'PLATINUM':
            rank_tier[2] += 1
        elif p['highestAchievedSeasonTier'] == 'GOLD':
            rank_tier[3] += 1
        elif p['highestAchievedSeasonTier'] == 'SILVER' or p['highestAchievedSeasonTier'] == 'UNRANKED':
            rank_tier[4] += 1
        elif p['highestAchievedSeasonTier'] == 'BRONZE':
            rank_tier[5] += 1
        if p['stats']['winner']:
            write_line += '^' + p['timeline']['lane'] + '^' + p['timeline']['role'] + \
                          '^' + str(p['stats']['minionsKilled']+p['stats']['neutralMinionsKilled']) + \
                          '^' + str(p['stats']['kills']) + '^' + str(p['stats']['deaths']) + \
                          '^' + str(p['stats']['assists'])
            if matchDuration > 600:
                write_line += '^' + str(p['timeline']['creepsPerMinDeltas']['zeroToTen']) + \
                                '^' + str(p['timeline']['goldPerMinDeltas']['zeroToTen'])                              
            else:
                write_line += '^' + str(0) + '^' + str(0)
            if matchDuration > 1200:
                write_line += '^' + str(p['timeline']['creepsPerMinDeltas']['tenToTwenty']) + \
                                '^' + str(p['timeline']['goldPerMinDeltas']['tenToTwenty'])
            else:
                write_line += '^' + str(0) + '^' + str(0)
            if matchDuration > 1800:
                write_line += '^' + str(p['timeline']['creepsPerMinDeltas']['twentyToThirty']) + \
                                '^' + str(p['timeline']['goldPerMinDeltas']['twentyToThirty'])
            else:
                write_line += '^' + str(0) + '^' + str(0)
        else:
            write_line_b += '^' + p['timeline']['lane'] + '^' + p['timeline']['role'] + \
                            '^' + str(p['stats']['minionsKilled']+p['stats']['neutralMinionsKilled']) + \
                            '^' + str(p['stats']['kills']) + '^' + str(p['stats']['deaths']) + \
                            '^' + str(p['stats']['assists'])
            if matchDuration > 600:
                write_line_b += '^' + str(p['timeline']['creepsPerMinDeltas']['zeroToTen']) + \
                                '^' + str(p['timeline']['goldPerMinDeltas']['zeroToTen'])                              
            else:
                write_line_b += '^' + str(0) + '^' + str(0)
            if matchDuration > 1200:
                write_line_b += '^' + str(p['timeline']['creepsPerMinDeltas']['tenToTwenty']) + \
                                '^' + str(p['timeline']['goldPerMinDeltas']['tenToTwenty'])
            else:
                write_line_b += '^' + str(0) + '^' + str(0)
            if matchDuration > 1800:
                write_line_b += '^' + str(p['timeline']['creepsPerMinDeltas']['twentyToThirty']) + \
                                '^' + str(p['timeline']['goldPerMinDeltas']['twentyToThirty'])
            else:
                write_line_b += '^' + str(0) + '^' + str(0)
                
    write_line += write_line_b
    if rank_tier.index(max(rank_tier)) == 0:
        write_line += '^' + 'c'
    elif rank_tier.index(max(rank_tier)) == 1:
        write_line += '^' + 'd'
    elif rank_tier.index(max(rank_tier)) == 2:
        write_line += '^' + 'p'
    elif rank_tier.index(max(rank_tier)) == 3:
        write_line += '^' + 'g'
    elif rank_tier.index(max(rank_tier)) == 4:
        write_line += '^' + 's'
    elif rank_tier.index(max(rank_tier)) == 5:
        write_line += '^' + 'b'
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
            sid = getFirstId('anniebot') # seed player
            mid_set = getRecentGames(sid)['matches']
            addMatchIdToData(mid_set)
        while mid_index<3000: # number of games
            if mid_index%5==0 and mid_index!=0:
                mid_set = getRecentGames(global_sid_list[mid_index/5])['matches']
                addMatchIdToData(mid_set)
            getMatchData(mid_index, write_file)
            mid_index += 1

    except KeyError:
        print "Key Error"
        time.sleep(15)
        mid_index +=1
        loop(write_file, mid_index)
        

def main(initial_mid_index=0):
    try:
        write_file = open('RiotChallengerData.txt', 'a') # output file
        loop(write_file)
    finally:
        write_file.close()
        print "done"
    
    
if __name__ == "__main__":
    main()
