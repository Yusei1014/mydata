
#必要ライブラリをインポートする
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import requests
import pandas as pd
import streamlit as st
import time
from selenium.webdriver.support.select import Select


#ブラウザをヘッドレスモードで起動
options = webdriver.ChromeOptions()
options.add_argument("--headless")
browser = webdriver.Chrome(ChromeDriverManager().install(),options=options)

#Yahoo!ニュースにアクセス
url = "https://news.yahoo.co.jp/categories/business"

#暗号通貨価格テーブル作成
url = "https://www.coindeskjapan.com/price/bitcoin/"
res = requests.get(url)
soup = BeautifulSoup(res.text,"html.parser")


coin_ls =  ["bitcoin","ethereum","xrp","usd-coin","stellar-lumens"]
coin_data_ls = [["価格","24時間変動率","24時間変動値"]]
def get_crypt_data(coin_name):


    url = "https://www.coindeskjapan.com/price/" + str(coin_name)
    res = requests.get(url)
    soup = BeautifulSoup(res.text,"html.parser")

    
    price = soup.select_one("body > main > article > header > div > div > div.o-marketPriceChart > div.o-marketPriceChartBodyArea > div:nth-child(1) > div.o-marketPriceChartInfo > div").text.replace("価格","").replace("円","")
    rate_24 = soup.select_one("body > main > article > header > div > div > div.o-marketPriceChart > div.o-marketPriceChartBodyArea > div:nth-child(1) > div.o-marketPriceChartInfo > div:nth-child(2)").text.replace("\n","").replace(" ","").replace("24時間変動率","")
    amount_24 = soup.select_one("body > main > article > header > div > div > div.o-marketPriceChart > div.o-marketPriceChartBodyArea > div:nth-child(1) > div.o-marketPriceChartInfo > div:nth-child(4)").text.replace("\n","").replace(" ","").replace("24時間変動値","")

    coin_data_ls.append([price,rate_24,amount_24])
    
    return 


def table_create():    
    for coin_name in coin_ls:
        get_crypt_data(coin_name)

    df = pd.DataFrame(data = coin_data_ls[1:],index = coin_ls ,columns=coin_data_ls[0])
    return df

#求人情報取得
 
def get_kyujin_data(order):
    url = "https://www.lancers.jp/work/search" 
    #ブラウザをヘッドレスモードで起動
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    browser = webdriver.Chrome(ChromeDriverManager().install(),options=options)

    #Lancersの求人検索画面にアクセス
    browser.get(url)
    time.sleep(1)

    #検索ボックスに入力したいワードを入力する。
    search_word = "Python スクレイピング"
    #検索ボックスに文字を入力する
    browser.find_element_by_id("Keyword").send_keys(search_word)
    #検索ボタンを押す
    search_btn = browser.find_element_by_id("Search").click() 
    time.sleep(1)

    selectbox = Select(browser.find_element_by_css_selector("body > div.l-wrapper > div.l-base.l-base--gray.p-search.p-search-job > main > section > section > div.c-paper.p-search__contents.l-search-section-content.clearfix > div.p-search__right > div.p-search__tools > div > div.c-search-bar__sub > div > label > select"))
    selectbox.select_by_visible_text(order)
    time.sleep(1)

    kyujin_price_ls = []
    kyujin_name_ls = []
    kyujin_url_ls = []
    kyujin_data_ls = []

    kyujin_ls = browser.find_elements_by_css_selector("body > div.l-wrapper > div.l-base.l-base--gray.p-search.p-search-job > main > section > section > div.c-paper.p-search__contents.l-search-section-content.clearfix > div.p-search__right > div.c-media-list.c-media-list--forClient > div")

    for kyujin in kyujin_ls:
        kyujin_name = kyujin.find_element_by_css_selector("div.c-media__content > div.c-media__content__right > a > span").text
        #print(kyujin_name)
        kyujin_name_ls.append(kyujin_name)
        kyujin_url = kyujin.find_element_by_css_selector("div.c-media__content > div.c-media__content__right > a").get_attribute("href")
        #print(kyujin_url)
        kyujin_url_ls.append(kyujin_url)
        kyujin_price = kyujin.find_element_by_css_selector("div.c-media__content > div.c-media__content__right > div > div > span.c-media__job-price").text
        #print(kyujin_price)
        kyujin_price_ls.append(kyujin_price)
        kyujin_data_ls.append([kyujin_name,kyujin_url,kyujin_price])

    df_kyujin_osusume = pd.DataFrame(kyujin_data_ls,columns=["募集名","求人URL","単価"])

    return df_kyujin_osusume.head()

    
crypt_tb = table_create()
lancers_osusume_tb = get_kyujin_data("おすすめ順")
lancers_new_tb = get_kyujin_data("新着順")

st.title("ぺぺの情報一覧部屋")
st.write("### 暗号通貨価格情報" , crypt_tb)
st.write("### ランサーズ求人情報おすすめ順" , lancers_osusume_tb)
st.write("### ランサーズ求人情報新着順" , lancers_new_tb)

