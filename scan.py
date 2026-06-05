import requests, socket
from urllib.parse import urlparse
import urllib3
urllib3.disable_warnings()
from bs4 import BeautifulSoup

G = '\033[92m'; R = '\033[91m'; Y = '\033[93m'; Z = '\033[0m'; C = '\033[96m'

def skema(u):
    u = u.strip().replace('\u200e', '').replace('\u200f', '').replace('\u200b', '').replace('\ufeff', '')
    return u if u.startswith('http') else 'https://' + u

def isp(ip):
    try:
        r = requests.get(f'http://ip-api.com/json/{ip}?fields=org', timeout=5)
        return r.json().get('org', 'Unknown')
    except:
        return 'Unknown'

def warna(c):
    return f'{G}{c}{Z}' if 200 <= c < 300 else f'{Y}{c}{Z}' if 300 <= c < 400 else f'{R}{c}{Z}'

urls_raw = open('list.txt', encoding='utf-8', errors='ignore').readlines()
urls = [l.strip() for l in urls_raw if l.strip()]
print(f'{C}Total baris di file: {len(urls_raw)} | URL valid: {len(urls)}{Z}\n')

f = open('hasil_scan_2026-06-05.txt', 'w', encoding='utf-8')
sukses = 0
gagal = 0

for no, u in enumerate(urls, 1):
    u = skema(u)
    if u == 'https://':
        print(f'[{no}] SKIP: Baris kosong/karakter aneh')
        continue

    header = f'[{no}] URL: {u}'
    print(f'\n{header}')
    f.write(header + '\n')

    try: # <-- try/except ini bungkus 1 URL doang
        d = urlparse(u).netloc
        ip = socket.gethostbyname(d)
        print(f'DNS: {d} -> {ip}')
        print(f'ISP: {isp(ip)}')
        f.write(f'DNS: {d} -> {ip}\nISP: {isp(ip)}\n')

        r = requests.get(u, timeout=20, verify=False) # timeout dinaikin
        st = f'Status: {warna(r.status_code)}'
        sv = f'Server: {r.headers.get("Server", "-")}'
        cf = 'Protected' if 'cloudflare' in str(r.headers).lower() else 'Unprotected'
        cf = f'Cloudflare: {G+cf+Z}' if cf == 'Protected' else f'Cloudflare: {R+cf+Z}'
        t = BeautifulSoup(r.text[:200000], 'html.parser').title
        t = t.string.strip() if t else 'No title'

        print(st); print(sv); print(cf); print(f'Title: {t}')
        f.write(st + '\n' + sv + '\n' + cf + '\n' + f'Title: {t}\n')
        sukses += 1

    except Exception as e:
        err = f'Error: {R}{e}{Z}'
        print(err)
        f.write(err + '\n')
        gagal += 1

    garis = '-'*50
    print(garis)
    f.write(garis + '\n\n')

f.close()
print(f'\n{G}[SELESAI]{Z} hasil_scan_2026-06-05.txt')
print(f'{G}Sukses: {sukses}{Z} | {R}Gagal: {gagal}{Z}')
