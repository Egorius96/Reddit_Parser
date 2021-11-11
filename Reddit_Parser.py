import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime, timedelta


def get_html_code(url):
    driver = webdriver.Chrome(
        executable_path='G:\YandexDisk\study\Python\PycharmProjects\Reddit_Parser\chromedriver.exe')
    try:
        driver.get(url=url)
        while True:
            posts = 0
            while posts <= 5:
                posts = driver.page_source.count('_eYtD2XCVieq6emjKBH3m')
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            main_html_code = driver.page_source
            return main_html_code
    except Exception as _ex:
        print(_ex)
    finally:
        driver.close()
        driver.quit()


def get_user_urls(main_html_code):
    user_url = []
    soup = BeautifulSoup(main_html_code, 'html.parser').find_all('a', attrs={'class' : '_2tbHP6ZydRpjI44J3syuqC'})
    for link in soup:
        user_url.append('https://www.reddit.com/' + link.get('href'))
    return user_url


def get_data(main_html_code):
    data = []
    element = BeautifulSoup(main_html_code, 'html.parser').find_all('div', attrs={'class' : '_1oQyIsiPHYt6nx7VOmd1sz'})
    for post in element:
        try:
            if len(data) <= 4:
                data.append({
                    'username' : post.find('a', attrs={'class' : '_2tbHP6ZydRpjI44J3syuqC'}).text[2:],
                    'number of comments' : post.find('span', attrs={'class' : 'FHCV02u6Cp2zYL0fhQPsO'}).text.split(' ')[0],
                    'number of votes': post.find('div', attrs={'class': '_1rZYMD_4xY3gRcSS3p8ODO'}).text,
                    'post category': post.find('a', attrs={'class': '_3ryJoIoycVkA88fy40qNJc'}, text=True).text[2:],
                })
            else: pass
        except Exception as _ex:
            print(_ex)
    return data

def get_date(main_html_code):
    element = BeautifulSoup(main_html_code, 'html.parser').find_all('div', attrs={'class': '_1oQyIsiPHYt6nx7VOmd1sz'})
    for post in element:
        try:
            str = post.find('a', attrs={'class': '_3jOxDPIQ0KaOWpzvSQo-1s'}).text
            if 'days' or 'day' in str:
                date = (datetime.today() - timedelta(int(str.split(' ')[0]))).strftime('%Y %m %d')
            else:
                num = datetime.today().strftime('%Y %m %d')
        except Exception as _ex:
            print(_ex)


def main():
    main_html_code = get_html_code(url='https://www.reddit.com/top/?t=month')
    user_urls = get_user_urls(main_html_code)
    # data = get_data(main_html_code)
    print(user_urls)
    # get_date(main_html_code)
    # with open('result.txt', 'w', encoding="utf-8") as result:
    #     result.write(str(post_urls))


if __name__ == "__main__":
    main()