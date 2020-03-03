import copy
import http
import time

import requests

from config import Config


class Api(object):
    def _prepare_request_args(self, **kwargs):
        headers = copy.deepcopy(self.base_headers)
        headers.update(kwargs.get("headers", {}))
        kwargs["headers"] = headers
        cookies = dict(iksm_session=self.config.get("cookie"))
        kwargs["cookies"] = cookies
        return kwargs

    def request(self, path, **kwargs):
        method = kwargs.get("method", "GET")
        base_url = "https://app.splatoon2.nintendo.net/api"
        url = base_url + path
        retry_num = 2
        for _ in range(retry_num):
            kwargs_ = self._prepare_request_args(**kwargs)
            resp = requests.request(method=method, url=url, **kwargs_)
            if resp.status_code == http.HTTPStatus.OK:
                return resp
            else:
                self.config.update_cookie("auth")
        else:
            print(f"Authentication failed. Last response from {url} :")
            print(resp.json())

    def __init__(self, **kwargs):
        self.config = Config()
        app_unique_id = "32449507786579989234"
        app_user_agent = "Mozilla/5.0 (Linux; Android 7.1.2; Pixel Build/NJH47D; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36"
        self.base_headers = {
            'x-unique-id': app_unique_id,
            'User-Agent': app_user_agent,
            'Referer': 'https://app.splatoon2.nintendo.net/home',
            'Accept-Language': self.config.get("user_lang"),
        }

    def get_records(self, **kwargs):
        path = "/records"
        return self.request(path, **kwargs)

    def get_stages(self, **kwargs):
        path = "/stages"
        return self.request(path, **kwargs)

    def get_stages_id(self, stage_id, **kwargs):
        path = f"/stages/{stage_id}"
        return self.request(path, **kwargs)

    def get_results(self, **kwargs):
        path = "/results"
        return self.request(path, **kwargs)
