import easyocr
import PIL
import os
import difflib
#from __future__ import barry_as_FLUFL
from PIL import ImageDraw
from functools import lru_cache
import difflib
import logging
import telebot
import psycopg2
from psycopg2 import OperationalError
#from config import reader

reader = easyocr.Reader(['en','ru'], gpu = False)
print('done')
#x = str(input()).lower()
###сортировка файликов в папочке###
unsorted_file_list = os.listdir(path=r"C:\Users\User\Desktop\ocrd\images")
sortetd_file_list = sorted(unsorted_file_list)
os.chdir(path=r"C:\Users\User\Desktop\ocrd\images")
print(sortetd_file_list)

###создание массивика только с картиночками###
image_list = []
for file in sortetd_file_list:
    if '.png' in file:
        image_list.append(file)
    elif '.jpg' in file:
        image_list.append(file)
    elif '.jpeg' in file:
        image_list.append(file)
    elif '.jfif' in file:
        image_list.append(file)
#print(image_list)


###Прогон картиночек###
pile = []
for image in image_list:
    bond = reader.readtext(image)
    pile.append(bond)
#print(pile)


###Фильтр от всякого###
pile_copy = pile.copy()
trash_list = []
# print(pile_copy)
for trash in pile_copy:
    trash = list(map(list, trash))
    # print(trash)
    trash_list.append(trash)
    '''
    for i in trash:
        i= list(map(list,i))
        print(i)
'''

# print(pile_copy)
##print(trash_list)

for trash in trash_list:
    for i in trash:
        i.remove(i[0])
        i.remove(i[1])

# print(trash_list)

tr = []
for i in trash_list:
    i = sum(i, [])
    tr.append(i)
# print(tr)
for i in tr:
    for j in i:
        j.lower()
# print(tr)

###создание массивика строк найденых на картиночках###
ansvers = []
for i in pile:
    for j in i:
        ansvers.append(j[1])
# print(ansvers)

for i in ansvers:
    if i == '':
        i =='None'
### создание словаря###
trash_dict = {key: value for key, value in zip(image_list, tr)}
#print(trash_dict)

###перебор словаря###
for i in trash_dict:
    trash_dict[i] = ' '.join(map(str,trash_dict[i]))
    trash_dict[i] = trash_dict[i].lower()

print(trash_dict)
pict = []
for i in trash_dict.items():
    pict.append(i)
#print(trash_dict.items())
print(pict)
print('done')
###БАЗА###


def create_connection(db_name, db_user, db_password, db_host, db_port):
    connection = None
    try:
        connection = psycopg2.connect(
            database=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print("Connection to PostgreSQL DB successful")
    except OperationalError as e:
        print(f"The error '{e}' occurred")
    return connection


connection = create_connection(
    "postgres", "postgres", "logocentrism1", "localhost", "5432"
)
####Создание базы###

def create_database(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

create_database_query = "CREATE DATABASE Pict_Base"
#create_database(connection, create_database_query)

###коннект###
connection = create_connection(
    "Pict_Base", "postgres", "logocentrism1", "127.0.0.1", "5432"
)

### создание таблицы###

def execute_query(connection, query):
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        print("Query executed successfully")
    except OperationalError as e:
        print(f"The error '{e}' occurred")

create_Picture_table = """
CREATE TABLE IF NOT EXISTS Picture (
  id SERIAL PRIMARY KEY,
  picture_name TEXT NOT NULL, 
  pict_text TEXT
)
"""

execute_query(connection, create_Picture_table)
print('create_Pict_table: done')

###внесение данных в таблицу###
pict_records = ", ".join(["%s"] * len(pict))
insert_query = (
    f"INSERT INTO pict (picture_name, pict_text) VALUES {pict_records}"
)

connection.autocommit = True
cursor = connection.cursor()
cursor.execute(insert_query, pict)
print('information insert into database')
### алгоритмы ###

### Левенштейн ###
def my_dist_cached(a, b):
    @lru_cache(maxsize=len(a) * len(b))
    def recursive(i, j):
        if i == 0 or j == 0:
            return max(i, j)
        elif a[i - 1] == b[j - 1]:
            return recursive(i - 1, j - 1)
        else:
            return 1 + min(
                recursive(i, j - 1),
                recursive(i - 1, j),
                recursive(i - 1, j - 1)
            )
    return recursive(len(a), len(b))

###Коэфициент Танимото###
def tanimoto(s1, s2):
    a, b, c = len(s1), len(s2), 0.0

    for sym in s1:
        if sym in s2:
            c += 1

    return c / (a + b - c)

###Дифлиб###


def simil(s1,s2):
    matcher = difflib.SequenceMatcher(None, s1, s2)
    return matcher.ratio()

### поиск###
"""
lev_dict = {}

####поиск картинки###
for i in trash_dict:
    klev = simil(trash_dict[i],x)
    lev_dict[klev] = i
#print(lev_dict)
res = PIL.Image.open(lev_dict[max(lev_dict)])
res.show()

#print(lev_dict)
"""

'''
API_TOKEN = '1433598427:AAFMI1BDQw0DZ_YTvMAc--0A3IZgmWV8nLw'
path = "C:/Users/User/Desktop/ocrd/images/"
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(content_types=["text", "photo","sticker"])
def repeat_all_messages(message):
    lev_dict = {}

    ####поиск картинки###
    for i in trash_dict:
        klev = simil(trash_dict[i], message.text.lower())
        lev_dict[klev] = i
    # pic = lev_dict[max(lev_dict)]
    pic = open(path + lev_dict[max(lev_dict)], 'rb')
    bot.send_sticker(message.chat.id, pic)
    # bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)'''

