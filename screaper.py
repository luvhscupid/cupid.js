import re
import requests
from bs4 import BeautifulSoup

urls = [
    'https://ciapak-proxy.cf/api/paid/?key=980321830129381029&type=http',
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=anonymous',
    'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt',
    'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt',
    'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt',
    'https://api.proxyscrape.com/?request=displayproxies&proxytype=http&timeout=9000&country=all&anonymity=all&ssl=all',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://www.proxy-list.download/api/v1/get?type=http',
    'https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt',
    'https://spys.me/proxy.txt',
    'https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt',
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all',
    'https://www.proxy-list.download/api/v1/get?type=http&anon=elite',
    'https://www.proxy-list.download/api/v1/get?type=http&anon=anonymous',
    'https://www.proxy-list.download/api/v1/get?type=http&anon=transparent'
]

proxies = []

for url in urls:
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        proxy_list = re.split('[ :/]', text)
        for i in range(len(proxy_list)):
            if re.match(r'^\d{1,3}(\.\d{1,3}){3}$', proxy_list[i]):
                proxies.append(proxy_list[i])

# Write proxies to file
with open('/var/cache/motd/bigboy/proxies.txt', 'w') as f:
    for proxy in proxies:
        f.write(proxy + '\n')
