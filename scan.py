import requests
from bs4 import BeautifulSoup
import socket
import datetime
from urllib.parse import urlparse
import urllib3
urllib3.disable_warnings()
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

GREEN = '\033[92m'
RED = '\033[91m'
CYAN = '\033[96m'
RESET = '\033[0m'

lock = threading.Lock()
counter = 0

def scan(url, f, total):
    global counter
    url = 'https://' + url.strip().replace('https://','').replace('http://','')
    f.write(f"\n=== SCAN: {url} ===\n")
    try:
        domain = urlparse(url).netloc
        ip = socket.gethostbyname(domain)
        f.write(f"IP: {ip}\n")
        r = requests.get(url, timeout=15, verify=False)
        f.write(f"Status: {r.status_code}\n")
        f.write(f"Server: {r.headers.get('Server','Unknown')}\n")
        soup = BeautifulSoup(r.text[:500000], 'html.parser')
        f.write(f"Title: {soup.title.string if soup.title else 'No title'}\n")
    except Exception as e:
        f.write(f"Error: {e}\n")
    f.write("="*40 + "\n")
    counter += 1
    sys.stdout.write(f'\r[{CYAN}{"█"*int(30*counter/total)}{RESET}] {counter}/{total}')
    sys.stdout.flush()

def main():
    urls = [x.strip() for x in open("list.txt") if x.strip()]
    total = len(urls)
    print(f"Total URL: {total}\nThread: 10\n")
    with open(f"hasil_scan_{datetime.date.today()}.txt", 'w') as f:
        with ThreadPoolExecutor(max_workers=10) as ex:
            list(ex.map(lambda u: scan(u, f, total), urls))
    print(f"\n\n{GREEN}[SELESAI]{RESET} hasil_scan_{datetime.date.today()}.txt")

if __name__ == "__main__":
    main
