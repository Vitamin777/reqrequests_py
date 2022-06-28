# Task 2
import os

from pprint import pprint

import requests

class YaUploader:
    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': 'OAuth {}'.format(self.token)
        }

    def _get_upload_link(self, disk_file_path):
        upload_url = 'https://cloud-api.yandex.net:443/v1/disk/resources/upload'
        headers = self.get_headers()
        params = {"path": disk_file_path, "overwrite": "true"}
        response = requests.get(upload_url, headers=headers, params=params)
        #pprint(response.json())
        return response.json()

    def upload(self, files_path: str, dir: str ):
        """Метод загружает файлы по списку file_list на яндекс диск"""
        # We shall store all the file names in this list
        file_list = []

        for root, dirs, files in os.walk(path_to_files):
            for file in files:
                # Append the file name to the list
                file_list.append(os.path.join(root, file))

        for name in file_list:
            file_name = os.path.basename(name)
            disk_file_path = file_name
            # disk_file_path = dir + '/' + file_name    # Если папка существует на яндекс диске
            response_href = self._get_upload_link(disk_file_path=disk_file_path)
            href = response_href.get("href", "")
            response = requests.put(href, data=open(name, 'rb'))
            response.raise_for_status()
            if response.status_code == 201:
                print(f'Файл {file_name} успешно записан на яндекс диск')


if __name__ == '__main__':

    dir = 'txt_files'

    # Get the path to the file folder
    path_to_files = os.path.dirname(__file__) + '\\' + dir

    # Get token from file token.txt
    with open('token.txt', 'r') as f:
        token = f.readline()

    uploader = YaUploader(token)
    result = uploader.upload(path_to_files, dir)





