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
bill = ''

def GetContent():
    global content, bill
    # Создание сеанса
    session = requests.Session()
    url1 = f"https://backoffice.algoritmika.org/student?StudentSearch%5Bgroup_student_status%5D=0&StudentSearch%5Bcontent_type%5D%5B0%5D=course&StudentSearch%5Bcontent_type%5D%5B1%5D=intensive&StudentSearch%5BgroupType%5D%5B0%5D=masterclass&StudentSearch%5BgroupType%5D%5B1%5D=regular&StudentSearch%5BgroupType%5D%5B2%5D=intensive&StudentSearch%5BgroupType%5D%5B3%5D=individual&StudentSearch%5BisCourseInProgress%5D=1&presetType=active_v2&export=true&name=default&exportType=html"
    url2 = f"https://backoffice.algoritmika.org/payment/manage?PaymentSearch%5Bid%5D=&PaymentSearch%5Bcreated_at%5D=&PaymentSearch%5BpaymentCreatedAtStart%5D=&PaymentSearch%5BpaymentCreatedAtEnd%5D=&PaymentSearch%5Bcent_amount_received%5D=&PaymentSearch%5BstudentId%5D=&PaymentSearch%5Bcent_amount_paid%5D=&PaymentSearch%5Bfullname%5D=&PaymentSearch%5BinvoiceCredits%5D=&PaymentSearch%5Bupdated_at%5D=&PaymentSearch%5BpaymentUpdatedAtStart%5D=&PaymentSearch%5BpaymentUpdatedAtEnd%5D=&PaymentSearch%5Bstatus%5D=&PaymentSearch%5Breceipt_status%5D=&PaymentSearch%5Bpayment_type%5D=&PaymentSearch%5Bis_primary%5D=&PaymentSearch%5BactiveCourse%5D=&PaymentSearch%5BupdatedBy%5D=&PaymentSearch%5BcontractNumber%5D=&page=1&per-page=200&export=true&name=default&exportType=html"

    # Значение cookie
    cookie_value = 'SL_G_WPT_TO=en; SL_GWPT_Show_Hide_tmp=1; SL_wptGlobTipTmp=1; _gid=GA1.2.1042649071.1684313787; _ym_uid=1684313787290135952; _ym_d=1684313787; intercom-device-id-ufjpx6k3=1b691db9-8635-4458-8134-4639ff5cf647; _grid_page_size=d3ebbdf9ec9235bfc4ba59572a6d3dd403a563222be148e9c705e91612194e49a:2:{i:0;s:15:"_grid_page_size";i:1;s:3:"200";}; _grid_page_size_schedule=35d0980fa38e2255112d0c62698773cab8aa12a81c6735caf172064b5eb6ea47a:2:{i:0;s:24:"_grid_page_size_schedule";i:1;s:3:"200";}; _ym_isad=1; _ym_visorc=w; SERVERID=b440; userId=30450; createdTimestamp=1684491765; accessToken=e3e8e46e853131801497846ff6ff3f0437fcb1314d3fd67a9e0e8bc8519672c0; SERVERID=b530; _backendMainSessionId=c7ed2d7e4366e399f6ffacf63bc557d3; _ga_3QSGZBLTE3=GS1.1.1684490453.14.1.1684491769.0.0.0; _ga=GA1.2.1661591960.1684313787; _gat_gtag_UA_122842599_49=1; intercom-session-ufjpx6k3=eGQ1V0RLZVNGZnM3c3ZvRVJ6aysrYWFkbFd1ekhRaHpheGdSdnVMT1RSYWkyTTBIS3d3Z1J0d0NYTDl2aXZrQS0tNkM4MlVQaGpaSkl6TUhRdFVmalRhZz09--93e556a9a2e94a64baae806ef37b1b177231cf04'

    # Разделение значения cookie
    cookie_list = cookie_value.split('; ')

    # Установка каждого значения cookie
    for cookie in cookie_list:
        cookie_name, cookie_value = cookie.split('=', 1)
        session.cookies.set(cookie_name, cookie_value)

    # Выполнение запросов на сайт с использованием авторизационных cookie
    response = session.get(url1)
    response1 = session.get(url2)

    # Проверка успешного выполнения запроса
    if response.status_code == 200:
        # Обработка ответа
        content = response.text
        print(content)
    else:
        # Обработка ошибки
        print('Ошибка при выполнении запроса')

    # Проверка успешного выполнения запроса
    if response1.status_code == 200:
        # Обработка ответа
        bill = response1.text
        print(bill)
    else:
        # Обработка ошибки
        print('Ошибка при выполнении запроса')

