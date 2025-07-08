import time
import hmac
import hashlib

def create_signature(query_string, secret):
    return hmac.new(secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256).hexdigest()

def log_response(data):
    with open("logs.txt", "a", encoding="utf-8") as f:
        f.write(f"{time.ctime()} -> {data}\n\n")
