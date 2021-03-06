# coding: utf-8
"""
ЗАДАНИЕ

Выбрать источник данных и собрать данные по некоторой предметной области.

Цель задания - отработать навык написания программ на Python.
В процессе выполнения задания затронем области:
- организация кода в виде проекта, импортирование модулей внутри проекта
- unit тестирование
- работа с файлами
- работа с протоколом http
- работа с pandas
- логирование

Требования к выполнению задания:

- собрать не менее 1000 объектов

- в каждом объекте должно быть не менее 5 атрибутов
(иначе просто будет не с чем работать.
исключение - вы абсолютно уверены что 4 атрибута в ваших данных
невероятно интересны)

- сохранить объекты в виде csv файла

- считать статистику по собранным объектам


Этапы:

1. Выбрать источник данных.

Это может быть любой сайт или любое API

Примеры:
- Пользователи vk.com (API)
- Посты любой популярной группы vk.com (API)
- Фильмы с Кинопоиска
(см. ссылку на статью ниже)
- Отзывы с Кинопоиска
- Статьи Википедии
(довольно сложная задача,
можно скачать дамп википедии и распарсить его,
можно найти упрощенные дампы)
- Статьи на habrahabr.ru
- Объекты на внутриигровом рынке на каком-нибудь сервере WOW (API)
(желательно англоязычном, иначе будет сложно разобраться)
- Матчи в DOTA (API)
- Сайт с кулинарными рецептами
- Ebay (API)
- Amazon (API)
...

Не ограничивайте свою фантазию. Это могут быть любые данные,
связанные с вашим хобби, работой, данные любой тематики.
Задание специально ставится в открытой форме.
У такого подхода две цели -
развить способность смотреть на задачу широко,
пополнить ваше портфолио (вы вполне можете в какой-то момент
развить этот проект в стартап, почему бы и нет,
а так же написать статью на хабр(!) или в личный блог.
Чем больше у вас таких активностей, тем ценнее ваша кандидатура на рынке)

2. Собрать данные из источника и сохранить себе в любом виде,
который потом сможете преобразовать

Можно сохранять страницы сайта в виде отдельных файлов.
Можно сразу доставать нужную информацию.
Главное - постараться не обращаться по http за одними и теми же данными много раз.
Суть в том, чтобы скачать данные себе, чтобы потом их можно было как угодно обработать.
В случае, если обработать захочется иначе - данные не надо собирать заново.
Нужно соблюдать "этикет", не пытаться заддосить сайт собирая данные в несколько потоков,
иногда может понадобиться дополнительная авторизация.

В случае с ограничениями api можно использовать time.sleep(seconds),
чтобы сделать задержку между запросами

3. Преобразовать данные из собранного вида в табличный вид.

Нужно достать из сырых данных ту самую информацию, которую считаете ценной
и сохранить в табличном формате - csv отлично для этого подходит

4. Посчитать статистики в данных
Требование - использовать pandas (мы ведь еще отрабатываем навык использования инструментария)
То, что считаете важным и хотели бы о данных узнать.

Критерий сдачи задания - собраны данные по не менее чем 1000 объектам (больше - лучше),
при запуске кода командой "python3 -m gathering stats" из собранных данных
считается и печатается в консоль некоторая статистика

Код можно менять любым удобным образом
Можно использовать и Python 2.7, и 3

Зачем нужны __init__.py файлы
https://stackoverflow.com/questions/448271/what-is-init-py-for

Про документирование в Python проекте
https://www.python.org/dev/peps/pep-0257/

Про оформление Python кода
https://www.python.org/dev/peps/pep-0008/


Примеры сбора данных:
https://habrahabr.ru/post/280238/

Для запуска тестов в корне проекта:
python3 -m unittest discover

Для запуска проекта из корня проекта:
python3 -m gathering gather
или
python3 -m gathering transform
или
python3 -m gathering stats


Для проверки стиля кода всех файлов проекта из корня проекта
pep8 .

setlist.fm
API Key c985ee98-9b2e-4d35-9328-8fb3bdf10953

"""

import logging

import sys
import pandas as pd
from datetime import datetime
from pprint import pprint

from scrappers.scrapper import Scrapper
from storages.json_storage import JsonStorage

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


JSON_FILES_PATH = './jsons/'
TABLE_FORMAT_FILE = 'data.csv'


def gather_process():
    logger.info("gather")
    storage = JsonStorage(JSON_FILES_PATH)

    # You can also pass a storage
    scrapper = Scrapper()
    scrapper.scrap_process(storage)


def convert_data_to_table_format():
    logger.info("transform")
    data_frame_dict = {'name': [], 'date': [], 'venue': [], 'tour': [], 'has_setlist': []}
    for page, json in JsonStorage(JSON_FILES_PATH).read_json():
        for setlist in json['setlist']:
            data_frame_dict['name'].append(setlist['artist']['name'])
            data_frame_dict['date'].append(setlist['eventDate'])
            data_frame_dict['venue'].append(setlist['venue']['name'])
            data_frame_dict['tour'].append(setlist['tour']['name'])
            data_frame_dict['has_setlist'].append(True if len(setlist['sets']['set']) > 0 else False)

    df = pd.DataFrame(data=data_frame_dict)
    df.to_csv(TABLE_FORMAT_FILE, encoding='utf-8')

def stats_of_data():
    logger.info("stats")

    df = pd.read_csv(TABLE_FORMAT_FILE)

    # Сколько концертов всего
    concerts_count = df.shape[0]
    print("1) Всего " + str(concerts_count) + " концертов\n")

    # За какие годы есть данные по концертам
    years = sorted(set([str(datetime.strptime(date, '%d-%m-%Y').year) for date in df['date']]))
    print("2) Годы концертов: \n")
    print('\n'.join(years) + "\n")

    # Сколько артиство дало концерты за это время
    artists_count = len(df['name'].unique())
    print("3) Сколько артистов дало концерты: " + str(artists_count) + "\n")

    # 5 самых популярных площадок
    venues = df['venue'].value_counts().head()
    print("4) 5 самых популярных площадок:\n")
    print(venues)
    print('\n')

    #Сколько концертов с сетлистами
    has_setlist = df[df['has_setlist'] == True].shape[0]
    print("5) Концертов с сетлистами: " + str(has_setlist))

if __name__ == '__main__':
    """
    why main is so...?
    https://stackoverflow.com/questions/419163/what-does-if-name-main-do
    """
    logger.info("Work started")

    if sys.argv[1] == 'gather':
        gather_process()

    elif sys.argv[1] == 'transform':
        convert_data_to_table_format()

    elif sys.argv[1] == 'stats':
        stats_of_data()

    logger.info("work ended")
