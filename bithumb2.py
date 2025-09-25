import json
import re
from datetime import datetime, timedelta, timezone
from telethon import TelegramClient

def eventcoinname(file_path):
    exclude_keywords = ['BITHUMB', 'FAST', 'FINALITY', 'BTC', 'L2E']
    api_id ='21818073'
    api_hash ='699aa1c316419825940a834cbe3184c1'
    client = TelegramClient('session_file', api_id, api_hash)
    #자동인증
    async def main():
        await client.connect()
        if not await client.is_user_authorized():
            print("Telegram 인증이 필요합니다. 전화번호를 입력하세요.")
            phone_number = '+82***핸드폰번호***'
            await client.send_code_request(phone_number)
            code = input('Telegram에서 받은 인증 코드를 입력하세요: ')
            await client.sign_in(phone_number, code)

        # 한국 시간(KST) 기준 오늘 날짜 설정
        KST = timezone(timedelta(hours=9))
        today = datetime.now(KST).date()

        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)

        print("■ 당일(오늘) 이벤트 코인 목록 ■")
        coinname = set()

        for entry in data:
            text = entry.get('text', '')
            
            # [변경] 정규식 패턴 수정 및 코인 추출 방식 변경
            pattern = r'빗썸 ([A-Z0-9 ,]+)'
            
            
            matches = re.findall(pattern, text)
            coins = []
            for match in matches:
                for coin_part in match.split(','):
                    main_coin = coin_part.strip().split()[0]
                    coins.append(main_coin)
            #print(coins)

            #main_coin = coins[0]

            period_match = re.search(r'(\d{1,2})/(\d{1,2})일?\s*~\s*(\d{1,2})/(\d{1,2})일?', text)
            if period_match:
                start_month, start_day, end_month, end_day = map(int, period_match.groups())
                start_date = datetime(today.year, start_month, start_day).date()
                end_date = datetime(today.year, end_month, end_day).date()
                if end_date < start_date:
                    end_date = datetime(today.year + 1, end_month, end_day).date()
                if start_date <= today <= end_date:
                    for coin in coins:  # [변경] 모든 코인 추가
                        coinname.add(coin)
            else:
                date_candidates = re.findall(r'\b(\d{1,2})/(\d{1,2})(?:일)?\b', text)
                for month_str, day_str in date_candidates:
                    month, day = int(month_str), int(day_str)
                    event_date = datetime(today.year, month, day).date()
                    if event_date == today:
                        for coin in coins:  # [변경] 모든 코인 추가
                            coinname.add(coin)
            print(coins)


        try:
            if coinname:
                message_text = "■ 오늘의 이벤트 코인 ■\n" + "\n".join(sorted(coinname))
            else:
                message_text = "오늘 날짜와 일치하는 이벤트 코인이 없습니다."

            target_entity = await client.get_entity('https://t.me/eventbithumb_bot')
            await client.send_message(target_entity, message_text)
            print("Telegram 메시지가 전송되었습니다.")
        except Exception as e:
            print(f"Telegram 메시지 전송 중 오류 발생: {e}")

        return list(coinname)

    with client:
        return client.loop.run_until_complete(main())

if __name__ == "__main__":
    result = eventcoinname('filtered_messages.json')
    print(result)
