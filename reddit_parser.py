import os.path, uuid, logging
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime, timedelta


def get_html_code(url: str) -> str:
    ''' get html code is 150 posts in size from main reddit page '''
    driver = webdriver.Chrome(
        executable_path=(os.getcwd() + '\chromedriver.exe'))
    try:
        driver.get(url=url)
        while True:
            posts = 0
            while posts <= 150:
                posts = driver.page_source.count('_eYtD2XCVieq6emjKBH3m')
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            main_html_code = driver.page_source
            return main_html_code
    except Exception as _ex:
        logging.basicConfig(filename='log-' + datetime.now().strftime('%Y%m%d%H%M') + '.txt',
                            level=logging.WARNING)
        logging.warning(_ex)
    finally:
        driver.close()
        driver.quit()


def get_user_urls(main_html_code: str) -> list:
    ''' collecting all user urls from main reddit page '''
    user_url = []
    soup = BeautifulSoup(main_html_code, 'html.parser').find_all('a', attrs={'class' : '_2tbHP6ZydRpjI44J3syuqC'})
    for link in soup:
        user_url.append('https://www.reddit.com/' + link.get('href'))
    return user_url


def get_date(main_html_code: str) -> list:
    ''' collecting the date of each post from main reddit page
    and conversion to the required format using datetime '''
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
        except Exception as _ex: pass
    return date


def get_data(main_html_code: str, user_urls: list, date: list) -> list:
    ''' data parsing using html main reddit page, user urls, date,
    adding ready-made data to the list of dictionaries '''
    data = []

    # adding UNIQUE_ID, post URL, username, number of comments, number of votes, post category
    element = BeautifulSoup(main_html_code, 'html.parser').find_all('div', attrs={'class' : '_1oQyIsiPHYt6nx7VOmd1sz'})
    for post in element:
        try:
            data.append({
                'UNIQUE_ID': uuid.uuid1().hex,
                'post URL': post.find('a', attrs={'class': '_3jOxDPIQ0KaOWpzvSQo-1s'}).get('href'),
                'username' : post.find('a', attrs={'class' : '_2tbHP6ZydRpjI44J3syuqC'}).text[2:],
                'number of comments' : post.find('span', attrs={'class' : 'FHCV02u6Cp2zYL0fhQPsO'}).text.split(' ')[0],
                'number of votes': post.find('div', attrs={'class': '_1rZYMD_4xY3gRcSS3p8ODO'}).text,
                'post category': post.find('a', attrs={'class': '_3ryJoIoycVkA88fy40qNJc'}, text=True).text[2:],
            })
        except Exception as _ex:
            logging.basicConfig(filename='log-' + datetime.now().strftime('%Y%m%d%H%M') + '.txt',
                                level=logging.WARNING)
            logging.warning(f'{_ex} - Page content is unavailable or user has been deleted')

    # adding post karma, comment karma, user cake day
    driver = webdriver.Chrome(
        executable_path='G:\YandexDisk\study\Python\PycharmProjects\Reddit_Parser\chromedriver.exe')
    for index, user_url in enumerate(user_urls):
        try:
            driver.get(url=user_url)
            user_html_code = driver.page_source
            data[index]['post karma'] = BeautifulSoup(user_html_code, 'html.parser').find('span', class_='karma').text
            data[index]['comment karma'] = BeautifulSoup(user_html_code, 'html.parser').find('span', class_='comment-karma').text
            cake_day = str(BeautifulSoup(user_html_code, 'html.parser').find('span', class_='age').find('time'))
            data[index]['user cake day'] = cake_day[cake_day.find('title="') + 7: cake_day.find(' UTC')]
        except Exception as _ex:
            logging.basicConfig(filename='log-' + datetime.now().strftime('%Y%m%d%H%M') + '.txt',
                                level=logging.WARNING)
            logging.warning(f'{_ex} {user_url} - Page content is unavailable or user has been deleted')
    driver.close()
    driver.quit()

    # adding post date
    try:
        for index in range(len(date) - 1):
            data[index]['post date'] = date[index]
    except Exception as _ex:
        logging.basicConfig(filename='log-' + datetime.now().strftime('%Y%m%d%H%M') + '.txt',
                            level=logging.WARNING)
        logging.warning(f'{_ex} - Page content is unavailable or user has been deleted')
    return data


def write_file(data: list) -> None:
    ''' writing data to file '''
    count: int = 0
    file_name: str = 'reddit-' + datetime.now().strftime('%Y%m%d%H%M') + '.txt'

    # deleting file with same name
    if os.path.exists(file_name):
        with open(file_name, 'w'):
            pass

    # writing data to a file in a readable format; checking
    # for integrity of information, if information isn't
    # fully collected, all data about the post is skipped;
    # fixing the number of posts = 100
    for index in data:
        if len(index) == 10:
            if count == 100:
                break
            else:
                with open(file_name, 'a', encoding="utf-8") as result:
                    for key, value in index.items():
                        if key == 'post date':
                            result.write(f'{key} - {value}\n')
                            count += 1
                            if count == 100:
                                break
                        else:
                            result.write(f'{key} - {value}; ')


def main():
    main_html_code = get_html_code(url='https://www.reddit.com/top/?t=month')
    user_urls = get_user_urls(main_html_code)
    date = get_date(main_html_code)
    data = get_data(main_html_code, user_urls, date)
    write_file(data)


if __name__ == "__main__":
    main()