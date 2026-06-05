import requests
from bs4 import BeautifulSoup
import socket
import datetime
from urllib.parse import urlparse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time
import sys

def tambah_skema(url):
    url = url.strip()
    if not url.startswith('http'):
        url = 'https://' + url
    return url

def get_ip_info(ip):
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,org,country"
        r = requests.get(url, timeout=5)
        data = r.json()
        if data['status'] == 'success':
            return {
                'org': data.get('org', 'Unknown'),
                'country': data.get('country', 'Unknown')
            }
    except:
        pass
    return {'org': 'Unknown', 'country': 'Unknown'}

def print_progress(current, total, bar_length=30):
    progress = current / total
    filled = int(bar_length * progress)
    bar = '█' * filled + '░' * (bar_length - filled)
    sys.stdout.write(f'\r[{bar}] {current}/{total} {progress*100:.1f}%')
    sys.stdout.flush()

def scan_satu_url(url, f):
    def tulis(teks):
        f.write(teks + '\n')  # hapus print biar terminal bersih

    url = tambah_skema(url)
    tulis(f"\n=== SCAN: {url} ===")

    try:
        domain = urlparse(url).netloc
        ip = socket.gethostbyname(domain)
        tulis(f"IP: {ip}")
        tulis(f"DNS: {domain} -> {ip}")

        data_ip = get_ip_info(ip)
        tulis(f"ISP: {data_ip.get('org', 'Unknown')}")
        tulis(f"Country: {data_ip.get('country', 'Unknown')}")

        with requests.get(url, timeout=15, stream=True, verify=False) as r:
            tulis(f"Status: {r.status_code}")
            
            server = r.headers.get('Server', 'Not detected')
            tulis(f"Server: {server}")
            tulis(f"Cloudflare: {'Protected' if 'cloudflare' in str(r.headers).lower() else 'Unif __name__ == "__main__":
    main()
if __name__ == "__main__":
    main()
