import configparser

import requests

config = configparser.ConfigParser()
config.read('setting.ini')
yandex_token = config['TOKEN']['yandex_token']

def create_path(file_name: str):
    base_url_YA = 'https://cloud-api.yandex.net/v1/disk/resources'
    headers = {
        "Authorization": f"OAuth {yandex_token}"
    }
    url = f'{base_url_YA}'
    params = {
              'path': file_name
              }
    responses = requests.put(url, headers=headers, params=params)
    if responses.status_code == 409:
        return 'already created'
    elif 200 <= responses.status_code < 300:
        return 'created'
    else:
        return responses.json()

if __name__=='__main__':
    print(create_path("testing_"))