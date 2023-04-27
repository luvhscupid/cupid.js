import requests
from bs4 import BeautifulSoup
import re
import concurrent.futures

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

def extract_ip_address(text):
    """
    Extracts valid IPv4 addresses from text using regex pattern
    """
    pattern = r'\b(?:\d{1,3}\.){3}\d{1,3}\b'
    return re.findall(pattern, text)

def get_proxies(url):
    """
    Gets proxies from a given URL
    """
    proxies = []
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.get_text()
        ip_addresses = extract_ip_address(text)
        proxies.extend(ip_addresses)
    return proxies

# Create a ThreadPoolExecutor for concurrent processing
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for url in urls:
        futures.append(executor.submit(get_proxies, url))
    
    # Aggregate the results from each future
    all_proxies = []
    for future in concurrent.futures.as_completed(futures):
        proxies = future.result()
        all_proxies.extend(proxies)

# Write proxies to file
with open('/var/cache/motd/bigboy/proxies.txt', 'w') as f:
    for proxy in all_proxies:
        f.write(proxy + '\n')
