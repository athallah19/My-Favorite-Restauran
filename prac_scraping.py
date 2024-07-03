import requests
from bs4 import BeautifulSoup

url = "https://clist.by/"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
}
data = requests.get(url, headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')

contests = soup.find_all('div', {
    'class': ['contests', 'row']
})

for contest in contests:
    start_time = contest.select_one('.start-time')
    if not start_time:
        continue

    time_left = contest.select_one('.timeleft').text.strip()
    duration = contest.select_one('.duration').text.strip()
    start_time = start_time.text.strip()
    event = contest.select_one('.title_search').text.strip()

    print(start_time, duration, time_left, event)