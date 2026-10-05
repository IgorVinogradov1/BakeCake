import os
import requests
import argparse
from dotenv import load_dotenv
from urllib.parse import urlparse


def is_regular_link(vk_token, user_url):
    payload = {
        'url': user_url,
        'access_token': vk_token,
        'v': '5.199'
    }
    vk_short_link_url = 'https://api.vk.ru/method/utils.getShortLink'
    response = requests.get(vk_short_link_url, params=payload)
    response.raise_for_status()
    return 'error' not in response.json()

def shorten_link(vk_token, user_url):
    payload = {
        'url': user_url,
        'access_token': vk_token,
        'v': '5.199'
    }
    vk_short_link_url = 'https://api.vk.ru/method/utils.getShortLink'
    response = requests.get(vk_short_link_url, params=payload)
    response.raise_for_status()
    return response.json()['response']['short_url']

def count_click(vk_token, link):
    payload = {
        'key': link,
        'access_token': vk_token,
        'v': '5.199'
    }
    vk_link_stats_url = 'https://api.vk.ru/method/utils.getLinkStats'
    response = requests.get(vk_link_stats_url, params=payload)
    response.raise_for_status()
    stats = response.json()['response']['stats']
    return stats[0]['views'] if stats else 0

def main():
    load_dotenv()
    vk_token = os.environ['VK_TOKEN']
    parser = argparse.ArgumentParser(description='Сокращатель ссылок VK')
    parser.add_argument('url', help='Ссылка для обработки')
    args = parser.parse_args()
    user_url = args.url

    if is_regular_link(vk_token, user_url):
        try:
            short_link = shorten_link(vk_token, user_url)
        except KeyError:
            print('Ошибка VK API (getShortLink)!')
            raise SystemExit
        else:
            print('Сокращенная ссылка: ', short_link)
    else:
        link = urlparse(user_url).path[1:]
        try:
            number_of_views = count_click(vk_token, link)
        except KeyError:
            print('Ошибка VK API (getLinkStats)!')
            raise SystemExit
        else:
            print('Количество кликов по ссылке: ', number_of_views)

if __name__ == '__main__':
    main()