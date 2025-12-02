
import requests
import socket

# 1. 测试端口通不通
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
result = sock.connect_ex(('127.0.0.1', 8000))
if result == 0:
    print("✅ 端口 8000 是通的！")
else:
    print(f"❌ 端口 8000 无法连接，错误码: {result}")

# 2. 测试 HTTP 请求
try:
    print("正在尝试发送请求...")
    session = requests.Session()
    session.trust_env = False
    resp = session.get("http://127.0.0.1:8000/docs")
    print(f"✅ 请求成功！状态码: {resp.status_code}")
except Exception as e:
    print(f"❌ 请求失败: {e}")