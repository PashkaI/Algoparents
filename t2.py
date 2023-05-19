import requests
from bs4 import BeautifulSoup, Comment


content = ''
User = 2486518

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
    #print(content)
else:
    # Обработка ошибки
    print('Ошибка при выполнении запроса')

# Создаем объект BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# Находим все строки (tr) в таблице
rows = soup.find_all('tr')

# Проходим по каждой строке, начиная со второй (пропускаем заголовок)
for row in rows[1:]:
    # Извлекаем значения ячеек (td) из текущей строки
    cells = row.find_all('td')

    # Проверяем, совпадает ли номер в User с номером в текущей строке
    if User == int(cells[0].text):
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


# Выводим извлеченные данные

print("Имя:", name)
print("Прошло уроков в группе:", lessons_completed)
print("Старт группы:", start_date)
print("Тип группы:", group_type)
print("Статус ученика в группе:", student_status)
print("Посетил уроков:", lessons_attended)
print("Пропустил уроков:", lessons_missed)
print("Оплачено:", paid)
print("Оплачено уроков:", lessons_paid)
print("Баланс:", balance)