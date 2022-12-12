import requests
from bs4 import BeautifulSoup
import time
from time import sleep
import pandas as pd
import datetime
import os

# 221127_gitにコミット

# 今日の年月日を自動取得
today = datetime.date.today()
today = today.strftime('%Y%m%d')

# 乗降地リストを表示
print('【乗降地リスト】')
sleep(1)
city_lists = {'東  京':'13', '横  浜':'14', '名古屋':'23', '大  阪':'27', '神　戸':'28', '徳　島':'36', '松　山':'38'}
for k, v in city_lists.items():
    print(f'{k}：{v}')

# 出発地の選択
dep_check = 0
while dep_check == 0: 
    dep = input('出発地の該当番号を入力してください > ')
    if dep not in [v for k, v in city_lists.items() ]:
        print('-------（入力誤り）-------')
        sleep(1)
    else:
        depCity_name = [k for k, v in city_lists.items() if v == dep]
        depCity = '000' + dep
        dep_check += 1

print(f'{depCity} : {depCity_name[0]} を選択しました')

# 目的地の選択
dest_check = 0
while dest_check == 0: 
    dest = input('目的地の該当番号を入力してください > ')
    if dest not in [v for k, v in city_lists.items() ]:
        print('-------（入力誤り）-------')
        sleep(1)
    elif dest == dep:
        print('出発地と同じ番号が入力されています')
        sleep(1)
    else:
        destCity_name = [k for k, v in city_lists.items() if v == dest]
        destCity = '000' + dest
        dest_check += 1
        
print(f'{destCity} ： {destCity_name[0]} を選択しました')

# 出発年月日を入力
date_check = 0
while date_check == 0:
    dep_date = input('出発年月日を8桁で入力してください (例)2022年12月25日 → 20221225 > ')
    if len(dep_date) == 8:
        try:
            dep_Y = int(dep_date[0:4])
            dep_M = int(dep_date[4:6])
            dep_D = int(dep_date[6:8])
            date_check += 1
        except:
            print('半角8桁の数字を入力してください')
    else:
        print('8桁の数字を入力してください')
        sleep(1)

print(f'出発日：{dep_Y}年{dep_M}月{dep_D}日')

# 検索期間を入力
days_check = 0
while days_check == 0:
    many_days = input('何日先までを検索しますか？（最大30日まで） > ')
    try:
        many_days = int(many_days)
        if 0 <= many_days <= 30:
            days_check += 1
        else:
            print('「0」以上「30」以下の数字を入力してください')
            sleep(1)
    except:
        print('半角数字（1～30）を入力してください')
        sleep(1)

dt_now = datetime.date(dep_Y,dep_M,dep_D)
dt_search = dt_now + datetime.timedelta(days=many_days)
how_many_day = dt_search - dt_now
how_many_day = how_many_day.days + 1
search_year = dt_search.year
search_month = dt_search.month
search_day = dt_search.day

sleep(1)
print(f'検索期間：{dep_Y}年{dep_M}月{dep_D}日 ～ {search_year}年{search_month}月{search_day}日（{how_many_day}日間）')

# 入力条件をもとに検索を開始
print('検索を開始します',end=' ')
sleep(1)
for i in range(5):
    print('🚌',end=' ')
    sleep(1)

for i in range(0,how_many_day):
    dt_next = dt_now + datetime.timedelta(days=i)
    dt_next_year = str(dt_next.year)
    dt_next_month = str(dt_next.month)
    if len(dt_next_month) == 1:
        dt_next_month = '0' +  dt_next_month
    dt_next_day = str(dt_next.day)
    if len(dt_next_day) == 1:
        dt_next_day = '0' +  dt_next_day
    depYM = dt_next_year + dt_next_month
    depD = dt_next_day
    depYMD = depYM + depD

    url = (f'https://www.kosokubus.com/?page=bus_list&sMode=1&pageNum=0'
            f'&depCity=&destCity=&depPreflog=&destPreflog={destCity}&depT=&arrT=&depPref={depCity}'
            f'&depCity=&destPref={destCity}&destCity=&depYM={depYM}&depD={depD}&numMan=1&numWoman=0&DepFrom=noselected&DepTo=noselected&DestFrom=noselected&DestTo=noselected')    
    
    r = requests.get(url)

    soup = BeautifulSoup(r.text, 'html.parser')

    pageNum = soup.find('div', id='pagernum').text
    pageNum = int(pageNum[-2:]) # 検索するページ数を取得
    num = soup.find('span', class_='num').text # 検索件数を取得

    print()
    print(f'検索年月日：{dt_next_year}年{dt_next_month}月{dt_next_day}日')  
    print(f'検索路線：{depCity_name[0]} ➡ {destCity_name[0]}') 
    print(f'検索結果：{num}件  検索を開始します')
    
    d_list = []

    for i in range(0,pageNum):
        
        url = (f'https://www.kosokubus.com/?page=bus_list&sMode=1&pageNum={i}\&depCity=&destCity=&depPreflog=&destPreflog=&depT=&arrT=&depPref='
            f'{depCity}&depCity=&destPref={destCity}&destCity=&depYM={depYM}&depD={depD}&numMan=1&numWoman=0&DepFrom=noselected&DepTo=noselected&DestFrom=noselected&DestTo=noselected')
        r = requests.get(url)
        print(url)
        soup = BeautifulSoup(r.text, 'html.parser')

        sleep(1)

        contents = soup.find_all('div', class_='scheduleBox')

        for content in contents: 
            title = content.find('a').text
            name = content.find('div', class_='name')
            company = name.find('a').text
            daynight = content.find('p', class_='daynight').text
            stools = name.find_all('p')
            stools = stools[2].text.split('：')
            stools = stools[1]
            price = content.find('span', class_='tRed').text
            seats = content.find('table', class_='section')
            seats = seats.find_all('td')
            seats = int(seats[1].text)

            d = {
                '便名': title,
                '運行会社': company,
                '便コード': stools,
                '料金': price,
                '空席': seats,
                '時間帯':daynight
            }

            d_list.append(d)

        df = pd.DataFrame(d_list)
        df = df[['時間帯', '運行会社', '便コード', '料金', '空席', '便名']]

        filename = f'{today}_{depYMD}{depCity_name[0]}→{destCity_name[0]} 空席状況.csv'
        df.to_csv(filename,encoding='utf_8_sig')

print('処理が完了しました')


