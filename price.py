import requests
import json

def nameprice(name):
    
    url = f"https://api.bithumb.com/v1/ticker?markets=KRW-{name}"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)
    
    data = json.loads(response.text)

    first_entry = data[0]
    trade_price = first_entry["trade_price"]
    return trade_price


if __name__ == "__main__":
    # 이 예제에서는 기본 'filtered_messages.json' 사용
    result = nameprice("USDT")
    print(result)