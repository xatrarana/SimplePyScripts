#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'ipetrash'


"""
Вытаскивание и сохранение на диск файлов логотипов

"""


if __name__ == '__main__':
    FILE_NAME_DICT_LOGO = 'mini_full_dict__CONTACT/logo.xml'
    DIR_LOGO_IMAGES = 'logo_images'

    import os
    if not os.path.exists(DIR_LOGO_IMAGES):
        os.makedirs(DIR_LOGO_IMAGES)

    from bs4 import BeautifulSoup
    root = BeautifulSoup(open(FILE_NAME_DICT_LOGO, 'rb'), 'lxml')

    for row in root.select('rowdata > row'):
        logo_name = row['logo_name']
        print(logo_name)

        logo_data = row['logo_data']
        import base64
        img_data = base64.b64decode(logo_data)

        open(os.path.join(DIR_LOGO_IMAGES, logo_name), 'wb').write(img_data)
