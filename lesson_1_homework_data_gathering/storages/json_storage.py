import json
import os


class JsonStorage:

    def __init__(self, jsons_path):
        self.jsons_path = jsons_path
        if not os.path.exists(os.path.dirname(jsons_path)):
            os.makedirs(os.path.dirname(jsons_path))

    def write_json(self, jsons):
        for page, j in jsons:
            with open(self.jsons_path + str(page) + ".json", "w") as write_file:
                json.dump(j, write_file)

    def read_json(self):
        jsons = []

        for f in os.listdir(self.jsons_path):
            if f.endswith(".json"):
                with open(self.jsons_path + f) as fi:
                    jsons.append((f.split('.')[0], json.load(fi)))

        return jsons

    def get_pages(self):
        pages = []
        for f in os.listdir(self.jsons_path):
            if f.endswith(".json"):
                pages.append(int(f.split('.')[0]))

        return pages

    def get_json_by_page(self, page):
        if os.path.exists(self.jsons_path + str(page) + ".json"):
            with open(self.jsons_path + str(page) + ".json", "r") as f:
                return json.load(f)
        else:
            return None
