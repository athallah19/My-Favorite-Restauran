from tracemalloc import start
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep
from pymongo import MongoClient
import certifi
import requests

password = 'sparta'
cxn_str = f'mongodb+srv://test:{password}@cluster0.5qv8bta.mongodb.net/?retryWrites=true&w=majority'
client = MongoClient(cxn_str)
db = client.dbsparta2

driver = webdriver.Chrome('./chromedriver')

url = "https://www.yelp.com/search?cflt=restaurants&find_loc=San+Francisco%2C+CA"

driver.get(url)

sleep(5)

driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')

sleep(3)

acces_token = 'pk.eyJ1IjoiYXRoYWxsYWgxOSIsImEiOiJjbGJkY2V6OXcxMXZsM3BwaWdlMWZ5eThmIn0.ZCWnInKFjUgeDKsA6NHYkw'
long = -122.420679
lat = 37.772537

start = 0

seen = {}

for _ in range(5):
    req = driver.page_source
    soup = BeautifulSoup(req, 'html.parser')
    restaurants = soup.select('div[class*="arrange-unit__"]')
    for restaurant in restaurants:
        business_name = restaurant.select_one('div[class*="businessName__"]')
        if not business_name:
            continue

        name = business_name.text.split('.')[-1].strip()

        if name in seen:
            continue

        seen[name] = True

        name = business_name.text.split('.')[-1].strip()
        link = business_name.select_one('a')['href']
        link = 'https://www.yelp.com' + link

        categories_price_location = restaurant.select_one('div[class*="priceCategory__"]')
        spans = categories_price_location.select('span')
        categories = spans[0].text.strip()
        location = spans[-1].text.strip()

        geo_url = f"https://api.mapbox.com/geocoding/v5/mapbox.places/{location}.json?proximity={long},{lat}&access_token={acces_token}"
        geo_response = requests.get(geo_url)
        geo_json = geo_response.json()
        center = geo_json['features'][0]['center']

        print(name, ',', categories, ',', location, ',', link)

        doc = {
            'name': name,
            'categories': categories,
            'location': location,
            'coordinates': center,
        }
        db.restaurants.insert_one(doc)

    start += 10
    driver.get(f'{url}&start={start}')
    sleep(3)

driver.quit()