"""
-*- coding: utf-8 -*-
@Time    : 18/10/21 12:05 AM
@Author  : Thu Ra
@Email   : thura747@gmail.com
@File    : media-fire-download2.py
@Software: PyCharm
"""
import os
import sys
import argparse
from datetime import datetime

from media_download import MediafireDownloader
from Utilities import Utilities


def create_arg_parser():
    # Creates and returns the ArgumentParser object

    parser = argparse.ArgumentParser(description='Description of your app.')
    parser.add_argument('--downloadDirectory',
                        help='Path to the input directory.')
    # parser.add_argument('--outputDirectory',
    #                     help='Path to the output that contains the resumes.')
    return parser


def main():
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])

    mf = MediafireDownloader()

    mf.dist_folder = os.path.join(os.getcwd(), datetime.now().strftime("%Y%m%d"))
    if parsed_args.downloadDirectory:
        mf.dist_folder = parsed_args.downloadDirectory
    download_list_file = os.path.join(os.getcwd(), "download_list.csv")
    utilities = Utilities(download_list_file)
    mf_keys = utilities.downloading_list()
    for mf_key in mf_keys:
        print(mf_key)

        downloading = mf.download_file(mf_key.strip())
        if downloading['return']:
            utilities.inserting_record(downloading)


if __name__ == "__main__":
    main()


