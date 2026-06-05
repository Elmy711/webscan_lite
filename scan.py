import requests, socket
from urllib.parse import urlparse
import urllib3
urllib3.disable_warnings()
from bs4 import BeautifulSoup

G = '\033[92m'
R = '\033[91m'
Y = '\033[93m'
Z = '\033[0m'
C = '\033[96m'

def skema(u):
    u = u.strip()
    return u if u.startswith('http') else 'https://' + u

def isp(ip):
    try:
        r = requests.get(f'http://ip-api.com/json/{ip}?fields=org', timeout=5)
        return r.json().get('org', 'Unknown')
    except:
        return 'Unknown'

def warna(c):
    return f'{G}{c}{Z}' if 200 <= c < 300 else f'{Y}{c}{Z}' if 300 <= c < 400 else f'{R}{c}{Z}'

urls = [l.strip() for l in open('list.txt', encoding='utf-8') if l.strip()][:30]
print(f'{C}Total URL: {len(urls)}{Z}\n')

f = open('hasil_scan.txt', 'w', encoding='utf-8')
f.write(f'BATCH SCAN {len(urls)} URL\n')

for u in urls:
    u = skema(u)
    print(f'\nURL: {u}')        
    f.write(f'\nURL: {u}\n')   
    
    try:
        d = urlparse(u).netloc
        ip = socket.gethostbyname(d)
        s = f'DNS: {d} -> {ip}\nISP: {isp(ip)}'
        print(s)
        f.write(s + '\n')
        
        r = requests.get(u, timeout=15, verify=False)
        st = f'Status: {warna(r.status_code)}'
        sv = f'Server: {r.headers.get("Server", "-")}'
        cf = 'Protected' if 'cloudflare' in str(r.headers).lower() else 'Unprotected'
        cf = f'Cloudflare: {G+cf+Z}' if cf == 'Protected' else f'Cloudflare: {R+cf+Z}'
        t = BeautifulSoup(r.text[:200000], 'html.parser').title
        t = t.string.strip() if t else 'No title'
        
        out = f'{st}\n{sv}\n{cf}\nTitle: {t}\n\n'
        print(out)
        f.write(out)
    except Exception as e:
        e = f'Error: {R}{e}{Z}\n'
        print(e)
        f.write(e)
    f.write('-'*40 + '\n')

f.close()
print(f'\n{G}[SELESAI]{Z} hasil_scan.txt')
