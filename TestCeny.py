from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller

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
    finally:
        #Zamykamy witryne
        driver.quit()

product_url = "https://www.sinsay.com/pl/pl/sukienka-z-golfem-430be-99x"
expected_price = 29.99

check_price_change(product_url, expected_price)