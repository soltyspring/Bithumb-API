
from telethon import TelegramClient
import json
from datetime import datetime, timedelta, timezone

def bit1():
    # API ID와 API Hash 설정
    api_id ='21818073'
    api_hash ='699aa1c316419825940a834cbe3184c1'
    #자동인증
    # Telethon 클라이언트 생성 (세션 파일 사용)
    client = TelegramClient('session_file', api_id, api_hash)

    # 메시지를 JSON 파일로 저장하는 함수
    async def save_messages_to_json(channel, include_keywords, exclude_keywords):
        one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
        messages = []

        async for message in client.iter_messages(channel):
            msg_date_aware = message.date.astimezone(timezone.utc)
            if msg_date_aware < one_week_ago:
                break

            text = message.text or ''
            if any(keyword in text for keyword in include_keywords) and not any(keyword in text for keyword in exclude_keywords):

                messages.append({
                    'id': message.id,
                    'text': text,
                    'date': str(msg_date_aware)
                })

        with open('filtered_messages.json', 'w', encoding='utf-8') as f:
            json.dump(messages, f, ensure_ascii=False, indent=4)
        print("조건을 만족하는 메시지가 filtered_messages.json 파일에 저장되었습니다.")

    # 메인 함수
    async def main():
        channel = await client.get_entity('https://t.me/SUS_secretnote')
        include_keywords = ['1/N']
        exclude_keywords = ['전에 했던']

        print("조건을 만족하며, 7일 이내 작성된 메시지 출력:")
        async for message in client.iter_messages(channel):
            msg_date_aware = message.date.astimezone(timezone.utc)
            one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)

            if msg_date_aware < one_week_ago:
                break

            text = message.text or ''
            if any(k in text for k in include_keywords) and not any(k in text for k in exclude_keywords):
                print(f"ID: {message.id}, Date: {msg_date_aware}, Text: {text}")

        await save_messages_to_json(channel, include_keywords, exclude_keywords)
        return 200

    # 클라이언트 실행
    with client:
        result = client.loop.run_until_complete(main())
    return result

if __name__ == "__main__":
    bit1()

