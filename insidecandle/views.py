from django.shortcuts import render
from django.http import HttpResponse
from fyers_api import fyersModel
from fyers_api import accessToken
from selenium.webdriver.common.by import By
import pyotp
from selenium import webdriver
import time



def generate_auth_code():
    client_id = 'C3HL2IWT0X-100'
    secret_key = 'PHA683XHJN'
    redirect_uri = 'https://www.google.com/'
    username = 'XN09067'
    pin1 = '1'
    pin2 = '7'
    pin3 = '2'
    pin4 = '7'

    session = accessToken.SessionModel(
        client_id=client_id,
        secret_key=secret_key,
        redirect_uri=redirect_uri,
        response_type='code',
        grant_type='authorization_code'
    )

    response = session.generate_authcode()
    driver = webdriver.Chrome()
    driver.get(response)
    driver.find_element(By.XPATH, '//*[@id="login_client_id"]').click()
    driver.find_element(By.XPATH, '//*[@id="fy_client_id"]').send_keys(username)
    driver.find_element(By.XPATH, '//*[@id="clientIdSubmit"]').click()
    time.sleep(7)
    p = pyotp.TOTP('QOWYDCCB6LP7GOM7QYYFVML7SPNTJZ5N').now()
    print(p)
    driver.find_element(By.XPATH, '//*[@id="first"]').send_keys(p[0])
    driver.find_element(By.XPATH, '//*[@id="second"]').send_keys(p[1])
    driver.find_element(By.XPATH, '//*[@id="third"]').send_keys(p[2])
    driver.find_element(By.XPATH, '//*[@id="fourth"]').send_keys(p[3])
    driver.find_element(By.XPATH, '//*[@id="fifth"]').send_keys(p[4])
    driver.find_element(By.XPATH, '//*[@id="sixth"]').send_keys(p[5])
    driver.find_element(By.XPATH, '//*[@id="confirmOtpSubmit"]').click()
    time.sleep(6)

    driver.find_element(By.ID, 'verify-pin-page').find_element(By.ID, 'first').send_keys(pin1)
    driver.find_element(By.ID, 'verify-pin-page').find_element(By.ID, 'second').send_keys(pin2)
    driver.find_element(By.ID, 'verify-pin-page').find_element(By.ID, 'third').send_keys(pin3)
    driver.find_element(By.ID, 'verify-pin-page').find_element(By.ID, 'fourth').send_keys(pin4)
    driver.find_element(By.XPATH, '//*[@id="verifyPinSubmit"]').click()

    time.sleep(4)

    newurl = driver.current_url
    auth_code = newurl[newurl.index('auth_code=')+10:newurl.index('&state')]
    driver.quit()

    return auth_code

def index(request):
    if request.method == 'POST':
        auth_code = generate_auth_code()
        session = accessToken.SessionModel(
            client_id='C3HL2IWT0X-100',
            secret_key='PHA683XHJN',
            redirect_uri='https://www.google.com/',
            response_type='code',
            grant_type='authorization_code'
        )
        session.set_token(auth_code)
        response = session.generate_token()
        access_token = response['access_token']

        with open('access.txt', 'w') as f:
            f.write(access_token)

        print(access_token)

    return render(request, 'index.html')
