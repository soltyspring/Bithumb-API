# Python 3
# pip3 installl pyJwt
import jwt
import uuid
import time
import requests
import json

  # keys.py에서 key 함수 가져오기


# key 함수 호출 및 튜플 언패킹

def balance(target_currency,accessKey,secretKey):
    
    # Set API parameters

    
    apiUrl = 'https://api.bithumb.com'

    # Generate access token
    payload = {
        'access_key': accessKey,
        'nonce': str(uuid.uuid4()),
        'timestamp': round(time.time() * 1000)
    }
    jwt_token = jwt.encode(payload, secretKey)
    authorization_token = 'Bearer {}'.format(jwt_token)
    headers = {
    'Authorization': authorization_token
    }

    def get_balance(data, target_currency):
        for item in data:
            if item['currency'] == target_currency:
                return item['balance']
        return None

    try:
        # Call API
        response = requests.get(apiUrl + '/v1/accounts', headers=headers)
        data = response.json()
        # handle to success or fail
        target_currency

        # balance 값 추출
        balance = get_balance(data, target_currency)


        return balance

    except Exception as err:
        # handle exception
        print(err)

if __name__ == "__main__":
    a = 'BTC'
    name = list()  # 빈 리스트 생성
    name.append(a)  # 'USDT'를 리스트에 추가 -> name = ['USDT']
    result = balance(name[0])  # 리스트의 첫 번째 요소 ('USDT')를 balance 함수에 전달
    print(result)


