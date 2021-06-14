import fake_useragent
import requests
from colorama import init
import time

from data import accounts
from func import *



init(convert=True)
iteration = 0
seconds_to_sleep = 10

while True:
    iteration += 1
    beautiful_print(f'[   ///   ITERATION #{iteration}   ///   ]')

    # создаём копию аккаунтов и перемешиваем её
    accounts_list = accounts
    random.shuffle(accounts_list)

    for i in range(len(accounts_list)):

        # получаем логин, пароль, прокси для логина
        login = accounts_list[i]["coin_mail"]
        passwd = accounts_list[i]["coin_password"]
        proxy = { 'https': 'http://' + accounts_list[i]["proxy"],
                  'http': 'http://' + accounts_list[i]["proxy"]
                }

        # генерируем фейковый юзер-агент
        user = fake_useragent.UserAgent().random
        header = {
            'user-agent': user
        }

        # создаём сессию и подключаем прокси
        session = requests.Session()
        session.proxies = proxy

        # выполняем логин
        if login_coingecko(session=session, login=login, passwd=passwd, header=header):
            sleep(seconds_to_sleep)
            result_of = get_balance_and_token(session=session, header=header)
            if result_of != False:
                sleep(seconds_to_sleep)
                collect_candies(result_of, session=session, header=header)
            else:
                print(f'we have to sleep, cant redeem candies.')
        else:
            print(f'something went wrong.')

        # пауза между аккаунтами от 3 до 6 минут
        sleep(seconds_to_sleep*25)

    # итерация прошла, спим пару часов
    sleep(50000)



