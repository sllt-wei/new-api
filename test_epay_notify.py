#!/usr/bin/env python3
"""
测试易支付回调接口是否接受无签名的伪造请求
用法: python test_epay_notify.py http://localhost:3000 <trade_no>
"""
import sys
import requests

BASE_URL = sys.argv[1].rstrip("/") if len(sys.argv) > 1 else "http://localhost:3000"
TRADE_NO = sys.argv[2] if len(sys.argv) > 2 else "USR1NOtest123"

url = f"{BASE_URL}/api/user/epay/notify"

# 伪造回调参数，无签名
fake_params = {
    "pid": "1",
    "type": "alipay",
    "out_trade_no": TRADE_NO,
    "trade_no": "FAKE_TRADE_12345",
    "name": "TUC100",
    "money": "1.00",
    "trade_status": "TRADE_SUCCESS",
    # 故意不带 sign / sign_type
}

print(f"[*] 目标: {url}")
print(f"[*] 订单号: {TRADE_NO}")
print(f"[*] 发送伪造 POST 回调（无签名）...")

resp = requests.post(url, data=fake_params)
print(f"[*] HTTP {resp.status_code}: {resp.text!r}")

if resp.text == "success":
    print("[!] 危险: 服务器返回 success，可能存在漏洞！")
elif resp.text == "fail":
    print("[+] 正常: 服务器拒绝了无签名请求")
else:
    print(f"[?] 未知响应: {resp.text!r}")

# 也测试 GET 方式
print(f"\n[*] 发送伪造 GET 回调（无签名）...")
resp2 = requests.get(url, params=fake_params)
print(f"[*] HTTP {resp2.status_code}: {resp2.text!r}")

if resp2.text == "success":
    print("[!] 危险: GET 方式也返回 success！")
elif resp2.text == "fail":
    print("[+] 正常: GET 方式也被拒绝")
