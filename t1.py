from aiogram import Bot, Dispatcher, executor, types
import datetime
import time
import requests
import sqlite3
from bs4 import BeautifulSoup, Comment
from apscheduler.schedulers.background import BackgroundScheduler
import subprocess
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

bot = Bot('5838878828:AAFVtAnF6732ccUcjG8DnFWddZKTMvM74Fo')
dp = Dispatcher(bot)

scheduler = BackgroundScheduler()
content = ''

def GetContent():
    global content
    # Создание сеанса
    session = requests.Session()
    url = f"https://backoffice.algoritmika.org/student?StudentSearch%5Bgroup_student_status%5D=0&StudentSearch%5Bcontent_type%5D%5B0%5D=course&StudentSearch%5Bcontent_type%5D%5B1%5D=intensive&StudentSearch%5BgroupType%5D%5B0%5D=masterclass&StudentSearch%5BgroupType%5D%5B1%5D=regular&StudentSearch%5BgroupType%5D%5B2%5D=intensive&StudentSearch%5BgroupType%5D%5B3%5D=individual&StudentSearch%5BisCourseInProgress%5D=1&presetType=active_v2&export=true&name=default&exportType=html"

    # Значение cookie
    cookie_value = 'SL_G_WPT_TO=en; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; _gid=GA1.2.1042649071.1684313787; _ym_uid=1684313787290135952; _ym_d=1684313787; intercom-device-id-ufjpx6k3=1b691db9-8635-4458-8134-4639ff5cf647; _grid_page_size=d3ebbdf9ec9235bfc4ba59572a6d3dd403a563222be148e9c705e91612194e49a:2:{i:0;s:15:"_grid_page_size";i:1;s:3:"200";}; _grid_page_size_schedule=35d0980fa38e2255112d0c62698773cab8aa12a81c6735caf172064b5eb6ea47a:2:{i:0;s:24:"_grid_page_size_schedule";i:1;s:3:"200";}; _ym_isad=1; _ym_visorc=w; SERVERID=b440; userId=30450; createdTimestamp=1684491765; accessToken=e3e8e46e853131801497846ff6ff3f0437fcb1314d3fd67a9e0e8bc8519672c0; SERVERID=b530; _backendMainSessionId=c7ed2d7e4366e399f6ffacf63bc557d3; _ga_3QSGZBLTE3=GS1.1.1684490453.14.1.1684491769.0.0.0; _ga=GA1.2.1661591960.1684313787; _gat_gtag_UA_122842599_49=1; intercom-session-ufjpx6k3=eGQ1V0RLZVNGZnM3c3ZvRVJ6aysrYWFkbFd1ekhRaHpheGdSdnVMT1RSYWkyTTBIS3d3Z1J0d0NYTDl2aXZrQS0tNkM4MlVQaGpaSkl6TUhRdFVmalRhZz09--93e556a9a2e94a64baae806ef37b1b177231cf04'

    # Разделение значения cookie
    cookie_list = cookie_value.split('; ')

    # Установка каждого значения cookie
    for cookie in cookie_list:
        cookie_name, cookie_value = cookie.split('=', 1)
        session.cookies.set(cookie_name, cookie_value)

    # Выполнение запросов на сайт с использованием авторизационных cookie
    response = session.get(url)

    # Проверка успешного выполнения запроса
    if response.status_code == 200:
        # Обработка ответа
        content = response.text
        print(content)
    else:
        # Обработка ошибки
        print('Ошибка при выполнении запроса')

GetContent()
# scheduler.add_job(GetContent, 'cron', hour=14, minute=31, second=10)
#
# scheduler.start()

# =================== Определяем время пользователя ======================
def getuserid(nameid):
    conn = sqlite3.connect('userdata.sql')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE pass=?", (nameid,))
    existing_record = cur.fetchone()
    if existing_record:
        userid = existing_record[-2]
    cur.close()
    conn.close()
    return userid

