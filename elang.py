import requests, socket, re, csv
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
        r = requests.get(f'http://ip-api.com/json/{ip}?fields=org', timeout=3)
        return r.json().get('org', 'Unknown')
    except:
        return 'Unknown'

def detect_cms(html, headers):
    html = html.lower()
    h = str(headers).lower()
    if 'wp-content' in html or 'wordpress' in html: return 'WordPress'
    if 'wix' in html or 'wix.com' in h: return 'Wix'
    if 'shopify' in html or 'shopify' in h: return 'Shopify'
    if 'vercel' in h: return 'Vercel/NextJS'
    if 'x-powered-by: php' in h: return 'PHP'
    return '-'

def warna(c):
    return f'{G}{c}{Z}' if 200 <= c < 300 else f'{Y}{c}{Z}' if 300 <= c < 400 else f'{R}{c}{Z}'

def scan_one(no, u):
    result = {'no': no, 'url': u, 'dns': '-', 'ip': '-', 'isp': '-', 'status': '-',
              'server': '-', 'cloudflare': '-', 'cms': '-', 'title': '-', 'error': '-'}
    try:
        d = urlparse(u).netloc
        ip = socket.gethostbyname(d)
        result['dns'] = d; result['ip'] = ip; result['isp'] = isp(ip)

        headers = {'User-Agent':'Mozilla/5.0'}
        try:
            r = requests.get(u, timeout=8, verify=False, headers=headers)
        except:
            # Retry 1x fallback HTTP
            u = u.replace('https://', 'http://')
            r = requests.get(u, timeout=8, verify=False, headers=headers)
            result['url'] = u

        result['status'] = r.status_code
        result['server'] = r.headers.get("Server", "-")
        result['cloudflare'] = 'Protected' if 'cloudflare' in str(r.headers).lower() else 'Unprotected'
        result['cms'] = detect_cms(r.text[:100000], r.headers)
        t = BeautifulSoup(r.text[:100000], 'html.parser').title
        result['title'] = t.string.strip() if t and t.string else 'No title'
        return result, True
    except Exception as e:
        result['error'] = str(e)
        return result, False

urls_raw = open('list.txt', encoding='utf-8', errors='ignore').readlines()
urls = [clean_url(l) for l in urls_raw if clean_url(l)]

print(f'{C}Total URL: {len(urls)}{Z}\n{C}Scanning... timeout 8s + retry 1x{Z}\n')
start = time.time()

results = [None] * len(urls)
sukses = gagal = 0

with ThreadPoolExecutor(max_workers=20) as executor:
    futures = {executor.submit(scan_one, i+1, u): i for i, u in enumerate(urls)}
    for future in as_completed(futures):
        idx, res, ok = future.result()
        results[idx-1] = res
        if ok: sukses += 1
        else: gagal += 1

# Print ke terminal
for r in results:
    if r['error'] == '-':
        st = warna(r['status'])
        cf = f'{G}Protected{Z}' if r['cloudflare'] == 'Protected' else f'{R}Unprotected{Z}'
        print(f"[{r['no']}] {r['url']}\nDNS: {r['dns']} -> {r['ip']}\nISP: {r['isp']}\nStatus: {st}\nServer: {r['server']}\nCloudflare: {cf}\nCMS: {Y}{r['cms']}{Z}\nTitle: {r['title']}\n" + '-'*50)
    else:
        print(f"[{r['no']}] {r['url']}\nDNS: {r['dns']} -> {r['ip']}\nISP: {r['isp']}\nError: {R}{r['error']}{Z}\n" + '-'*50)

# Export TXT
f = open('hasil_scan_2026-06-05.txt', 'w', encoding='utf-8')
for r in results:
    f.write(f"[{r['no']}] {r['url']}\nDNS: {r['dns']} -> {r['ip']}\nISP: {r['isp']}\n")
    if r['error'] == '-':
        f.write(f"Status: {r['status']}\nServer: {r['server']}\nCloudflare: {r['cloudflare']}\nCMS: {r['cms']}\nTitle: {r['title']}\n\n" + '-'*50 + '\n\n')
    else:
        f.write(f"Error: {r['error']}\n\n" + '-'*50 + '\n\n')
f.close()

# Export CSV buat Excel
with open('hasil_scan_2026-06-05.csv', 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['no','url','dns','ip','isp','status','server','cloudflare','cms','title','error'])
    writer.writeheader()
    writer.writerows(results)

print(f'\n{G}[SELESAI]{Z} hasil_scan_2026-06-05.txt +.csv')
print(f'Waktu: {time.time()-start:.2f} detik')
print(f'{G}Sukses: {sukses}{Z} | {R}Gagal: {gagal}{Z}')
