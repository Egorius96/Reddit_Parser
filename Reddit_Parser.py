import requests
from bs4 import BeautifulSoup
import urllib.request

def spider():
    url = 'https://www.reddit.com/top/?t=month'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    with open('result.txt', 'w', encoding="utf-8") as result:
        result.write(str(soup.encode("utf-8")))

    #print(soup.prettify())

spider()





# post_url = urllib.request.urlopen("https://www.reddit.com/r/antiwork/comments/q82vqk/quit_my_job_last_night_it_was_nice_to_be_home_to/")
# print (post_url.read())


