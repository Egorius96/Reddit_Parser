import requests
from bs4 import BeautifulSoup
import time
from selenium import webdriver


def spider():
    url = 'https://www.reddit.com/top/?t=month'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    with open('result.txt', 'w', encoding="utf-8") as result:
        result.write(str(soup.encode("utf-8")))

#spider()


def get_html_code(url):
    driver = webdriver.Chrome(
        executable_path='G:\YandexDisk\study\Python\PycharmProjects\Reddit_Parser\chromedriver.exe'
    )

    #driver.maximize_window()

    try:
        driver.get(url=url)
        time.sleep(3)
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


def main():
    get_html_code(url='https://www.reddit.com/top/?t=month')


if __name__ == "__main__":
    main()