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
        f.write(teks + '\n')  # cuma tulis ke file, terminal bersih

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
            tulis(f"Cloudflare: {'Protected' if 'cloudflare' in str(r.headers).lower() else 'Unprotected'}")  # <- udah bener

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
    time.sleep(2)

def main():
    input_file = "list.txt"
    output_file = f"hasil_scan_{datetime.date.today()}.txt"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file_list:
            urls = [line.strip() for line in file_list if line.strip()]
    except FileNotFoundError:
        print(f"Error: File {input_file} nggak ketemu. Bikin dulu isinya URL.")
        return

    total = len(urls)
    print(f"Total URL: {total}")
    print("Tekan Ctrl+C buat stop\n")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"=== BATCH SCAN {total} URL ===\n\n")
        
        try:
            for i, url in enumerate(urls, 1):
                print_progress(i, total)
                scan_satu_url(url, f)
        except KeyboardInterrupt:
            print("\n\nScan dihentikan manual")
            f.write("\nScan dihentikan manual\n")
    
    print(f"\n\n[SELESAI] Hasil: {output_file}")

if __name__ == "__main__":
    main()
