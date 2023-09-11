import requests
import os
import json
from multiprocessing.dummy import Pool as ThreadPool
from datetime import datetime
import logging


def get_html(url: str) -> str:
    """
    Вытягивание html файла страницы
    url: Коенчный путь к сайту
    """
    try:
        html = requests.get(url)
    except:
        raise Exception
    if(html.status_code != 200):
        print(html.status_code)
        raise Exception
    return html.text

def worker(i):
    currentFile = "{}.json".format(i)

    if os.path.isfile(currentFile):
        logging.info("{} - File exists".format(i))
        return 1

    url = "https://m.habr.com/kek/v1/articles/{}/?fl=ru%2Cen&hl=ru".format(i)
    try:
        r = get_html(url)
    except:
        return Exception

    data = json.loads(r.text)

    if data['success']:
        article = data['data']['article']

        id = article['id']
        is_tutorial = article['is_tutorial']
        time_published = article['time_published']
        comments_count = article['comments_count']
        lang = article['lang']
        tags_string = article['tags_string']
        title = article['title']
        content = article['text_html']
        reading_count = article['reading_count']
        author = article['author']['login']
        score = article['voting']['score']

        data = (id, is_tutorial, time_published, title, content, comments_count, lang, tags_string, reading_count, author, score)
        with open(currentFile, "w") as write_file:
            json.dump(data, write_file)

min = int(400000)
max = int(500000)

# Если потоков >3
# то хабр банит ipшник на время
pool = ThreadPool(3)
sites_pool = [705906, 705308]
# Отсчет времени, запуск потоков
start_time = datetime.now()
results = pool.map(worker, sites_pool)

# После закрытия всех потоков печатаем время
pool.close()
pool.join()
print(datetime.now() - start_time)

