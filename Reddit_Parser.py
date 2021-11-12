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
            while posts <= 100:
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


def get_date(main_html_code):
    date = []
    element = BeautifulSoup(main_html_code, 'html.parser').find_all('div', attrs={'class': '_1oQyIsiPHYt6nx7VOmd1sz'})
    for post in element:
        try:
            date_str = post.find('a', attrs={'class': '_3jOxDPIQ0KaOWpzvSQo-1s'}).text
            if 'days' in date_str or 'day' in date_str:
                date.append((datetime.today() - timedelta(int(date_str.split(' ')[0]))).strftime('%Y %m %d'))
            elif 'month' in date_str:
                date.append((datetime.today() - timedelta(days=30)).strftime('%Y %m %d'))
            else:
                date.append(datetime.today().strftime('%Y %m %d'))
        except Exception as _ex:
            print(_ex)
    return date


def get_data(main_html_code, user_urls, date):
    data = []
    element = BeautifulSoup(main_html_code, 'html.parser').find_all('div', attrs={'class' : '_1oQyIsiPHYt6nx7VOmd1sz'})
    for post in element:
        try:
            data.append({
                'username' : post.find('a', attrs={'class' : '_2tbHP6ZydRpjI44J3syuqC'}).text[2:],
                'number of comments' : post.find('span', attrs={'class' : 'FHCV02u6Cp2zYL0fhQPsO'}).text.split(' ')[0],
                'number of votes': post.find('div', attrs={'class': '_1rZYMD_4xY3gRcSS3p8ODO'}).text,
                'post category': post.find('a', attrs={'class': '_3ryJoIoycVkA88fy40qNJc'}, text=True).text[2:],
                'post URL': post.find('a', attrs={'class': '_3jOxDPIQ0KaOWpzvSQo-1s'}).get('href'),
            })
        except Exception as _ex:
            print(_ex)

    driver = webdriver.Chrome(
        executable_path='G:\YandexDisk\study\Python\PycharmProjects\Reddit_Parser\chromedriver.exe')
    for index, user_url in enumerate(user_urls):
        try:
            driver.get(url=user_url)
            user_html_code = driver.page_source
            data[index]['post karma'] = BeautifulSoup(user_html_code, 'html.parser').find('span', class_='karma').text
            data[index]['comment karma'] = BeautifulSoup(user_html_code, 'html.parser').find('span', class_='comment-karma').text
            post_date = str(BeautifulSoup(user_html_code, 'html.parser').find('span', class_='age').find('time'))
            data[index]['cake day'] = post_date[post_date.find('title="') + 7:post_date.find(' UTC')]
        except Exception as _ex:
            print(_ex)
    driver.close()
    driver.quit()

    try:
        for index in range(len(date) - 1):
            data[index]['post date'] = date[index]
    except Exception as _ex:
        print(_ex)
    return data


def main():
    main_html_code = get_html_code(url='https://www.reddit.com/top/?t=month')
    user_urls = get_user_urls(main_html_code)
    date = get_date(main_html_code)
    data = get_data(main_html_code, user_urls, date)
    with open('result.txt', 'w', encoding="utf-8") as result:
        result.write(str(data))


if __name__ == "__main__":
    main()