GetContent()
# scheduler.add_job(GetContent, 'cron', hour=14, minute=31, second=10)
#
# scheduler.start()

# =================== Определяем пользователя и язык ======================
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

def getlanguage(nameid):
    conn = sqlite3.connect('userdata.sql')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE pass=?", (nameid,))
    existing_record = cur.fetchone()
    if existing_record:
        userlang = existing_record[-1]
    cur.close()
    conn.close()
    return userlang

# ============== Обработка запросов по командам Бота ========================
@dp.message_handler(commands=['start'])
async def main(message):
    name = message.from_user.first_name
    nameid = message.from_user.id
    conn = sqlite3.connect('userdata.sql')                      # utc INTEGER
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS users (id int auto_increment primary key, name varchar(50), '
                'pass varchar(50), utc integer, lang integer)')
    cur.execute("SELECT * FROM users WHERE name=? AND pass=?", (name, nameid))
    existing_record = cur.fetchone()
    if existing_record:
        await message.answer( "Welcome you again")
    else:
        cur.execute("INSERT INTO users (name, pass, utc, lang) VALUES (?, ?, ?, ?)", (name, nameid, 1, 1))
        conn.commit()
        #bot.send_message(message.chat.id, "Запись успешно добавлена.")   .from_user.first_name
    cur.close()
    conn.close()
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('🇬🇧 English', callback_data='Eng')
    btn2 = types.InlineKeyboardButton('🇵🇱 Polish', callback_data='Pol')
    markup.row(btn1, btn2)
    await message.answer(               f'  Hello, <b>{name}!</b> '
                                        f'\nWelcome to the Algo - Parents Bot'
                                        f'\nPlease enter the <b>student ID</b>'
                                        f'\nAnd choose your <b>language</b>'
                                        ,parse_mode='html', reply_markup=markup)

@dp.message_handler(commands=['get_users'])
async def allusers(message):
    conn = sqlite3.connect('userdata.sql')
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    info = ''
    for el in users: info += f'Name: {el[1]}, ID:{el[2]}, utc:{el[3]}, lang:{el[4]}\n'
    cur.execute("SELECT COUNT(*) FROM users")
    count = cur.fetchone()[0]
    cur.close()
    conn.close()
    await message.answer(f'{count}\n{info}')

@dp.message_handler(commands=['getuser'])
async def getuser(message, nameid=None):
    if nameid is None:
        nameid = message.from_user.id
    userid = getuserid(nameid)
    userlang = getlanguage(nameid)

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

    print("Запрос для :", name)
    if userlang == 1:
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

    if userlang == 2:
        await message.answer(
            f'<b><u>Podstawowe informacje o uczniu :</u></b>'
            f'\nImię i nazwisko -  {name}'
            f'\nLekcje zaliczone w grupie: -  {lessons_completed}'
            f'\nPoczątek grupy: -  {start_date}'
            #f'\nGroup type: -  {group_type}'
            #f'\nStudent status in the group: -  {student_status}'
            f'\nUczęszczane lekcje: -  {lessons_attended}'
            f'\nNieodebrane lekcje: -  {lessons_missed}'
            f'\nZapłacone: -  {paid}'
            f'\nPłatne za lekcje: -  {lessons_paid}'
            f'\nSaldo: -  {balance}'
            ,parse_mode='html')

