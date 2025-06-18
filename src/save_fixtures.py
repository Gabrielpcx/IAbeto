# src/save_fixtures.py

import requests
import pandas as pd
import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()
API_KEY = os.getenv("API_FOOTBALL_KEY")

BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {"x-apisports-key": API_KEY}

def get_next_fixtures(league_id=10, season=2024, qtd=3):
    url = f"{BASE_URL}/fixtures"
    params = {
        "league": league_id,
        "season": season,
        "next": qtd
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        print("Erro ao buscar jogos:", response.status_code)
        return []
    return response.json()["response"]

def get_odds_for_fixture(fixture_id):
    url = f"{BASE_URL}/odds"
    params = {"fixture": fixture_id}
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code != 200:
        return None

    try:
        bookmakers = response.json()["response"][0]["bookmakers"]
        for book in bookmakers:
            if "match winner" in [b["name"].lower() for b in book["bets"]]:
                for bet in book["bets"]:
                    if bet["name"].lower() == "match winner":
                        odds = bet["values"]
                        return {
                            "odds_home": float(odds[0]["odd"]),
                            "odds_draw": float(odds[1]["odd"]),
                            "odds_away": float(odds[2]["odd"])
                        }
    except (IndexError, KeyError):
        return None

    return None

def save_fixtures_to_csv():
    fixtures = get_next_fixtures()

    rows = []
    for match in fixtures:
        fixture_id = match["fixture"]["id"]
        date = match["fixture"]["date"]
        league_name = match["league"]["name"]
        season = match["league"]["season"]
        home_team = match["teams"]["home"]["name"]
        away_team = match["teams"]["away"]["name"]

        odds_data = get_odds_for_fixture(fixture_id)
        if odds_data:
            row = {
                "fixture_id": fixture_id,
                "date": date,
                "league": league_name,
                "season": season,
                "home_team": home_team,
                "away_team": away_team,
                **odds_data
            }
            rows.append(row)

    if rows:
        df = pd.DataFrame(rows)
        os.makedirs("data", exist_ok=True)
        df.to_csv("data/matches.csv", index=False)
        print(f"Salvo com sucesso {len(rows)} jogos em data/matches.csv")
    else:
        print("Nenhum jogo com odds disponível no momento.")

if __name__ == "__main__":
    save_fixtures_to_csv()
