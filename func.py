from bs4 import BeautifulSoup
import datetime
import colorama as color
import random
import time


def sleep(seconds):
    difference = random.randint(-round(seconds/2), round(seconds/2))
    time.sleep(seconds-difference)


def beautiful_print(text):
    length = 68
    if len(text) % 2:
        length += 1
    print()
    print(color.Fore.LIGHTMAGENTA_EX + ('{0: ^' + str(length) + '}').format(text))
    print(color.Fore.WHITE)


def get_time():
    return datetime.datetime.now().strftime("%H:%M:%S")


def login_coingecko(session, login, passwd, header):
    # отправляем запрос, чтобы получить Auth_token
    response = session.get('https://www.coingecko.com/account/sign_in?locale=en', headers=header)
    soup = BeautifulSoup(response.text, 'lxml')
    csrf_token = soup.find('input', {'name': 'authenticity_token'})['value']
    data = {
        'utf8': "✓",
        'authenticity_token': csrf_token,
        'user[redirect_to]': "",
        'user[email]': login,
        'user[password]': passwd,
        'user[remember_me]': {
            0: '0',
            1: '1'
        },
        'commit': "Log+in"
    }

    # отправляем запрос логина
    login_request = session.post(url="https://www.coingecko.com/account/sign_in?locale=en", data=data, headers=header)
    if login_request.ok:
        print(f'[{get_time()}] >> [{login}] >> successfully logged.', end=' ')
        return True
    else:
        print(f'[{get_time()}] >> GG.')
        return False


def get_balance_and_token(session, header):
    # отправляем запрос на баланс токенов
    balance_request = session.get('https://www.coingecko.com/account/candy?locale=en', headers=header)
    soup = BeautifulSoup(balance_request.text, 'lxml')

    balance = soup.find('div', {'data-target': 'points.balance'}).text
    print(f'balance: {balance} candies.', end=' ')

    try:
        csrf_token = soup.find('input', {'name': 'authenticity_token'})['value']
        return csrf_token
    except:
        return False



def collect_candies(csrf_token, session, header):
    # отправляю запрос на сбор конфет
    data = {
        'authenticity_token' : csrf_token
    }
    collect_request = session.post('https://www.coingecko.com/account/candy/daily_check_in?locale=en', headers=header,data=data)
    if collect_request.ok:
        print(f'successfully redeemed.', end=' ')
        # получаю новый баланс
        balance_request = session.get('https://www.coingecko.com/account/candy?locale=en', headers=header)
        soup = BeautifulSoup(balance_request.text, 'lxml')
        balance = soup.find('div', {'data-target': 'points.balance'}).text
        print(f'new balance: {balance} candies.')
    else:
        print(f'GG.')
