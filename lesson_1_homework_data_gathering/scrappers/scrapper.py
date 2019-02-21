# coding: utf-8

import logging
import requests
import json

logger = logging.getLogger(__name__)


class Scrapper(object):
    def __init__(self, skip_objects=None):
        self.skip_objects = skip_objects

    def scrap_process(self, storage):
        data = []

        url = 'https://api.setlist.fm/rest/1.0/search/setlists?cityName=Moscow'
        headers = {'Accept': 'application/json', 'x-api-key': 'c985ee98-9b2e-4d35-9328-8fb3bdf10953'}
        payload = {'cityName': 'Moscow', 'p': 1}

        first_page_json = storage.get_json_by_page(1)

        if first_page_json is None:
            first_page = self.get_response(url, headers, payload)
            data.append((1, first_page.json()))
            first_page_json = first_page.json()

        pages_count = first_page_json['total'] / first_page_json['itemsPerPage'] + 1 if \
            first_page_json['total'] % first_page_json['itemsPerPage'] != 0 else \
            first_page_json['total'] / first_page_json['itemsPerPage']

        pages = storage.get_pages()
        for page in range(2, pages_count + 1):
            if page not in pages:
                payload['p'] = page
                response = requests.get(url, headers=headers, params=payload)
                data.append((page, response.json()))

        if len(data) > 0:
            storage.write_json(data)

    def get_response(self, url, headers, payload):
        response = requests.get(url, headers=headers, params=payload)
        if not response.ok:
            logger.error(response.text)
            return None
        else:
            return response
