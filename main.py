import schedule
import time
from api import send_data_to_api
from price import nameprice
import api
import account
from account import balance
import bithumb2
from bithumb2 import eventcoinname
import bithumb1
from bithumb1 import bit1
from keys import KeyManager
keys = KeyManager()
time.sleep(1)

print("크롤링 실행")
Result = bithumb1.bit1()
while(1):
    if(Result == 200):
        print("크롤링 정상작동")
        break
name = eventcoinname('filtered_messages.json')

#강제 지정시 코인이름
#name = ["USDT"]

lenkey = keys.lenaccount()
for i in range(lenkey):
    accessKey, secretKey = keys.indexkey(i)
    accessKey = str(accessKey)
    secretKey = str(secretKey)

    
    print(name)
    for i in range(len(name)):
        inname = name[i]
        inname=str(inname)
        #inname="USDT"
        #price 파일 호출
        print(name[i])
        price = nameprice(name[i]) #name의 가격
        print(price)

        data_to_send=[]
        # 전송할 데이터 정의 (딕셔너리 형태)
        #bid ask
        #limit,price 시장가매수 ,market 시장가 매도
        
        send_data_to_api(dict(market=f"KRW-{inname}", side="bid", price=5200, ord_type="price"),accessKey,secretKey) 
        time.sleep(1)

        #account 파일 호출
        target_currency = balance(inname,accessKey,secretKey) #name의 잔액
        print(target_currency)
        send_data_to_api(dict(market=f"KRW-{inname}", side="ask", volume=target_currency, ord_type="market"),accessKey,secretKey)

