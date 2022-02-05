import os
from dbcommands import DBCommands
import requests
import json


class LeagueApi:
    _lol_db = DBCommands()
    _session = None
    _headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/96.0.4664.93 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Charset": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://developer.riotgames.com",
        'X-Riot-Token': os.environ.get("X_RIOT_TOKEN")
    }

    def __init__(self):
        self._session = requests.Session()
        self._session.headers.update(self._headers)
        self._lol_db = DBCommands()

    def get_champions(self):

        results = self._session.get("https://ddragon.leagueoflegends.com/api/versions.json")
        version = json.loads(json.dumps(results.json()))[0]
        results = self._session.get("https://ddragon.leagueoflegends.com/cdn/{}/data/en_US/champion.json".format(version))

        champions_data = json.loads(json.dumps(results.json()))["data"]
        champions = {}

        for name, data in champions_data.items():
            print(data)
            champions[data["key"]] = data["id"]

        return champions

    def summoner_by_name(self, region, name):

        size, db_results = self._lol_db.get_account_by_name(name)

        if size == 0:
            results = self._session.get(
                "https://{}.api.riotgames.com/lol/summoner/v4/summoners/by-name/{}".format(region, name))

            if results.status_code == 200:
                account = json.loads(json.dumps(results.json()))
                self._lol_db.insert_account(account)
                return self.summoner_by_name(region, name)
        else:
            return db_results[0][0], db_results[0][1], db_results[0][2], db_results[0][3]

    def insert_match(self, id):
        self._lol_db.insert_match(id)

    def match_by_id(self, region, id):

        results = self._session.get(
            "https://{}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/{}".format(region, id))
        match_info = json.loads(json.dumps(results.json()))

        if results.status_code == 200 and self._lol_db.match_recorded("{}".format(match_info["gameId"])):
            return 404, ""

        return results.status_code, match_info