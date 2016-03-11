<<<<<<< HEAD
import requests
import time
import RiotConsts as Consts
import collections

class RiotAPI(object):
    callCounter = 0

    def __init__(self, api_key, region=Consts.REGIONS['north_america']):
        self.api_key = api_key
        self.region = region
        
            
            

    def _request(self, api_url, params={}):
        RiotAPI.callCounter += 1
        if RiotAPI.callCounter%7==0:
            print "running... " + str(RiotAPI.callCounter)
            
            time.sleep(11)
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value
        response = requests.get(
            Consts.URL['base'].format(
                proxy=self.region,
                region=self.region,
                url=api_url),
            params=args)

        print response.status_code
        ## point system
        point = collections.namedtuple('Point', ['x', 'y'])
        p = point(response.json(), response.status_code)
        
        
        return p

    def get_summoner_by_name(self, name):
        api_url = Consts.URL['summoner_by_name'].format(
            version=Consts.API_VERSIONS['summoner'],
            names=name
            )
        return self._request(api_url)

    def get_matchlist_by_summid(self, summid, beginIndex=0, endIndex=15):
        api_url = Consts.URL['matchlist_by_summid'].format(
            version=Consts.API_VERSIONS['matchlist'],
            summid=summid
            )
        params = { 'beginIndex': beginIndex,
                   'endIndex': endIndex }
        return self._request(api_url, params)

    def get_match(self, matchid):
        api_url = Consts.URL['match'].format(
            version=Consts.API_VERSIONS['match'],
            matchid=matchid
            )
        return self._request(api_url)


=======
import requests
import time
import RiotConsts as Consts
import collections

class RiotAPI(object):
    callCounter = 0

    def __init__(self, api_key, region=Consts.REGIONS['north_america']):
        self.api_key = api_key
        self.region = region
        
            
            

    def _request(self, api_url, params={}):
        RiotAPI.callCounter += 1
        if RiotAPI.callCounter%7==0:
            print "running... " + str(RiotAPI.callCounter)
            
            time.sleep(11)
        args = {'api_key': self.api_key}
        for key, value in params.items():
            if key not in args:
                args[key] = value
        response = requests.get(
            Consts.URL['base'].format(
                proxy=self.region,
                region=self.region,
                url=api_url),
            params=args)

        print response.status_code
        ## point system
        point = collections.namedtuple('Point', ['x', 'y'])
        p = point(response.json(), response.status_code)
        
        
        return p

    def get_summoner_by_name(self, name):
        api_url = Consts.URL['summoner_by_name'].format(
            version=Consts.API_VERSIONS['summoner'],
            names=name
            )
        return self._request(api_url)

    def get_matchlist_by_summid(self, summid, beginIndex=0, endIndex=15):
        api_url = Consts.URL['matchlist_by_summid'].format(
            version=Consts.API_VERSIONS['matchlist'],
            summid=summid
            )
        params = { 'beginIndex': beginIndex,
                   'endIndex': endIndex }
        return self._request(api_url, params)

    def get_match(self, matchid):
        api_url = Consts.URL['match'].format(
            version=Consts.API_VERSIONS['match'],
            matchid=matchid
            )
        return self._request(api_url)


>>>>>>> c8f0b38a1d531b4d0d295c6e57fd492d306f0b54
