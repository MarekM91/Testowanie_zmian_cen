from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time  # Importujemy moduł time

# Automatyczna instalacja odpowiedniej wersji ChromeDrivera
chromedriver_autoinstaller.install()

# Funkcja do sprawdzania ceny
def check_price_change(sku, expected_price):
    product_url = f"https://www.sinsay.com/pl/pl/{sku}"
    
    service = Service()
    driver = webdriver.Chrome(service=service)

    try:
        driver.get(product_url)
        price_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//div[@data-selen="product-price"]'))
        )
        current_price = price_element.text.strip()
        current_price_value = float(current_price.replace('PLN', '').replace(',', '.').strip())

        if current_price_value != expected_price:
            return {
                'SKU': sku,
                'Oczekiwana cena': expected_price,
                'Aktualna cena': current_price_value,
                'Status': f"Inna cena: {current_price_value}"
            }
    except Exception as e:
        return {'SKU': sku, 'Status': f"Błąd: {e}"}
    finally:
        driver.quit()

# Wczytujemy dane z pliku Excel
excel_file = "C:\\Users\\mimarek\\OneDrive - LPP S.A\\Desktop\\Testy Selenium\\produkty.xlsx"
df = pd.read_excel(excel_file)

# Zaczynamy timer
start_time = time.time()  # Mierzymy czas rozpoczęcia operacji

# Tworzymy listę do przechowywania wyników
results = []

# Uruchamiamy równoległe sprawdzanie cen
with ThreadPoolExecutor(max_workers=4) as executor:  # Liczba wątków równoległych
    futures = [
        executor.submit(check_price_change, row['sku'].strip().lower(), row['cena'])
        for _, row in df.iterrows()
    ]
    for future in futures:
        result = future.result()
        if result:
            results.append(result)

# Zapisujemy wyniki tylko, jeśli są rozbieżności
if results:
    results_df = pd.DataFrame(results)
    output_file = "C:\\Users\\mimarek\\OneDrive - LPP S.A\\Desktop\\Testy Selenium\\wyniki.xlsx"
    results_df.to_excel(output_file, index=False)
    print(f"Wyniki zapisano w: {output_file}")
else:
    print("Wszystkie ceny były zgodne – brak wyników do zapisania.")

# Zatrzymujemy timer i obliczamy czas trwania operacji
end_time = time.time()  # Mierzymy czas zakończenia operacji
duration = end_time - start_time  # Obliczamy czas trwania
print(f"Czas trwania operacji: {duration:.2f} sekund")
