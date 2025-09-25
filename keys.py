import os
from dotenv import load_dotenv

load_dotenv()

class KeyManager:
    def __init__(self):
        self.accessKey = []
        self.secretKey = []

        i = 1
        while True:
            access = os.getenv(f"ACCESS_KEY_{i}")
            secret = os.getenv(f"SECRET_KEY_{i}")
            if access and secret:
                self.accessKey.append(access)
                self.secretKey.append(secret)
                i += 1
            else:
                break

    def indexkey(self, i):
        return self.accessKey[i], self.secretKey[i]

    def lenaccount(self):
        return len(self.accessKey)
