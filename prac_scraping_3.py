from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep

driver = webdriver.Chrome('.\chromedriver.exe')
url = "https://www.airbnb.co.id/s/Seoul/homes?place_id=ChIJzWXFYYuifDUR64Pq5LTtioU&query=Seoul&refinement_paths%5B%5D=%2Fhomes&tab_id=home_tab&_set_bev_on_new_domain=1670310904_ZTk0ZWI2MWUwNDA5"
driver.get(url)
sleep(5)

driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
sleep(5)

req = driver.page_source
driver.quit()
soup = BeautifulSoup(req, 'html.parser')

images = soup.select('img')
for image in images:
    print(image['src'])