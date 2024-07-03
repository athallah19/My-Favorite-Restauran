import requests
from bs4 import BeautifulSoup

url = "https://www.spacex.com/launches/"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
data = requests.get(url, headers=headers)

req = data.text
soup = BeautifulSoup(req, 'html.parser')

items = soup.select('.item')
for item in items:
    date = item.select_one('.date').text.strip()
    label = item.select_one('.label').text.strip()
    print(date, label)