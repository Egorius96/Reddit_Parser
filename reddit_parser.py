import os.path
import argparse
import uuid
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from datetime import datetime, timedelta
from typing import List, Dict, AnyStr, Any


def argparsing() -> List[Any]:
    parser = argparse.ArgumentParser()
    parser.add_argument('-p', '--posts', type=int, help='enter the number of posts', default=100)
    parser.add_argument('-n', '--name', type=str, help='enter the file name', default='default')
    args = parser.parse_args()

    if args.posts != 100:
        post_count = args.posts
    else:
        post_count = 100

    if args.name != 'default':
        file_name = args.name
    else:
        file_name = 'default'

    return [post_count, file_name]


def get_html_code(url: str, post_count: int) -> str:
    """
    Get html code is 150 posts in size from main reddit page

    :param url: str with url
    :param post_count: int value from  argparsing function to determine the number of scrolls
    :return: str with html code from main reddit page
    """
    driver = webdriver.Chrome()
    try:
        driver.get(url=url)
        while True:
            posts = 0
            while posts <= (post_count + int((post_count / 2))):
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


def get_user_urls(main_html_code: str) -> List[AnyStr]:
    """
    Collecting all user urls from main reddit page

    :param main_html_code: str with result of executing get_html_code function
    :return: list wist user urls
    """
    user_url = []
    soup = BeautifulSoup(main_html_code, 'html.parser').find_all('a', attrs={'class': '_2tbHP6ZydRpjI44J3syuqC'})
    for link in soup:
        user_url.append('https://www.reddit.com/' + link.get('href'))
    return user_url


def get_date(main_html_code: str) -> List[AnyStr]:
    """
    Collecting date list

    There was a need to make the calculation the date of creation
    of the post in a separate function because the date is displayed
    on the page in the following form: "14 days ago" or "15 hours ago".
    That is, the words are used: Hours, Days, Months. Therefore, these
    times must be distinguished in order not to take hours away from days.
    Next, the date of each message is collected from the main page of
    reddit and converted to the required format using datetime.

    :param main_html_code: str with result of executing get_html_code function
    :return: list with dates of posts
    """
    post_date = []
    element = BeautifulSoup(main_html_code, 'html.parser').find_all('div', attrs={'class': '_1oQyIsiPHYt6nx7VOmd1sz'})
    for post in element:
        try:
            date_str = post.find('a', attrs={'class': '_3jOxDPIQ0KaOWpzvSQo-1s'}).text
            if 'days' in date_str or 'day' in date_str:
                post_date.append((datetime.today() - timedelta(int(date_str.split(' ')[0]))).strftime('%Y %m %d'))
            elif 'month' in date_str:
                post_date.append((datetime.today() - timedelta(days=30)).strftime('%Y %m %d'))
            else:
                post_date.append(datetime.today().strftime('%Y %m %d'))
        except Exception as _ex:
            post_date.append('Date ERROR')
            logging.basicConfig(filename='log-' + datetime.now().strftime('%Y%m%d%H%M') + '.txt',
                                level=logging.WARNING)
            logging.warning(f'{_ex} - Date ERROR')
    return post_date


