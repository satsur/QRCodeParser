import os
from enum import StrEnum
from dotenv import load_dotenv
import requests

class MatchTypes(StrEnum):
    QUALIFICATION = "qm"
    PLAYOFF = "sf"
    FINALS = "f"

load_dotenv()
API_KEY = os.getenv("API_KEY")

headers = {
    "X-TBA-Auth-Key": API_KEY
}

def get_event_matches(event_key:str):
    response = requests.get(f"https://www.thebluealliance.com/api/v3/event/{event_key}/matches/simple", headers=headers)
    if response.status_code != 200:
        return None
    else: 
        return response.json()

def get_teams_in_match(event_data, match_num:int, match_type: MatchTypes):
    if event_data == None:
        return None
    for match in event_data:
        if str(match["match_number"]) == str(match_num) and match["comp_level"] == match_type:
            return {
                "red": [team.replace("frc", "") for team in match["alliances"]["red"]["team_keys"]],
                "blue": [team.replace("frc", "") for team in match["alliances"]["blue"]["team_keys"]]
            }
    return None