from sqlalchemy import create_engine
from selenium import webdriver
from geopy.geocoders import Nominatim
from bs4 import BeautifulSoup
import re
import time
import csv
import pandas as pd

geolocator = Nominatim(user_agent="myGeocoder")
with open('commercial_premises.csv', "w", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(('Name', 'Price', 'Square', 'Address', 'Latitude', 'Longitude', 'Link'))

# Specify the number of pages to parse
num_pages = 1

for i in range(1, num_pages + 1):
    URL = f'https://www.avito.ru/sankt-peterburg/kommercheskaya_nedvizhimost/sdam-ASgBAgICAUSwCNRW?cd={i}&p={i}'
    driver = webdriver.Chrome(
        executable_path="C:\\Users\\Пользователь\\Desktop\\project\\parsing\\parser\\ChromeWebDriver\\chromedriver.exe")

    try:
        driver.get(url=URL)
        main_page = driver.page_source
        time.sleep(1)
        main_source = BeautifulSoup(main_page, "html.parser")
        adt = main_source.find_all('div', class_='iva-item-content-rejJg')
        for item in adt:
            title = item.find('h3', class_='title-root-zZCwT')
            price = item.find('span', class_='price-text-_YGDY')
            price_text = price.text.replace('\xa0', '') if price else None
            address = item.find('div', class_='geo-address-fhHd0')
            location = None
            if address:
                address_text = address.text.strip()
                if '-я' in address_text:
                    address_text = address_text.replace('-я', '')
                if 'В.О.' or 'Васильевского острова' in address_text:
                    address_text = address_text.replace('В.О.', '')
                    address_text = address_text.replace('Васильевского острова', '')
                if 'пр-т' in address_text:
                    address_text = address_text.replace('пр-т', 'проспект')
                if 'Санкт-Петербург' not in address_text and 'Ленинградская область' not in address_text \
                        and 'пос' not in address_text and 'поселок' not in address_text:
                    address_text = 'Санкт-Петербург, ' + address_text
                location = geolocator.geocode(address_text)

            regex = r"(\d+(\.\d+)?)(\s?)(м²|м|м2|кв\.м)"
            title_text = title.text.strip() if title else None
            match = re.search(regex, title_text) if title_text else None
            if match:
                square = float(match.group(1))
            else:
                square = None
            if 'за м²' in price_text:
                price_match = re.search(r'\d+', price_text)
                if price_match:
                    price_value = float(price_match.group()) * square
                else:
                    price_value = None
            else:
                price_match = re.search(r'\d+', price_text)
                if price_match:
                    price_value = float(price_match.group())
                else:
                    price_value = None
            if location is not None:
                latitude = location.latitude
                longitude = location.longitude
            else:
                latitude = None
                longitude = None
            link = item.find('a', class_='link-link-MbQDP')
            link = link.get('href') if link else None
            link = 'https://www.avito.ru' + link if link else None
            with open('commercial_premises.csv', "a", encoding='utf-8', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(
                    (title.text.strip() if title else None, price_value, square,
                     address_text if address else None, latitude, longitude, link.strip() if link else None))

    except Exception as ex:
        print(ex)
    finally:
        driver.quit()
df = pd.read_csv('commercial_premises.csv')
# удаляем строки с пропущенными значениями (NaN)
df = df.dropna()
# записываем измененный DataFrame обратно в csv файл
df.to_csv('commercial_premises.csv', index=False)
engine = create_engine("postgresql://")


data = pd.read_csv('commercial_premises.csv')

with engine.connect() as conn, conn.begin():
    data.to_sql(
        'commercial_premises',
        con=conn,
        if_exists='append',
        index=False
    )