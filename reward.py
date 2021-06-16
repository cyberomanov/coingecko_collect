import fake_useragent
import requests

from data import accounts
from func import *



link = 'https://www.coingecko.com/account/rewards/how-to-bitcoin-book?locale=en'
seconds_to_sleep = 5

# создаём копию аккаунтов и перемешиваем её
accounts_list = accounts
random.shuffle(accounts_list)

for i in range(len(accounts_list)):

    # получаем логин, пароль, прокси для логина
    login = accounts_list[i]["coin_mail"]
    passwd = accounts_list[i]["coin_password"]
    proxy = {'https': 'http://' + accounts_list[i]["proxy"],
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
    try:

        # выполняем логин
        if login_coingecko(session=session, login=login, passwd=passwd, header=header):
            sleep(seconds_to_sleep)

            # получаем баланс
            get_balance_and_token(session=session, header=header)
            sleep(seconds_to_sleep)

            # покупаем предмет
            title_result = get_reward(link=link, session=session, header=header)
            if title_result != False:
                # получаем купленный предмет: ссылка или код
                get_promo(title=title_result, session=session, header=header)


        else:
            print(f'something went wrong with [{login}].')

        # пауза между аккаунтами от 3 до 10 минут
    except:
        print(f'something went wrong with [{login}].')

print(f'we got all of rewards.')





