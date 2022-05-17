import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

from fake_useragent import UserAgent
from fake_useragent import FakeUserAgentError
from math import ceil
from random import randint
from time import sleep
from base64 import b64decode
from io import BytesIO
from PIL import Image
import pytesseract

from realty import check_database, create_table
from export import exporting
from config import CITY_OR_REGION


URL_AVITO = f"https://www.avito.ru/{CITY_OR_REGION}/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?user=1"
EUR = 1


def cb_rf():
    url = "https://www.cbr.ru/"
    response = requests.get(url=url)
    soup = BeautifulSoup(response.text, "lxml")
    global EUR
    EUR = float(soup.findAll("div",
                             class_="col-md-2 col-xs-9 _right mono-num")[2].text[:-10].replace(",", "."))


def avito_parser():
    try:
        ua = UserAgent().chrome
    except FakeUserAgentError:
        ua = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:84.0) Gecko/20100101 Firefox/84.0"
    options = webdriver.ChromeOptions()
    options.add_argument(f"user-agent={ua}")
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(options=options)
    driver.implicitly_wait(15)
    driver.get(URL_AVITO)

    count = int((driver.find_element(by=By.CSS_SELECTOR,
                                     value='span[data-marker="page-title/count"]').text).replace(' ', ''))

    for i in range(ceil(count / 50)):
        offer = []
        elems = driver.find_elements(by=By.CSS_SELECTOR,
                                     value='div[data-marker="item"]')
        for elem in elems:
            try:
                avito_id = int(elem.get_attribute("id")[1:])
                url = elem.find_element(by=By.CSS_SELECTOR,
                                        value='a[itemprop="url"]').get_attribute("href")
                item_address = elem.find_element(by=By.CSS_SELECTOR,
                                                 value='div[data-marker="item-address"]').text.split('\n')
                address = item_address[0]
                district = item_address[1] if len(item_address) > 1 else "Рязанский р-н"
                advert = elem.text.split('\n')
                price = round(int(advert[1][:-10].replace(" ", "")) / EUR, 2)
                rooms = advert[0].split(", ")[0].split()[0].replace("-к.", "")
                area = float(advert[0].split(", ")[1][:-3].replace(",", "."))
                floor = int(advert[0].split(", ")[2].split('/')[0])
                total_floor = int(advert[0].split(", ")[2].split('/')[1][:-4])
                text = elem.find_element(by=By.CSS_SELECTOR,
                                         value='meta[itemprop="description"]').get_attribute("content")
                online_display = "Да" if "Онлайн-показ" in advert else "Нет"

                hover = ActionChains(driver).move_to_element(elem)
                hover.perform()

                button = elem.find_element(by=By.CSS_SELECTOR,
                                           value='button[type="button"]')
                button.click()

                rand_sleep = randint(25, 49)
                sleep(rand_sleep / 10)

                phone_pict = elem.find_element(by=By.CSS_SELECTOR,
                                               value="img[data-marker='phone-image']").get_attribute("src")
                data = b64decode(phone_pict.split('base64,')[-1].strip())
                image = Image.open(BytesIO(data))
                phone_number = pytesseract.image_to_string(image).split('\n')[0]

                result = (avito_id, rooms, area, price, address, district, floor,
                          total_floor, phone_number, text, online_display, url)
                offer.append(result)

            except Exception as ex:
                print(ex)

        check_database(offer)
        driver.find_element(by=By.CSS_SELECTOR,
                            value='span[data-marker="pagination-button/next"]').click()

    driver.quit()


if __name__ == "__main__":
    cb_rf()
    create_table()
    avito_parser()
    exporting()
