#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, re, time
import requests


def main():
    image_in_path = sys.argv[1]
    image_out_path = sys.argv[2]

    kraken(image_in_path, image_out_path)


def kraken(image_path, path):
    image_name = image_path.split('/')[-1]
    file_type = image_name.split('.')[-1]
    path = path if path[-1] == '/' else path + '/'

    user_agent = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0"
    main_url = "https://kraken.io/web-interface"
    post_url = "https://kraken.io/uploader"
    #post_url = 'http://httpbin.org/post'

    s = requests.Session()

    resp = s.get(main_url, headers={'User-Agent': user_agent})
    #print(resp.headers)
    xsrf_token = get_xsrf_token(resp.headers['set-cookie'])

    headers = {
        'User-Agent': user_agent,
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'ru,en-US;q=0.7,en;q=0.3',
        'X-XSRF-TOKEN': xsrf_token,
        'Referer': main_url
    }
    time.sleep(1)
    data = [
        ('lossy', (None, 'false')),
        ('file', ('{}'.format(image_name), open(image_path, 'rb'), "image/{}".format(file_type)))
    ]

    resp = s.post(post_url, headers=headers, files=data)
    #print(resp.json())
    d = resp.json()
    print("Compress coef: {}".format(d['optimizedSize'] / d['originalSize']))
    img_url = d['url']
    r = s.get(img_url, headers={'User-Agent': user_agent}, stream=True)
    if r.status_code == 200:
        with open(path + image_name, 'wb') as f:
            for chunk in r.iter_content(1024):
                f.write(chunk)
    print('File download ok')


def get_xsrf_token(xsrf_str):
    xsrf_token = re.search("XSRF-TOKEN=([^;]+);", xsrf_str).group(1)
    return xsrf_token

if __name__ == '__main__':
    main()

