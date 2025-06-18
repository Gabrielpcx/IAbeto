# src/live_matches.py

import requests
import os
from dotenv import load_dotenv

# Carrega a API key do .env
load_dotenv()
API_KEY = os.getenv("API_FOOTBALL_KEY")

# Define cabeçalho e endpoint
BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": API_KEY}

def get_live_matches():
    url = f"{BASE_URL}/fixtures"
    params = {
        "live": "all"
    }
    response = requests.get(url, headers=HEADERS, params=params)

    if response.status_code != 200:
        print("Erro:", response.status_code, response.text)
        return []

    data = response.json()["response"]
    return data

if __name__ == "__main__":
    live_games = get_live_matches()

    if not live_games:
        print("Nenhum jogo ao vivo agora.")
    else:
        for game in live_games:
            home = game["teams"]["home"]["name"]
            away = game["teams"]["away"]["name"]
            score_home = game["goals"]["home"]
            score_away = game["goals"]["away"]
            status = game["fixture"]["status"]["long"]
            print(f"{home} {score_home} x {score_away} {away} - {status}")
