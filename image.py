#!/usr/bin/env python
# encoding: utf-8
"""
@project:artist_api_test
@author:cloudy
@site:
@file:image.py
@date:2018/1/26 13:59
@description: 对图片处理获得base64
"""

import base64
import os
suffix_list = ["jpg"]


def media_base64():
    """
    图片base64
    :return:
    """
    media_path = os.path.join(os.getcwd(), "test_media")
    files = os.walk(media_path)
    for line in files:
        media_files = line[2]
        for media in media_files:
            file_path = os.path.join(media_path, media)
            filename, suffix = media.split(".")
            if suffix not in suffix_list:
                os.remove(file_path)
                continue
            f = open(file_path)
            base64_data = base64.b64encode(f.read())
            f.close()
            filename_str = os.path.join(media_path, "{}.txt".format(filename))
            if os.path.exists(filename_str):
                os.remove(filename_str)
            f = open(filename_str,"w")
            f.write(base64_data)
            f.close()


if __name__ == "__main__":
    media_base64()
