import requests, socket
from urllib.parse import urlparse
import urllib3
urllib3.disable_warnings()
from bs4 import BeautifulSoup

G = '\033[92m'; R = '\033[91m'; Y = '\033[93m'; Z = '\033[0m'; C = '\033[96m'

def skema(u):
    u = u.strip().replace('\u200e', '').replace('\u200f', '') # hapus karakter aneh
    return u if u.startswith('http') else 'https://' + u

def isp(ip):
    try:
        r = requests.get(f'http://ip-api.com/json/{ip}?fields=org', timeout=5)
        return r.json().get('org', 'Unknown')
    except:
        return 'Unknown'

def warna(c):
    return f'{G}{c}{Z}' if 200 <= c < 300 else f'{Y}{c}{Z}' if 300 <= c < 400 else f'{R}{c}{Z}'

urls = [l.strip() for l in open('list.txt', encoding='utf-8') if l.strip()] # tanpa limit
print(f'{C}Total URL: {len(urls)}{Z}\n')

f = open('hasil_scan_2026-06-05.txt', 'w', encoding='utf-8')

for no, u in enumerate(urls, 1):
    u = skema(u)
    if u == 'https://':
        continue # skip baris kosong

    # Header rapi
    header = f'[{no}] URL: {u}'
    print(f'\n{header}')
    f.write(header + '\n')

    try:
        d = urlparse(u).netloc
        ip = socket.gethostbyname(d)
        print(f'DNS: {d} -> {ip}')
        print(f'ISP: {isp(ip)}')
        f.write(f'DNS: {d} -> {ip}\n')
        f.write(f'ISP: {isp(ip)}\n')

        r = requests.get(u, timeout=15, verify=False)
        st = f'Status: {warna(r.status_code)}'
        sv = f'Server: {r.headers.get("Server", "-")}'
        cf = 'Protected' if 'cloudflare' in str(r.headers).lower() else 'Unprotected'
        cf = f'Cloudflare: {G+cf+Z}' if cf == 'Protected' else f'Cloudflare: {R+cf+Z}'
        t = BeautifulSoup(r.text[:200000], 'html.parser').title
        t = t.string.strip() if t else 'No title'

        print(st)
        print(sv)
        print(cf)
        print(f'Title: {t}')

        f.write(st + '\n')
        f.write(sv + '\n')
        f.write(cf + '\n')
        f.write(f'Title: {t}\n')

    except Exception as e:
        err = f'Error: {R}{e}{Z}'
        print(err)
        f.write(err + '\n')

    garis = '-'*50
    print(garis)
    f.write(garis + '\n\n')

f.close()
print(f'\n{G}[SELESAI]{Z} hasil_scan_2026-06-05.txt')
