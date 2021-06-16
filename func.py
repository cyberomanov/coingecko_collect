from bs4 import BeautifulSoup
import datetime
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
    print(('{0: ^' + str(length) + '}').format(text))
    print()



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
    response = session.get('https://www.coingecko.com/account/candy?locale=en', headers=header)
    soup = BeautifulSoup(response.text, 'lxml')
    balance = soup.find('div', {'data-target': 'points.balance'}).text
    print(f'balance: {balance} candies.', end=' ')

    return parse_token(response)



def parse_token(response):
    try:
        soup = BeautifulSoup(response.text, 'lxml')
        token = soup.find('input', {'name': 'authenticity_token'})['value']
        return token
    except:
        return False



def get_reward(link, session, header):

    # получаем токен
    response = session.get(link, headers=header)
    token = parse_token(response)

    # если токен получен
    if token != False:

        # получем действие
        soup = BeautifulSoup(response.text, 'lxml')
        action = soup.findAll('form', {'class': 'button_to'})[1]['action']

        # получаем название предмета
        title = soup.find('div', {'class': 'text-lg-2xl text-xl pl-1 font-weight-bold'})
        data = {
            'authenticity_token': token,
        }

        # отправляем запрос покупки реварда
        buy_response = session.post(url="https://www.coingecko.com/"+action, data=data,
                                     headers=header)
        if buy_response.ok:
            print(f'successfully bought.', end=' ')
            return title.text
        else:
            print(f'GG.')
            return False
    else:
        print(f'GG.')
        return False



def get_promo(title, session, header):
    response = session.get("https://www.coingecko.com/account/my-rewards?locale=en", headers=header)
    soup = BeautifulSoup(response.text, 'lxml')

    # получаем список полученных наград
    rewards = soup.findAll('div', {'class': 'ml-3 mr-md-3 ml-lg-4 mb-3 mr-lg-1 voucher-card-section'})
    for reward in rewards:

        # ищем ссылку на награду по названию покупки
        if title in reward.contents[3].text:

            # достаём промо
            href = reward.contents[1].contents[1]['href']
            response = session.get("https://www.coingecko.com/" + href, headers=header)
            soup = BeautifulSoup(response.text, 'lxml')
            promo = soup.find('input', {'class': 'form-control font-semibold'})['value']
            print(f'promo: {promo}.')
            break



def collect_candies(csrf_token, session, header):
    # отправляю запрос на сбор конфет
    data = {
        'authenticity_token' : csrf_token
    }
    collect_request = session.post('https://www.coingecko.com/account/candy/daily_check_in?locale=en', headers=header, data=data)
    if collect_request.ok:
        print(f'successfully redeemed.', end=' ')
        # получаю новый баланс
        balance_request = session.get('https://www.coingecko.com/account/candy?locale=en', headers=header)
        soup = BeautifulSoup(balance_request.text, 'lxml')
        balance = soup.find('div', {'data-target': 'points.balance'}).text
        print(f'new balance: {balance} candies.')
    else:
        print(f'GG.')
