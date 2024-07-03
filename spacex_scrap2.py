from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

driver = webdriver.Chrome('.\chromedriver.exe')
url = " https://www.spacex.com/launches/"
driver.get(url)
sleep(5)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(5)

req = driver.page_source
driver.quit()
soup = BeautifulSoup(req, 'html.parser')

items = soup.select('.item')
for item in items:
    date = item.select_one('.date').text.strip()
    label = item.select_one('.label').text.strip()
    print(date, label)