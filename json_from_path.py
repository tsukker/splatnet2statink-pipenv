import datetime as dt
import http
import json
import os
import sys
import termios
import time

import requests

from api import Api

if __name__ == '__main__':
    api = Api()
    print('path:')
    path = input()
    if path == '':
        path = '/results'
    elif path[0] != '/':
        path = '/' + path
    resp = api.request(path)
    assert (resp.status_code == http.HTTPStatus.OK)
    if getattr(sys, 'frozen', False):
        app_path = os.path.dirname(sys.executable)
    elif __file__:
        app_path = os.path.dirname(__file__)
    print('json filename:')
    filename = input()
    if filename == '':
        filename = '{}_{}.json'.format(
            path.replace('/', ''),
            dt.datetime.now().strftime('%Y%m%d%H%M'))
    filepath = os.path.join(app_path, filename)
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
