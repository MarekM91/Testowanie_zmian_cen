from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import pandas as pd

# Automatically install the matching ChromeDriver version
chromedriver_autoinstaller.install()

service = Service()  # No need to specify the path if using autoinstaller
driver = webdriver.Chrome(service=service)

def check_price_change(product_url, expected_price):
    try:
        #Otwieramy stronę z produktem
        driver.get(product_url)

        #Czekamy aż strona się wczyta
        price_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@data-selen="product-price"]')))

        #Wyciągamy obecną cene
        current_price = price_element.text.strip()
        print(f"Aktualna cena: {current_price}")

        #Czyścimy i porównywamy ceny
        current_price_value = float(current_price.replace('PLN', '').replace(',', '.').strip())

        #Sprawdzamy czy cena się zmieniła
        if current_price_value == expected_price:
            print("Cena jest taka sama")
        else:
            print(f"Inna cena {current_price_value}")
    except Exception as e:
        print(f"Error occured: {e}")

#Wczytujemy dane z pliku excel
excel_file = "C:\\Users\\mimarek\\OneDrive - LPP S.A\\Desktop\\Testy Selenium\\produkty.xlsx"
df = pd.read_excel(excel_file)

try:
    #Iterujemy przez wiersze z użyciem data frame
    for index, row in df.iterrows():
        sku = row['sku'].strip().lower()
        expected_price = row['cena']
        product_url = f"https://www.sinsay.com/pl/pl/{sku}"  # Zakładam, że URL jest tworzony na podstawie SKU
        print(f"Sprawdzanie ceny dla SKU: {sku}")
        check_price_change(product_url, expected_price)

finally:
        #Zamykamy witryne
        driver.quit()