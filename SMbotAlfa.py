
import logging
import telebot
import psycopg2
from psycopg2 import OperationalError
from config import simil


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
    "pict_base", "postgres", "logocentrism1", "127.0.0.1", "5432"
)


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        print(f"The error '{e}' occurred")

select_pictures = "SELECT * FROM picture"
pictures = execute_read_query(connection, select_pictures)

#print(type(pictures))

pict_dict = {}
for rows in pictures:
    pict_dict[rows[1]] = rows[2]
#print(pict_dict)

API_TOKEN = '1433598427:AAFMI1BDQw0DZ_YTvMAc--0A3IZgmWV8nLw'
path = "C:/Users/User/Desktop/ocrd/images/"
bot = telebot.TeleBot(API_TOKEN)



@bot.message_handler(content_types=["text", "photo","sticker"])
def repeat_all_messages(message):
    lev_dict = {}

    ####поиск картинки###
    for i in pict_dict:
        klev = simil(pict_dict[i], message.text.lower())
        lev_dict[klev] = i
    # pic = lev_dict[max(lev_dict)]
    pic = open(path + lev_dict[max(lev_dict)], 'rb')
    bot.send_sticker(message.chat.id, pic)
    # bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling(none_stop=True)