def get_data(main_html_code: str, user_urls: list, post_date: list) -> List[Dict[AnyStr, AnyStr]]:
    """
    Data parsing using html main reddit page, user urls, date,
    adding ready-made data to the list of dictionaries

    :param main_html_code: str with result of executing get_html_code function
    :param user_urls: list wist user urls
    :param post_date: list with dates of posts
    :return: list of dictionaries with received data
    """
    data = []

    ''' adding UNIQUE_ID, post URL, username, number of comments, number of votes, post category '''
    element = BeautifulSoup(main_html_code, 'html.parser').find_all('div', attrs={'class': '_1oQyIsiPHYt6nx7VOmd1sz'})
    for post in element:
        try:
            data.append({
                'UNIQUE_ID': uuid.uuid1().hex,
                'post URL': post.find('a', attrs={'class': '_3jOxDPIQ0KaOWpzvSQo-1s'}).get('href'),
                'username': post.find('a', attrs={'class': '_2tbHP6ZydRpjI44J3syuqC'}).text[2:],
                'number of comments': post.find('span', attrs={'class': 'FHCV02u6Cp2zYL0fhQPsO'}).text.split(' ')[0],
                'number of votes': post.find('div', attrs={'class': '_1rZYMD_4xY3gRcSS3p8ODO'}).text,
                'post category': post.find('a', attrs={'class': '_3ryJoIoycVkA88fy40qNJc'}, text=True).text[2:],
            })
        except Exception as _ex:
            logging.basicConfig(filename='log-' + datetime.now().strftime('%Y%m%d%H%M') + '.txt',
                                level=logging.WARNING)
            logging.warning(f'{_ex} - Page content is unavailable or user has been deleted')

    ''' adding post karma, comment karma, user cake day '''
    driver = webdriver.Chrome()
    for index, user_url in enumerate(user_urls):
        try:
            driver.get(url=user_url)
            user_html_code = driver.page_source
            data[index]['post karma'] = BeautifulSoup(user_html_code, 'html.parser').find('span', class_='karma').text
            data[index]['comment karma'] = BeautifulSoup(user_html_code,
                                                         'html.parser').find('span', class_='comment-karma').text
            cake_day = str(BeautifulSoup(user_html_code, 'html.parser').find('span', class_='age').find('time'))
            data[index]['user cake day'] = cake_day[cake_day.find('title="') + 7: cake_day.find(' UTC')]
        except Exception as _ex:
            logging.basicConfig(filename='log-' + datetime.now().strftime('%Y%m%d%H%M') + '.txt',
                                level=logging.WARNING)
            logging.warning(f'{_ex} {user_url} - Page content is unavailable or user has been deleted')
    driver.close()
    driver.quit()

    ''' adding post date '''
    try:
        for index in range(len(data) - 1):
            data[index]['post date'] = post_date[index]
    except Exception as _ex:
        logging.basicConfig(filename='log-' + datetime.now().strftime('%Y%m%d%H%M') + '.txt',
                            level=logging.WARNING)
        logging.warning(f'{_ex} - Page content is unavailable or user has been deleted')
    return data


def write_file(data: list, post_count: int, file_name: str) -> None:
    """
    Writing data to file

    :param data: list of dictionaries with received data from get_data function
    :param post_count: int value from  argparsing function to determine
                       the number of posts in the output file
    :param file_name: str value from argparsing function to determine
                      the file name
    :return: None
    """
    count: int = 0
    ''' checking for a custom file name forced file type .txt '''
    if file_name == 'default':
        file_name: str = 'reddit-' + datetime.now().strftime('%Y%m%d%H%M') + '.txt'
    else:
        if '.' in file_name:
            if file_name.split('.')[1] != 'txt':
                file_name = file_name.split('.')[0] + '.txt'
        else:
            file_name = file_name + '.txt'

    ''' deleting file with same name '''
    if os.path.exists(file_name):
        os.remove(file_name)

    ''' writing data to a file in a readable format;
    checking for integrity of information, if information isn't
    fully collected, i.e. less than 10 data points all data
    about the post is skipped '''
    with open(file_name, 'a', encoding="utf-8") as result:
        for post in data:
            if len(post) == 10:
                if count == post_count:
                    break
                else:
                    for key, value in post.items():
                        if key == 'post date':
                            result.write(f'{key} - {value}\n')
                            count += 1
                        else:
                            result.write(f'{key} - {value}; ')


def main():
    post_count, file_name = argparsing()
    main_html_code = get_html_code(url='https://www.reddit.com/top/?t=month', post_count=post_count)
    user_urls = get_user_urls(main_html_code)
    post_date = get_date(main_html_code)
    data = get_data(main_html_code, user_urls, post_date)
    write_file(data, post_count, file_name)


if __name__ == "__main__":
    main()
