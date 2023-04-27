import re
import requests
from bs4 import BeautifulSoup

urls = [
    'https://api.proxyscrape.com/v2/?request=getproxies&protocol=http&timeout=10000&country=all&ssl=all&anonymity=anonymous',
    'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt',
    'https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/https.txt',
    'https://raw.githubusercontent.com/monosans/proxy-list/main/proxies_anonymous/http.txt',
    'https://raw.githubusercontent.com/mertguvencli/http-proxy-list/main/proxy-list/data.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt',
    'https://raw.githubusercontent.com/jetkai/proxy-list/main/online-proxies/txt/proxies-https.txt'
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
