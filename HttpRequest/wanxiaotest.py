import requests

url = 'http://ocsp.pki.goog/gts1c3/MFAwTjBMMEowSDAHBgUrDgMCGgQUxy55it3%2FYTSzuu1HQri7xsAkB2MEFIp0f6%2BFze6VzT2c0OJGFPNxNR0nAhEAxzbbw4ZNt74QUarMPFbBlQ%3D%3D'

headers = {
    'X-Apple-Request-UUID': '8DEA89AD-E3EC-4F1D-9A94-14709BA5A843',
    'Accept': '*/*',
    'User-Agent': 'com.apple.trustd/3.0',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
}

response = requests.get(url, headers=headers)

# 输出响应内容
print(response.status_code)  # HTTP状态码
print(response.text)  # 响应内容
print(response.content)  # 字节响应内容
