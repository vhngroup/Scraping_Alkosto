import undetected_chromedriver as webdriver1
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
import pandas as pd
import math
import datetime
import time
import re

class Scraping_Alkosto:
    def __init__(self, url, service, csvProductos):
        self.data = []
        self.load_Pref(service)      

    def load_Pref(self, service):
        try:
            options = webdriver1.ChromeOptions()
            options.add_argument('--disable-dev-shm-usage')
            ##options.add_argument('--headless')
            options.add_argument('--disable-browser-side-navigation')
            options.add_argument('--disable-background-networking')
            options.add_argument('--disable-notifications')
            options.add_argument('--autoplay-policy=user-gesture-required')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-save-password-bubble')
            #options.add_argument('--start-maximized')
            chrome_prefs = {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False
            }
            options.add_experimental_option("prefs", chrome_prefs)
            driver = webdriver1.Chrome(service=service, options=options)
        except:
            options = webdriver.ChromeOptions()
            options.add_argument('--disable-dev-shm-usage')
            ##options.add_argument('--headless')
            options.add_argument('--disable-browser-side-navigation')
            options.add_argument('--disable-background-networking')
            options.add_argument('--disable-notifications')
            options.add_argument('--autoplay-policy=user-gesture-required')
            options.add_argument('--disable-gpu')
            options.add_argument('--disable-extensions')
            options.add_argument('--disable-save-password-bubble')
            options.add_experimental_option("detach", True)
            #options.add_argument('--start-maximized')
            chrome_prefs = {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False
            }
            options.add_experimental_option("prefs", chrome_prefs)
            driver = webdriver.Chrome(service=service, options=options)
        self.load_Browser(driver, url)

    def load_Browser(self, driver, url):
        guardo = 0
        for s in csvProductos:
            driver.get(url+s)
            time.sleep(10)
            all_data_no_clean = driver.find_elements(By.CSS_SELECTOR, '#js-hits li')
            for element in all_data_no_clean:
                try:
                    title_element = element.find_element(By.TAG_NAME,'h3')
                    price_element = element.find_element(By.CLASS_NAME,'price')
                    image_element = element.find_element(By.TAG_NAME,'img').get_attribute('src')
                    brand_element = element.find_element(By.CLASS_NAME,'product__item__information__brand')
                    characteristics_element = element.find_element(By.CLASS_NAME,'product__item__information')
                    url_product_element = element.find_element(By.LINK_TEXT, f'Ver más detalles').get_attribute('href')
                    self.data.append(
                        {
                            'Titulo': title_element.text,
                            'Precio': price_element.text,
                            'Imagen': image_element,
                            'Marca': brand_element.text,
                            'Caracteristicas' : re.sub(r"[^a-zA-Z0-9]", "", characteristics_element.text),
                            'url Producto': url_product_element
                            
                        }
                    )
                except NoSuchElementException:
                    pass
            print("Se han analizado",len(self.data))
            df = pd.DataFrame(self.data)
            if guardo == 0:
                df.to_csv("Alkosto.csv", encoding='UTF-8', sep ="!")
                guardo = 1
            else:
                df.to_csv("Alkosto.csv", index=True, mode='a', header=False, encoding='UTF-8', sep ="!")


if __name__ == "__main__":
    url = f'https://www.alkosto.com/search?text='
    service = Service()
    csvProductos = pd.read_csv('productos.csv',sep=',')['Equipo'].to_numpy()
    scraping_Site = Scraping_Alkosto(url, service, csvProductos)
    


