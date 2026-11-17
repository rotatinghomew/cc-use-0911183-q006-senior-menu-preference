from pathlib import Path
import json

from .nutrition import *
from .evidence import *
from .kitchen import *


class Application:
    def __init__(self, store):
        self.store = store

    def seed(self):
        directory = Path(__file__).resolve().parent.parent / 'fixtures'
        for path in sorted(directory.glob('*.json')):
            if not self.store.all(path.stem):
                self.store.put_many(path.stem, json.loads(path.read_text(encoding='utf-8')))

    def demo(self):
        return {'meals': meal_totals(self.store), 'nutrition': nutrition(self.store, 'r1', {'soft_rice': 1}), 'quote': quote_menu(self.store, {'soft_rice': 10, 'fish': 6})}

    def check(self):
        value = self.demo()
        return {'status': 'ok', 'summary': value}

    def call(self, method, route, payload):
        if method == 'GET' and route == 'summary':
            return self.demo()
        if method == 'POST' and route == 'meal':
            return {'revision': save_meal(self.store, payload)}
        if method == 'POST' and route == 'nutrition':
            return nutrition(self.store, payload['resident'], payload['dishes'])
        if method == 'POST' and route == 'kitchen-quote':
            return quote_menu(self.store, payload['portions'])
        raise KeyError('接口不存在')
