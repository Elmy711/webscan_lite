import requests, socket, re
from urllib.parse import urlparse
import urllib3
urllib3.disable_warnings()
from bs4 import BeautifulSoup

G = '\033[92m'; R = '\033[91m'; Y = '\033[93m'; Z = '\033[0m'; C = '\033[96m'

def clean_url(u):
    # Hapus semua karakter invisible + spasi
    u = u.strip()
    u = re.sub(r'[\u200e\u200f\u200b\ufeff\u202a-\u202e]', '', u)
    # Ambil yang bentuk domain doang
    u = re.sub(r'[^a-zA-Z0-9.-]', '', u)
    return 'https://' + u if u and not u.startswith('http') else u

def isp(ip):
    try:
        r = requests.get(f'http://ip-api.com/json/{ip}?fields=org', timeout=5)
        return r.json().get('org', 'Unknown')
    except:
        return 'Unknown'

def warna(c):
    return f'{G}{c}{Z}' if 200 <= c < 300 else f'{Y}{c}{Z}' if 300 <= c < 400 else f'{R}{c}{Z}'

urls_raw = open('list.txt', encoding='utf-8', errors='ignore').readlines()
urls = [clean_url(l) for l in urls_raw if l.strip() and clean_url(l)]

print(f'{C}Total baris: {len(urls_raw)} | URL valid: {len(urls)}{Z}\n')

f = open('hasil_scan_2026-06-05.txt', 'w', encoding='utf-8')
sukses = gagal = 0

for no, u in enumerate(urls, 1):
    print(f'[{no}] URL: {u}')
    f.write(f'[{no}] URL: {u}\n')
    
    try:
        d = urlparse(u).netloc
        ip = socket.gethostbyname(d)
        print(f'DNS: {d} -> {ip}')
        print(f'ISP: {isp(ip)}')
        f.write(f'DNS: {d} -> {ip}\nISP: {isp(ip)}\n')

        r = requests.get(u, timeout=20, verify=False)
        st = f'Status: {warna(r.status_code)}'
        sv = f'Server: {r.headers.get("Server", "-")}'
        cf = 'Protected' if 'cloudflare' in str(r.headers).lower() else 'Unprotected'
        cf = f'Cloudflare: {G+cf+Z}' if cf == 'Protected' else f'Cloudflare: {R+cf+Z}'
        t = BeautifulSoup(r.text[:200000], 'html.parser').title
        t = t.string.strip() if t else 'No title'

        print(st); print(sv); print(cf); print(f'Title: {t}\n')
        f.write(st + '\n' + sv + '\n' + cf + '\n' + f'Title: {t}\n\n')
        sukses += 1

    except Exception as e:
        print(f'Error: {R}{e}{Z}\n')
        f.write(f'Error: {e}\n\n')
        gagal += 1

    print('-'*50)
    f.write('-'*50 + '\n\n')

f.close()
print(f'\n{G}[SELESAI]{Z} hasil_scan_2026-06-05.txt')
print(f'{G}Sukses: {sukses}{Z} | {R}Gagal: {gagal}{Z}')
