import os
from enum import StrEnum
from dotenv import load_dotenv
import requests
import json

DATA_FILE = "api\match_data.json"

class MatchTypes(StrEnum):
    QUALIFICATION = "qm"
    PLAYOFF = "sf"
    FINALS = "f"

load_dotenv()
API_KEY = os.getenv("API_KEY")

headers = {
    "X-TBA-Auth-Key": API_KEY
}

def get_stored_event_key():
    with open(DATA_FILE, 'r') as file:
        return json.load(file)["event_key"]

def schedule_exists(key:str):
    return get_stored_event_key() == key

def store_matches(match_data):
    stored_match_data = {}
    stored_match_data.update({"event_key": match_data[0]["event_key"]})
    for match in match_data:
        stored_match_data.update(
            {match["key"]: {
                "match_number": match["match_number"],
                "comp_level": match["comp_level"],
                "alliances": match["alliances"],
            }},
        )
    with open(DATA_FILE, 'w') as file:
        file.write(json.dumps(stored_match_data, indent=2))


def load_match_data_from_api(event_key:str):
    response = requests.get(f"https://www.thebluealliance.com/api/v3/event/{event_key}/matches/simple", headers=headers)
    if response.status_code != 200:
        return None
    else: 
        print("storing...")
        data = response.json()
        return data

def get_stored_match_data(event_key:str):
    if not schedule_exists(event_key):
        return None
    with open(DATA_FILE, 'r') as file:
        return json.load(file)

# set_number is the "match number" in eliminations - match_number refers to the match # in each bo3 round in elims
def compose_match_lookup_key(event_key:str, type: MatchTypes=MatchTypes.QUALIFICATION, set_number=1, match_number=1):
    if type == MatchTypes.QUALIFICATION:
        return f"{event_key}_qm{match_number}"
    elif type == MatchTypes.PLAYOFF:
        return f"{event_key}_sf{set_number}m{match_number}"
    elif type == MatchTypes.FINALS:
        return f"{event_key}_f1m{match_number}"

def get_teams_in_match(match_data, match_num:int, match_type: MatchTypes):
    event_key = match_data["event_key"]
    try:
        match = match_data[compose_match_lookup_key(event_key=event_key, type=match_type, match_number=match_num)]
    except KeyError:
        return None
    return {
        "red": [team.replace("frc", "") for team in match["alliances"]["red"]["team_keys"]],
        "blue": [team.replace("frc", "") for team in match["alliances"]["blue"]["team_keys"]]
    }
