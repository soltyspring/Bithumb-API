# Bithumb Event Workflow

**메시지에서 이벤트 대상 코인을 추출해 주문 처리로 연결하는 Python 개인 프로젝트입니다.**

> Exchange integration connecting structured inputs, authenticated API calls, and account-level order workflows.

## 처리 흐름

`bithumb1.py`가 Telegram 메시지를 수집하고 `bithumb2.py`가 이벤트 코인을 추출합니다. `main.py`는 계정별로 대상 코인의 가격과 잔고를 확인하고 API 주문을 요청합니다.

```text
Telegram 메시지 → 조건 필터 → 대상 코인
                             ↓
                가격 조회 → 매수 요청 → 잔고 조회 → 매도 요청
```

| 파일 | 역할 |
| --- | --- |
| `main.py` | 계정별 처리 순서와 주문 실행 |
| `api.py` | 인증된 주문 요청 |
| `account.py` | 코인 잔고 조회 |
| `price.py` | 시세 조회 |
| `keys.py` | 계정 키를 제공하는 `KeyManager` |

## 환경 구성

Python 가상환경을 사용하세요. 현재 저장소에는 고정된 의존성 파일이 없습니다. 아래는 소스의 주요 패키지 기준 설치 목록입니다.

```bash
python -m venv .venv
# 가상환경 활성화 후
python -m pip install requests PyJWT schedule python-dotenv telethon
```

실행 전 `KeyManager`가 사용하는 계정 설정을 확인하고 본인 키를 로컬에서만 관리해야 합니다. 설정 방식은 각 모듈을 확인하세요. Telegram 세션·대상 채널과 메시지 필터도 필요합니다.

## 실행과 주의할 동작

진입점은 `python main.py`입니다. **실행 즉시 실제 주문 흐름이 시작될 수 있으며 dry-run 모드는 구현되어 있지 않습니다.** 현재 코드에는 5,200원 시장가 매수 요청 후 조회된 잔고를 시장가 매도하는 흐름이 있습니다. 매도 수량은 이번 매수량만이 아니라 조회된 해당 코인 잔고일 수 있습니다.

주문 성공·체결 확인, 예외 처리, 금액과 계정별 한도를 검토한 뒤 사용해야 합니다. `main.py`는 import 시에도 최상위 코드가 실행되므로 동작 확인을 위해 무심코 import하지 마세요.

## 개발 경험

외부 API 인증, 입력 데이터 정리, 계정별 반복 처리와 주문·잔고 조회 순서를 연결한 자동화 구현입니다. 개인 스크립트 형태이며 범용 거래 플랫폼이나 수익 전략으로 소개하지 않습니다.
