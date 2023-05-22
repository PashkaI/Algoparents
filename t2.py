import requests
from bs4 import BeautifulSoup, Comment


content = ''
userid = 2486518

session = requests.Session()
url = f"https://backoffice.algoritmika.org/payment/manage?PaymentSearch%5Bid%5D=&PaymentSearch%5Bcreated_at%5D=&PaymentSearch%5BpaymentCreatedAtStart%5D=&PaymentSearch%5BpaymentCreatedAtEnd%5D=&PaymentSearch%5Bcent_amount_received%5D=&PaymentSearch%5BstudentId%5D=&PaymentSearch%5Bcent_amount_paid%5D=&PaymentSearch%5Bfullname%5D=&PaymentSearch%5BinvoiceCredits%5D=&PaymentSearch%5Bupdated_at%5D=&PaymentSearch%5BpaymentUpdatedAtStart%5D=&PaymentSearch%5BpaymentUpdatedAtEnd%5D=&PaymentSearch%5Bstatus%5D=&PaymentSearch%5Breceipt_status%5D=&PaymentSearch%5Bpayment_type%5D=&PaymentSearch%5Bis_primary%5D=&PaymentSearch%5BactiveCourse%5D=&PaymentSearch%5BupdatedBy%5D=&PaymentSearch%5BcontractNumber%5D=&page=1&per-page=200&export=true&name=default&exportType=html"

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

# Создаем пустой список для сохранения найденных строк
matching_rows = []

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
        matching_rows.append([field1, field2, field3, field4, field5])

print(matching_rows)

