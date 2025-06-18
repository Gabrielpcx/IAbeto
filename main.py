# main.py

from src.data_collector import get_odds

if __name__ == "__main__":
    print("Coletando odds...")
    df = get_odds()
    print(df.head())
