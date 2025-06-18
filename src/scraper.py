from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time

# Configurações do Selenium para rodar sem abrir janela
chrome_options = Options()
# chrome_options.add_argument('--headless')  # Comente esta linha
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--window-size=1920,1080')

url = "https://www.oddsagora.com.br/football/brazil/brasileirao-betano/"
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Inicia o navegador com webdriver-manager
with webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options) as driver:
    driver.get(url)
    time.sleep(5)
    # Aguarda até que os jogos estejam presentes na página
    try:
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".eventRow"))
        )
    except Exception as e:
        print(f"Erro ao carregar os jogos: {e}")
        driver.quit()
        exit(1)
    # Pega o HTML renderizado
    html = driver.page_source

    with open("pagina.html", "w", encoding="utf-8") as f:
        f.write(driver.page_source)

soup = BeautifulSoup(html, "html.parser")

# Seleciona todos os jogos
jogos = soup.select('[data-testid="game-row"]')

for jogo in jogos:
    # Pega os nomes dos times
    times = jogo.select("p.participant-name.truncate")
    
    # Pega as odds
    odds = jogo.select('p[data-testid="odd-container-default"]')

    if len(times) >= 2 and len(odds) >= 3:
        time_casa = times[0].text.strip()
        time_fora = times[1].text.strip()

        odd_casa = odds[0].text.strip()
        odd_empate = odds[1].text.strip()
        odd_fora = odds[2].text.strip()

        print(f"🎯 Jogo: {time_casa} x {time_fora}")
        print(f"   🏠 Casa      ➤ {odd_casa}")
        print(f"   🤝 Empate    ➤ {odd_empate}")
        print(f"   🛫 Visitante ➤ {odd_fora}")

    print("-" * 50)
    time.sleep(1)