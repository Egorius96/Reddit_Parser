import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def spider():
    url = 'https://www.reddit.com/top/?t=month'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    with open('result.txt', 'w', encoding="utf-8") as result:
        result.write(str(soup.prettify())) #.encode("utf-8")))


def get_html_code(url):
    driver = webdriver.Chrome(
        executable_path='G:\YandexDisk\study\Python\PycharmProjects\Reddit_Parser\chromedriver.exe')
    try:
        driver.get(url=url)
        while True:
            posts = 0
            while posts <= 100:
                posts = driver.page_source.count('_eYtD2XCVieq6emjKBH3m')
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            break
    except Exception as _ex:
        print(_ex)
    finally:
        main_html_code = driver.page_source
        driver.close()
        driver.quit()
        return main_html_code


def get_post_urls(main_html_code):
    post_urls = []
    soup = BeautifulSoup(main_html_code, 'html.parser').find_all('a', attrs={'class' : '_3jOxDPIQ0KaOWpzvSQo-1s'})
    for link in soup:
        post_urls.append(link.get('href'))
    return post_urls


def main():
    #spider()
    main_html_code = get_html_code(url='https://www.reddit.com/top/?t=month')
    post_urls = get_post_urls(main_html_code)
    # with open('result.txt', 'w', encoding="utf-8") as result:
    #     result.write(str(post_urls))


if __name__ == "__main__":
    main()