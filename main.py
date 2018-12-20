import requests
import os
import argparse
from dotenv import load_dotenv


load_dotenv()
token = os.getenv('token')


def create_bitlink(token, url):
    long_url = {"long_url": url}
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.post('https://api-ssl.bitly.com/v4/shorten', headers=headers, json=long_url)
    if response.status_code == requests.codes.ok:
        short_url_info = response.json()
        return short_url_info['link']
    else:
        return None


def amount_clicks_per_bitlink(token, bitlink):
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.get('https://api-ssl.bitly.com/v4/bitlinks/' + bitlink + '/clicks/summary', headers=headers)
    bitlink_clicks_info = response.json()
    return str(bitlink_clicks_info['total_clicks'])


def is_bitlink(token, url):
    headers = {'Authorization': 'Bearer ' + token}
    response = requests.get('https://api-ssl.bitly.com/v4/bitlinks/' + url, headers=headers)
    if response.status_code == requests.codes.ok:
        return True
    elif response.status_code == 404:
        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="длинная ссылка или битлинк", type=str)
    url = parser.parse_args()
    url = url.url
    if is_bitlink(token, url):
        print("Total click: " + amount_clicks_per_bitlink(token, url))
    else:
        result = create_bitlink(token, url)
        if result is not None:
            print(result)
        else:
            print("Invalid URL")
