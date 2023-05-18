import requests
from bs4 import BeautifulSoup


def today():

    for p in range(1, 32):
        print('----------------------------------------------------------------')
        print(p)
        url = f"https://tibetastromed.ru/docom.php?tdat=03/{p}/2023&tipv=0&type=old&lang=ru"
        soup = BeautifulSoup(requests.get(url).text, 'html.parser')
        main = soup.findAll('p')[1].text

        if ".Поездка" in main: main = main.replace('.Поездка', ' Поездка')
        if ".Последствия поездки:" in main: main = main.replace('.Последствия поездки:', ' Последствия поездки:')
        if ".Последствия" in main: main = main.replace('.Последствия', ' Последствия')

        start = main.find("Последствия поездки:")
        end = main.find(".Местонахождение")
        item1 = main[start:end]

        start1 = main.find("Поездка")
        end1 = main.find("Последствия стрижки")
        item2 = main[start1:end1]

        start2 = main.find("Поездка")
        end2 = main.find("Последствия мытья")
        item3 = main[start2:end2]

        start3 = main.find("Поездка")
        end3 = main.find(".Местонахождение")
        item4 = main[start3:end3]

        start4 = main.find("Последствия поездки:")
        end4 = main.find("Последствия стрижки")
        item5 = main[start4:end4]

        start5 = main.find("Последствия поездки:")
        end5 = main.find("Последствия мытья")
        item6 = main[start5:end5]

        # ===============  Поездка ======================
        if "Последствия поездки:" in item1 and "мытья" not in item1 and "стрижки" not in item1:
            print(item1)
            print('1 Код успешно выполнился')
        elif "Поездка" in item2 and "мытья" not in item2 and "стрижки" not in item2:
            print(item2)
            print('2 Код успешно выполнился')
        elif "Поездка" in item3 and "мытья" not in item3 and "стрижки" not in item3:
            print(item3)
            print('3 Код успешно выполнился')
        elif "Поездка" in item4 and "мытья" not in item4 and "стрижки" not in item4:
            print(item4)
            print('4 Код успешно выполнился')
        elif "Последствия поездки:" in item5 and "мытья" not in item5 and "стрижки" not in item5:
            print(item5)
            print('5 Код успешно выполнился')
        elif "Последствия поездки:" in item6 and "мытья" not in item6 and "стрижки" not in item6:
            print(item6)
            print('6 Код успешно выполнился')

        #print(item4)
        # print('1 Код успешно выполнился')



today()
