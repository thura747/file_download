"""
-*- coding: utf-8 -*-
@Time    : 18/10/2021 19:59
@Author  : Thu Ra
@Email   : thura747@gmail.com
@File    : media_download.py
@Software: PyCharm
"""
import os
import errno
import time
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import mediafire


class MediafireDownloader:
    dl_file_name = ''
    dl_file_full_path = ''
    dl_total_file_size = 0
    dl_existing_file_size = 0

    dl_page_url = ''
    dl_file_url = ''

    def __init__(self):
        self.dist_folder = None
        self.chunk_size = 1024  # 32KB
        # self.path = None
        self.media_fire_api = mediafire.MediaFireApi()
        pass

    def check_path_exists(self):
        """ checking the folder path is exists or not. If it isn't exists, create a new folder

            :return:
        """
        if not os.path.exists(self.dist_folder):
            try:
                os.makedirs(self.dist_folder)

            except OSError as exception:
                if exception.errno != errno.EEXIST:
                    raise

    def check_media_key(self, key):
        try:
            self.media_fire_api.file_get_info(key)
            return True
        except mediafire.api.MediaFireApiError as e:
            print("Incorrect Key: ", key)

    # @staticmethod
    def download_file(self, mediafire_key):
        """ Downloading file from media fire by key
            :mediafire_file_link: mediafire link to download
            :return:
        """

        if self.check_media_key(mediafire_key):
            response = self.media_fire_api.file_get_links(mediafire_key)

            self.dl_page_url = response['links'][0]['normal_download']
            print('----------------')
            print('Getting link from ' + self.dl_page_url)

            # Get download element
            r_download_page = requests.get(self.dl_page_url)
            soup_download_page = BeautifulSoup(r_download_page.text, 'lxml')
            links = []
            for link in soup_download_page.find_all('a'):
                links.append(link.get('href'))

            download_link_element = soup_download_page.select_one('.popsok')

            download_link_element_str = str(download_link_element)

            # Get download link from download element
            link_start = download_link_element_str.find('"http://') + 1
            link_end = download_link_element_str.find('";', link_start)

            self.dl_file_url = links[7]

            # Get file_name & file_size from HTTP head request
            header_request = requests.head(self.dl_file_url)
            self.dl_total_file_size = int(header_request.headers['Content-Length'])

            cd = header_request.headers['content-disposition']
            file_name_key = 'filename="'
            fn_start = cd.find(file_name_key) + len(file_name_key)
            fn_end = cd.find('"', fn_start)

            self.dl_file_name = cd[fn_start:fn_end]
            self.check_path_exists()
            self.dl_file_full_path = os.path.join(self.dist_folder, self.dl_file_name)

            # If file already exist, resume. Otherwise create new file
            if os.path.exists(self.dl_file_full_path):
                output_file = open(self.dl_file_full_path, 'ab')
                self.dl_existing_file_size = int(os.path.getsize(self.dl_file_full_path))
            else:
                output_file = open(self.dl_file_full_path, 'wb')

            if self.dl_existing_file_size == self.dl_total_file_size:
                print('File "' + str(os.path.join(self.dl_file_name)) + '" Already downloaded.')
                print('-------------------------')
                time.sleep(2)
            else:
                print('Resuming "' + self.dl_file_full_path + '".')
                # Add header to resume download
                headers = {'Range': 'bytes=%s-' % self.dl_existing_file_size}
                r = requests.get(self.dl_file_url, headers=headers, stream=True)
                pbar = tqdm(total=self.dl_total_file_size, initial=self.dl_existing_file_size, unit='B', unit_scale=True)
                for chunk in r.iter_content(self.chunk_size):
                    output_file.write(chunk)
                    pbar.update(self.chunk_size)

                output_file.close()
                pbar.close()
                pbar.refresh()

                print('Finished Downloading "' + self.dl_file_full_path + '".')
                print('-------------------------')

            data = {
                "return": True,
                "name": self.dl_file_name,
                "size": self.dl_total_file_size,
                "key": mediafire_key
            }
            return data
        else:
            data = {
                "return": False
            }
            return data
