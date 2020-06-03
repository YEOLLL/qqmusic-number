import base64
import random
import time
import sys
import requests
from selenium import webdriver

HOST = 'https://y.qq.com'
GET_COOKIE_API = 'https://api.qq.jsososo.com/user/cookie'
SET_COOKIE_API = 'https://api.qq.jsososo.com/user/setCookie'
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
TIMEOUT = 20
def encode(key: str, string: str) -> str:
    """
    Encrypt password with secret key.
    :param key: str, secret key.
    :param string: str, password.
    :return: str, encrypted password.
    """
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr(ord(string[i]) + ord(key_c) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    encoded_string = encoded_string.encode('latin')
    return base64.urlsafe_b64encode(encoded_string).rstrip(b'=').decode()


def decode(key: str, string: str) -> str:
    """
    Decrypt password with secret key.
    :param key: str, secret key.
    :param string: str, encrypted password.
    :return: str, password.
    """
    string = base64.urlsafe_b64decode(string.encode() + b'===')
    string = string.decode('latin')
    encoded_chars = []
    for i in range(len(string)):
        key_c = key[i % len(key)]
        encoded_c = chr((ord(string[i]) - ord(key_c) + 256) % 256)
        encoded_chars.append(encoded_c)
    encoded_string = ''.join(encoded_chars)
    return encoded_string


def login_for_cookies(qqnumber: str, password: str) -> dict:
    """
    Login to y.qq.com via selenium.
    :return: dict, user cookies.
    """
    # Use Google Chrome driver.
    driver = webdriver.Chrome()
    driver.get(HOST)
    # Open login page.
    driver.find_element_by_link_text('登录').click()
    # Switch to the top window.
    driver.switch_to.window(driver.window_handles[-1])
    # Switch to the login iframe step by step.
    while 1:
        try:
            driver.switch_to.frame('frame_tips')  # iframe frame_tips.
            break
        except Exception:
            time.sleep(0.5)

    while 1:
        try:
            driver.switch_to.frame('ptlogin_iframe')  # iframe ptlogin_iframe.
            break
        except Exception:
            time.sleep(0.5)

    time.sleep(3)
    # Switch to input popup, fill username and password, then login.
    driver.find_element_by_id('switcher_plogin').click()
    driver.find_element_by_name('u').send_keys(qqnumber)
    driver.find_element_by_name('p').send_keys(password)
    driver.find_element_by_id('login_button').click()

    # Check if login is successful by checking value of qm_keyst in cookies.
    time_cost = 0
    while 1:
        cookies_list = driver.get_cookies()
        cookies_dict = {item.get('name'): item.get('value') for item in cookies_list}
        if cookies_dict.get('qm_keyst'):
            break
        if time_cost > TIMEOUT:
            raise TimeoutError('Login timeout.')
        time.sleep(0.5)
        time_cost += 0.5
    driver.quit()

    return cookies_dict