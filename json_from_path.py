import datetime as dt
import http
import json
import os
import sys
import termios
import time

import requests

from api import Api


def select_path():
    options = [
        'results',
        'coop_results',
    ]
    for i, path in enumerate(options):
        print('{} : {}'.format(i + 1, path))
    print('Please select (default: 1) : ', end='')
    s = input()
    ret = options[0]
    if s == '2':
        ret = options[1]
    return ret


if __name__ == '__main__':
    api = Api()
    print('path:')
    path = select_path()
    if path == '':
        path = '/results'
    elif path[0] != '/':
        path = '/' + path
    print('path: "{}"'.format(path))
    resp = api.request(path)
    assert (resp.status_code == http.HTTPStatus.OK)
    if getattr(sys, 'frozen', False):
        app_path = os.path.dirname(sys.executable)
    elif __file__:
        app_path = os.path.dirname(__file__)
    json_dir = 'json'
    json_path = os.path.join(app_path, json_dir)
    filename = ''
    if filename == '':
        filename = '{}_{}.json'.format(
            path.replace('/', ''),
            dt.datetime.now().strftime('%Y%m%d%H%M'))
    filepath = os.path.join(json_path, filename)
    f = open(filepath, 'w')
    json.dump(
        resp.json(),
        f,
        indent=2,
        sort_keys=True,
        ensure_ascii=False,
    )
    f.close()
    print(f'Wrote json on "{filepath}"')