@dp.message_handler(commands=['billinfo'])
async def billinf(message, nameid=None):
    if nameid is None:
        nameid = message.from_user.id
    userid = getuserid(nameid)
    userlang = getlanguage(nameid)

    # Создаем объект BeautifulSoup
    soup = BeautifulSoup(bill, 'html.parser')

    # Находим все строки (tr) в таблице
    rows = soup.find_all('tr')
    field1 = ''
    field2 = ''
    field3 = ''
    field4 = ''
    field5 = ''

    # Создаем пустой список для сохранения найденных строк
    matching_values = []

    # Проходим по каждой строке, начиная со второй (пропускаем заголовок)
    for row in rows[1:]:
        # Извлекаем значения ячеек (td) из текущей строки
        cells = row.find_all('td')

        # Проверяем, совпадает ли номер в User с номером в текущей строке
        if userid == int(cells[2].text):
            # Извлекаем нужные данные из ячеек
            field1 = cells[0].text
            field2 = cells[1].text
            field3 = cells[3].text
            field4 = cells[4].text
            field5 = int(cells[5].text)

            # Добавляем найденные значения в список
            matching_values.append([field1, field2, field3, field4, field5])

    print("Запрос для :", field4)
    if userlang == 1:
        # Создаем переменную для объединения сообщения
        output_message = '<b><u>Payment Information :</u></b>'

        # Выводим найденные значения
        for values in matching_values:
            field1, field2, field3, field4, field5 = values

            output_message += (
                f'\nPayment date -  {field1}'
                f'\nbilled for payment -  {field2}'
                f'\nReceived -  {field3}'
                # f'\nGroup type: -  {group_type}'
                # f'\nStudent status in the group: -  {student_status}'
                f'\nNumber of paid lessons -  {field5}'
                f'\n----------'
            )

        # Отправляем одно сообщение с объединенными значениями
        await message.answer(output_message, parse_mode='html')

    if userlang == 2:
        # Создаем переменную для объединения сообщения
        output_message = '<b><u>Informacje o płatnościach :</u></b>'

        # Выводим найденные значения
        for values in matching_values:
            field1, field2, field3, field4, field5 = values

            output_message += (
                f'\nTermin płatności -  {field1}'
                f'\nDo zapłaty -  {field2}'
                f'\nOtrzymany -  {field3}'
                # f'\nGroup type: -  {group_type}'
                # f'\nStudent status in the group: -  {student_status}'
                f'\nLiczba płatnych lekcji -  {field5}'
                f'\n----------'
            )

        # Отправляем одно сообщение с объединенными значениями
        await message.answer(output_message, parse_mode='html')

# ========================================================================================================
#                       Обработка  Запросов  Callback
# ========================================================================================================
@dp.callback_query_handler()
async def callback(call):

    if call.data == 'Pol':
        nameid = call.from_user.id
        conn = sqlite3.connect('userdata.sql')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE pass=?", (nameid,))
        existing_record = cur.fetchone()
        if existing_record:
            # Обновляем запись в базе данных
            cur.execute("UPDATE users SET lang = ? WHERE pass = ?", (2, nameid))
            conn.commit()
        cur.close()
        conn.close()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        btn1 = types.KeyboardButton('Informacje o studencie')
        btn2 = types.KeyboardButton('Informacje o płatnościach')
        markup.row(btn1, btn2)
        await bot.send_message(call.message.chat.id, f'Wybrałeś język polski', reply_markup=markup)

    elif call.data == 'Eng':
        nameid = call.from_user.id
        conn = sqlite3.connect('userdata.sql')
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE pass=?", (nameid,))
        existing_record = cur.fetchone()
        if existing_record:
            # Обновляем запись в базе данных
            cur.execute("UPDATE users SET lang = ? WHERE pass = ?", (1, nameid))
            conn.commit()
        cur.close()
        conn.close()
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
        btn1 = types.KeyboardButton('User Infirmation')
        btn2 = types.KeyboardButton('Bill Infirmation')
        markup.row(btn1, btn2)
        await bot.send_message(call.message.chat.id, f'You have chosen English', reply_markup=markup)


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

    elif userid == 'user infirmation' or userid == 'bill infirmation':
        if userid == 'user infirmation': await getuser(message, nameid)
        if userid == 'bill infirmation': await billinf(message, nameid)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    elif userid == 'informacje o studencie' or userid == 'informacje o płatnościach':
        if userid == 'informacje o studencie': await getuser(message, nameid)
        if userid == 'informacje o płatnościach': await billinf(message, nameid)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    else:
        # Ввод содержит другие символы, кроме цифр
        await bot.send_message(message.chat.id, f'Student ID was entered incorrectly. Enter only numbers.'
                            f'\n----------'                    
                            f'\nIdentyfikator ucznia został wprowadzony nieprawidłowo. Należy wprowadzić tylko cyfry')


# file_handler.close()
executor.start_polling(dp)