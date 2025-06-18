import requests
import pandas as pd
import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}

def get_fixtures(league_id=71, season=2024):  # Brasileirão Série A = 71
    url = f"{BASE_URL}/fixtures"
    params = {
        "league": league_id,
        "season": season,
        
    }
    response = requests.get(url, headers=HEADERS, params=params)
    print("Status code:", response.status_code)
    print("Response text:", response.text) # Debugging: imprime o status code e o texto da resposta
    if response.status_code != 200:
        print("Erro:", response.status_code, response.text)
        return pd.DataFrame()

    data = response.json()["response"]
    df = pd.json_normalize(data)
    return df

def get_odds(fixture_id):
    url = f"{BASE_URL}/odds"
    params = {
        "fixture": fixture_id
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        print("Erro ao buscar odds:", response.status_code)
        return None

    return response.json()["response"]

if __name__ == "__main__":
    fixtures = get_fixtures()
    print("Próximos jogos:")
    print(fixtures[["fixture.id", "teams.home.name", "teams.away.name", "fixture.date"]])
