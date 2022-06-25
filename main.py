import os
import requests
from urllib.parse import urlparse
import argparse
from dotenv import load_dotenv
load_dotenv()


def is_bitlink(url, token):
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{url}',
        headers={'Authorization': f'Bearer {token}'}
    )
    return response.ok


def shorten_link(url, token):
    response = requests.post(
        'https://api-ssl.bitly.com/v4/bitlinks',
        json={'long_url': url},
        headers={'Authorization': f'Bearer {token}'}
    )
    response.raise_for_status()
    return response.json()['link']


def count_clicks(url, token):
    response = requests.get(
        f'https://api-ssl.bitly.com/v4/bitlinks/{url}/clicks/summary',
        headers={'Authorization': f'Bearer {token}'}
    )
    response.raise_for_status()
    return response.json()['total_clicks']


def main():
    parser = argparse.ArgumentParser(description='Сокращает ссылки или показывает статистику переходов по ним')
    parser.add_argument('url', help='URL веб-страницы или короткая ссылка')
    args = parser.parse_args()

    parsed_user_url = urlparse(args.url)
    url_without_scheme = f'{parsed_user_url.netloc}{parsed_user_url.path}'
    url_with_scheme = f'{parsed_user_url.scheme}://{url_without_scheme}'

    bitly_token = os.getenv('BITLY_TOKEN')
      
    try:
        if is_bitlink(url_without_scheme, bitly_token):
            clicks = count_clicks(url_without_scheme, bitly_token)
            return f'Битлинк кликнули {clicks} раз(а)'
        else:
            bitlink = shorten_link(url_with_scheme, bitly_token)
            return f'Битлинк: {bitlink}'
    except requests.exceptions.HTTPError:
        return 'Неверный запрос'

if __name__ == '__main__':
    print(main())
