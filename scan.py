import requests
from bs4 import BeautifulSoup
import socket
import datetime
import ipapi
from urllib.parse import urlparse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import time

def tambah_skema(url):
    url = url.strip()
    if not url.startswith('http'):
        url = 'https://' + url
    return url

def scan_satu_url(url, f):
    def tulis(teks):
        print(teks)
        f.write(teks + '\n')

    url = tambah_skema(url)
    tulis(f"\n=== SCAN: {url} ===")
    tulis(f"Waktu: {datetime.datetime.now()}")

    try:
        domain = urlparse(url).netloc
        ip = socket.gethostbyname(domain)
        tulis(f"IP: {ip}")
        tulis(f"DNS: {domain} -> {ip}")  # DNS ditambahin

        data_ip = ipapi.location(ip=ip)
        tulis(f"ISP: {data_ip.get('org', 'Unknown')}")

        with requests.get(url, timeout=15, stream=True, verify=False) as r:
            tulis(f"Status: {r.status_code}")
            
            # [HEADER] dihapus, langsung server + cloudflare
            server = r.headers.get('Server', 'Not detected')
            tulis(f"Server: {server}")
            tulis(f"Cloudflare: {'Protected' if 'cloudflare' in str(r.headers).lower() else 'Unprotected'}")

            # Baca max 500KB biar hemat RAM
            content = b""
            for chunk in r.iter_content(chunk_size=8192):
                content += chunk
                if len(content) > 500000:
                    break

            soup = BeautifulSoup(content, 'html.parser')

            title = soup.title.string.strip() if soup.title else "No title"
            tulis(f"\n[HTML]\nTitle: {title}")

            tulis("[META TAG]")
            count = 0
            for meta in soup.find_all('meta'):
                if count >= 20: break
                name = meta.get('name') or meta.get('property')
                content = meta.get('content')
                if name and content:
                    tulis(f"{name}: {content[:150]}")
                    count += 1

    except Exception as e:
        tulis(f"Error: {e}")
    
    tulis("="*40)
    time.sleep(3) # delay 3 detik

def main():
    input_file = "list.txt"
    output_file = f"hasil_scan_{datetime.date.today()}.txt"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file_list:
            urls = [line.strip() for line in file_list if line.strip()]
    except FileNotFoundError:
        print(f"Error: File {input_file} nggak ketemu. Bikin dulu isinya URL.")
        return

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"=== BATCH SCAN {len(urls)} URL ===\n")
        f.write(f"Mulai: {datetime.datetime.now()}\n\n")
        
        for i, url in enumerate(urls, 1):
            print(f"\n[{i}/{len(urls)}] Scanning...")
            scan_satu_url(url, f)
    
    print(f"\n[SELESAI] Semua hasil ada di: {output_file}")

if __name__ == "__main__":
    main()
