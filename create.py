import sqlite3
from bs4 import BeautifulSoup
import os


def create_table():
    connect = sqlite3.connect(r'database/auto.db')
    cursor = connect.cursor()
    create_model = "CREATE TABLE model (auto TEXT, model TEXT, text TEXT, foto TEXT)"
    cursor.execute(create_model)
    create_other = "CREATE TABLE other (auto TEXT, model TEXT, name TEXT, url TEXT)"
    cursor.execute(create_other)
    cursor.close()
    connect.close()


create_table()


def insert_model(add_auto, add_model, add_text=None, add_foto=None):
    connect = sqlite3.connect(r'database/auto.db')
    cursor = connect.cursor()
    insert = "INSERT INTO model VALUES (?, ?, ?, ?)"
    cursor.execute(insert, (add_auto, add_model, add_text, add_foto))
    connect.commit()
    cursor.close()
    connect.close()


def insert_other(add_auto, add_model, add_name, add_url):
    connect = sqlite3.connect(r'database/auto.db')
    cursor = connect.cursor()
    insert = "INSERT INTO other VALUES (?, ?, ?, ?)"
    cursor.execute(insert, (add_auto, add_model, add_name, add_url))
    connect.commit()
    cursor.close()
    connect.close()


soup = {}
catalog = '/home/indexother/Загрузки/htdocs/auto/'
for file in os.listdir(catalog):
    soup[file[:-6]] = BeautifulSoup(open(catalog + file, encoding='UTF-8'), 'html.parser')
for auto in sorted(soup):
    for model in soup[auto].find_all('label'):
        if model.text != '':
            none = ['Manual', 'Video', 'Вырез', 'Штатная', 'Активация']
            for i in none:
                if i in model.text:
                    break
            else:
                model_info = model.find_next_sibling('div').text
                for label in model.find_next_sibling('div').find_all('label'):
                    if 'cutout' in label.get('for'):
                        model_info = model_info.replace(label.text, '')
                        insert_other(auto, model.text, label.text, label.find_next('a').get('href'))
                    if 'manual' in label.get('for'):
                        model_info = model_info.replace(label.text, '')
                        insert_other(auto, model.text, label.text, label.find_next('img').get('src'))
                    if 'video' in label.get('for'):
                        model_info = model_info.replace(label.text, '')
                        insert_other(auto, model.text, label.text, label.find_previous('a').get('href'))
                model_info = model_info.replace('					', '')
                while '\n\n' in model_info:
                    model_info = model_info.replace('\n\n', '\n')
                model_photo_url = ''
                if model.find_next_sibling('div').find('a'):
                    if 'i.ibb.co' in model.find_next_sibling('div').find('a').get('href'):
                        model_photo_url = model.find_next_sibling('div').find('a').get('href')
                model_info = model_info.strip('\n')
                if model_photo_url != '':
                    if model_info != '':
                        insert_model(auto, model.text, model_info, model_photo_url)
                    else:
                        insert_model(auto, model.text, add_foto=model_photo_url)
                else:
                    if model_info != '':
                        insert_model(auto, model.text, model_info)
                    else:
                        insert_model(auto, model.text)
