import time
import os
import integ_auto as ia
from integ_auto import *

import pyperclip
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys

# NAVER SHOPPING APIs

# -------------------
# naver shopping apis
# -------------------

# Avoid Naver's Robot detection


def type_for_login(elem: WebElement, text: str):
    pyperclip.copy(text)
    elem.send_keys(Keys.CONTROL, 'v')


def get_purchasable_products(auto: Automatic, text: str):

    auto.go(f"https://brand.naver.com/samlip/search?q={text}")

    res = []
    es = auto.get_elements(
        By.XPATH, '//div/div/div[2]/div/div[2]/div/ul/li')
    for e in es:
        soldout = e.find_elements(By.XPATH, './/div[@class="_3tqnFuPpOs"]')
        title = e.find_element(By.XPATH, './/a/div/div/strong').text
        if not soldout and title.find(text) >= 0:
            res.append(e)
    return res


def login(auto: Automatic, id, pw):
    login_btn = auto.get_clickable(
        By.XPATH, '//*[@id="gnb_login_button"]', timeout=10)
    if not login_btn:
        print("Failed to find login button.")
        return False
    auto.click(login_btn)

    id_input = auto.get_clickable(By.ID, 'id')
    if not id_input:
        print("Failed to find id input.")
        return False
    type_for_login(id_input, id)

    pw_input = auto.get_clickable(By.ID, 'pw')
    if not pw_input:
        print("Failed to find pw input.")
        return False
    type_for_login(pw_input, pw)

    confirm_btn = auto.get_clickable(By.ID, 'log.login')
    if not confirm_btn:
        print("Failed to find pw input.")
        return False
    auto.click(confirm_btn)

    return True

# Precondition
# - detail page view


def buy_item_in_detail_page(auto: Automatic):
    # <a href="#" class="_2-uvQuRWK5"><span class="blind">구매하기</span></a>
    # //*[@id="content"]/div/div[2]/div[2]/fieldset/div[8]/div[1]/div/a
    buy_btn = auto.get_clickable(
        By.XPATH, '//*[@id="content"]/div/div[2]/div[2]/fieldset/div[8]/div[1]/div/a')
    if not buy_btn:
        print("Failed to find buy button.")
        return False
    auto.click(buy_btn)

    # 결제수단 선택
    credit_card_btn = auto.get_clickable(
        By.XPATH, '//*[@id="chargePointScrollArea"]/div[1]/ul[1]/li[3]/div[1]/span[1]')
    if not credit_card_btn:
        print("Failed to choose credit card.")
        return False
    auto.click(credit_card_btn)

    # 결재하기 버튼
    # //*[@id="orderForm"]/div/div[7]/button
    pay_btn = auto.get_clickable(
        By.XPATH, '//*[@id="orderForm"]/div/div[7]/button')
    if not pay_btn:
        print("Failed to find 결제하기 버튼.")
        return False
    auto.click(pay_btn)

    return True


# naver pay
def naver_payment(auto: Automatic, pw: str):
    if not auto.activate("네이버페이 - 프로필 1 - Microsoft​ Edge"):
        print(f"Failed to activate windows.")
        return False

    for num in pw:
        dir = os.path.dirname(os.path.abspath(__file__))
        num_btn = auto.get_element(f"{dir}/res/{num}.png")
        if not num_btn:
            return False
        auto.click(num_btn)
        time.sleep(1)

    close_btn = auto.get_element(
        By.XPATH, '//*[@id="order"]/div[5]/div/div[2]/div/button[2]')
    if not close_btn:
        print("Failed to find close button")
        return False
    auto.click(close_btn)

    return True


def go_home(auto: Automatic):
    auto.go("https://shopping.naver.com/home/p/index.naver")