# ============== Обработка запросов по командам Бота ========================
@dp.message_handler(commands=['start'])
async def main(message):
    name = message.from_user.first_name
    nameid = message.from_user.id
    conn = sqlite3.connect('userdata.sql')                      # utc INTEGER
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), '
                'pass varchar(50), utc integer, alarm varchar(8))')
    cur.execute("SELECT * FROM users WHERE name=? AND pass=?", (name, nameid))
    existing_record = cur.fetchone()
    if existing_record:
        await message.answer( "I welcome you again")
    else:
        cur.execute("INSERT INTO users (name, pass, utc) VALUES (?, ?, ?)", (name, nameid, 1))
        conn.commit()
        #bot.send_message(message.chat.id, "Запись успешно добавлена.")   .from_user.first_name
    cur.close()
    conn.close()
    await message.answer(               f'  Hello, <b>{name}!</b> '
                                        f'\nWelcome to the Algo - Parents Bot'
                                        f'\nPlease enter the student ID'
                                        ,parse_mode='html')

@dp.message_handler(commands=['get_users'])
async def allusers(message):
    conn = sqlite3.connect('userdata.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    info = ''
    for el in users: info += f'Name: {el[1]}, ID:{el[2]}, utc:{el[3]}\n'
    cur.execute("SELECT COUNT(*) FROM users")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    await message.answer(f'{count}\n{info}')

@dp.message_handler(commands=['get'])
async def maintest(message, nameid=None):
    if nameid is None:
        nameid = message.from_user.id
    userid = getuserid(nameid)

    # Создаем объект BeautifulSoup
    soup = BeautifulSoup(content, 'html.parser')

    # Находим все строки (tr) в таблице
    rows = soup.find_all('tr')
    name = ''
    lessons_completed = ''
    start_date = ''
    group_type = ''
    student_status = ''
    lessons_attended = ''
    lessons_missed = ''
    paid = ''
    lessons_paid = ''
    balance = ''

    # Проходим по каждой строке, начиная со второй (пропускаем заголовок)
    for row in rows[1:]:
        # Извлекаем значения ячеек (td) из текущей строки
        cells = row.find_all('td')

        # Проверяем, совпадает ли номер в User с номером в текущей строке
        if userid == int(cells[0].text):
            # Извлекаем нужные данные из ячеек
            name = cells[1].text
            lessons_completed = int(cells[2].text)
            start_date = cells[3].text
            group_type = cells[4].text
            student_status = cells[5].text
            lessons_attended = int(cells[6].text)
            lessons_missed = int(cells[7].text)
            paid = int(cells[8].text)
            lessons_paid = int(cells[9].text)
            balance = int(cells[10].text)
            break  # Прерываем цикл, так как данные для User найдены

    print("Имя:", name)
    await message.answer(
        f'<b><u>Basic information about the student :</u></b>'
        f'\nName -  {name}'
        f'\nLessons passed in group: -  {lessons_completed}'
        f'\nGroup start: -  {start_date}'
        #f'\nGroup type: -  {group_type}'
        #f'\nStudent status in the group: -  {student_status}'
        f'\nAttended lessons: -  {lessons_attended}'
        f'\nMissed lessons: -  {lessons_missed}'
        f'\nPaid: -  {paid}'
        f'\nPaid for lessons: -  {lessons_paid}'
        f'\nBalance: -  {balance}'
        ,parse_mode='html')


#============================ Запись запроса в базу по номеру =========================
@dp.message_handler(content_types=['text'])
async def fordate(message):
    nameid = message.from_user.id
    userid = message.text.strip().lower()
    if userid.isdigit():
        conn = sqlite3.connect('userdata.sql')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE pass=?", (nameid,))
        existing_record = cur.fetchone()
        if existing_record:
            # Обновляем запись в базе данных
            cur.execute("UPDATE users SET utc = ? WHERE pass = ?", (userid, nameid))
            conn.commit()
            # Получаем обновленную запись из базы данных
            cur.execute("SELECT utc FROM users WHERE pass=?", (nameid,))
        cur.close()
        conn.close()
        await message.answer(f'Great, you entered : \n{userid}', parse_mode='html')
    else:
        # Ввод содержит другие символы, кроме цифр
        await bot.send_message(message.chat.id, 'Student ID was entered incorrectly. Enter only numbers.')


# file_handler.close()
executor.start_polling(dp)