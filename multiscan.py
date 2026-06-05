import requests, socket, re
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import urllib3
urllib3.disable_warnings()
from bs4 import BeautifulSoup
import time

G = '\033[92m'; R = '\033[91m'; Y = '\033[93m'; Z = '\033[0m'; C = '\033[96m'

def clean_url(u):
    u = u.strip()
    u = re.sub(r'[\u200e\u200f\u200b\ufeff\u202a-\u202e]', '', u)
    if not u: return ''
    if not u.startswith('http'):
        u = 'https://' + u
    return u

def isp(ip):
    try:
        r = requests.get(f'http://ip-api.com/json/{ip}?fields=org', timeout=5)
        return r.json().get('org', 'Unknown')
    except:
        return 'Unknown'

def warna(c):
    return f'{G}{c}{Z}' if 200 <= c < 300 else f'{Y}{c}{Z}' if 300 <= c < 400 else f'{R}{c}{Z}'

def scan_one(no, u):
    result = f'[{no}] URL: {u}\n'
    try:
        d = urlparse(u).netloc
        ip = socket.gethostbyname(d)
        result += f'DNS: {d} -> {ip}\nISP: {isp(ip)}\n'

        headers = {'User-Agent':'Mozilla/5.0'}
        try:
            r = requests.get(u, timeout=15, verify=False, headers=headers)
        except:
            # Auto fallback ke HTTP kalo HTTPS gagal
            u_http = u.replace('https://', 'http://')
            r = requests.get(u_http, timeout=15, verify=False, headers=headers)
            result += f'Fallback: {Y}HTTP{u_http[4:]}{Z}\n'

        st = f'Status: {warna(r.status_code)}'
        sv = f'Server: {r.headers.get("Server", "-")}'
        cf = 'Protected' if 'cloudflare' in str(r.headers).lower() else 'Unprotected'
        cf = f'Cloudflare: {G+cf+Z}' if cf == 'Protected' else f'Cloudflare: {R+cf+Z}'
        t = BeautifulSoup(r.text[:200000], 'html.parser').title
        t = t.string.strip() if t and t.string else 'No title'

        result += st + '\n' + sv + '\n' + cf + '\n' + f'Title: {t}\n'
        return no, result, True
    except Exception as e:
        result += f'Error: {R}{e}{Z}\n'
        return no, result, False

urls_raw = open('list.txt', encoding='utf-8', errors='ignore').readlines()
urls = [clean_url(l) for l in urls_raw if clean_url(l)]

print(f'{C}Total URL: {len(urls)}{Z}\n')
start = time.time()

f = open('hasil_scan_2026-06-05.txt', 'w', encoding='utf-8')
sukses = gagal = 0
results = [None] * len(urls)

print(f'{C}Scanning... tunggu bentar{Z}\n')

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(scan_one, i+1, u): i for i, u in enumerate(urls)}
    for future in as_completed(futures):
        idx, res, ok = future.result()
        results[idx-1] = res
        if ok: sukses += 1
        else: gagal += 1

# Baru print urut setelah semua selesai
for res in results:
    print(res + '-'*50)
    f.write(res + '-'*50 + '\n\n')

f.close()
print(f'\n{G}[SELESAI]{Z} hasil_scan_2026-06-05.txt')
print(f'Waktu: {time.time()-start:.2f} detik')
print(f'{G}Sukses: {sukses}{Z} | {R}Gagal: {gagal}{Z}')
