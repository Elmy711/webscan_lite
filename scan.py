import requests
from bs4 import BeautifulSoup
import socket
import datetime
from urllib.parse import urlparse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
CYAN = '\033[96m'

lock = threading.Lock()
scan_satu_url.counter = 0

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
            return {'org': data.get('org', 'Unknown'), 'country': data.get('country', 'Unknown')}
    except:
        pass
    return {'org': 'Unknown', 'country': 'Unknown'}

def print_progress(current, total, bar_length=30):
    progress = current / total
    filled = int(bar_length * progress)
    bar = '█' * filled + '░' * (bar_length - filled)
    with lock:
        sys.stdout.write(f'\r[{CYAN}{bar}{RESET}] {current}/{total} {progress*100:.1f}%')
        sys.stdout.flush()

def scan_satu_url(url, f, total):
    def tulis(teks):
        with lock:
            f.write(teks + '\n')

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
            status = r.status_code
            tulis(f"Status: {status}")
            
            server = r.headers.get('Server', 'Not detected')
            tulis(f"Server: {server}")
            tulis(f"Cloudflare: {'Protected' if 'cloudflare' in str(r.headers).lower() else 'Unprotected'}")

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
    
    with lock:
        scan_satu_url.counter += 1
        print_progress(scan_satu_url.counter, total)

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
    print(f"Thread: 10 URL barengan\n")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"=== BATCH SCAN {total} URL ===\n\n")
        
        try:
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(scan_satu_url, url, f, total) for url in urls]
                for future in as_completed(futures):
                    pass
        except KeyboardInterrupt:
            print(f"\n\n{RED}Scan dihentikan manual{RESET}")
            f.write("\nScan dihentikan manual\n")
    
    print(f"\n\n{GREEN}[SELESAI]{RESET} Hasil: {output_file}")

if __name__ == "__main__":
    main()    output_file = f"hasil_scan_{datetime.date.today()}.txt"
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file_list:
            urls = [line.strip() for line in file_list if line.strip()]
    except FileNotFoundError:
        print(f"Error: File {input_file} nggak ketemu. Bikin dulu isinya URL.")
        return

    total = len(urls)
    print(f"Total URL: {total}")
    print(f"Thread: 10 URL barengan\n")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"=== BATCH SCAN {total} URL ===\n\n")
        
        try:
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(scan_satu_url, url, f, total) for url in urls]
                for future in as_completed(futures):
                    pass
        except KeyboardInterrupt:
            print(f"\n\n{RED}Scan dihentikan manual{RESET}")
            f.write("\nScan dihentikan manual\n")
    
    print(f"\n\n{GREEN}[SELESAI]{RESET} Hasil: {output_file}")

if __name__ == "__main__":
    main()
scan_satu_url.counter = 0

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
    print(f"Thread: 10 URL barengan\n")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"=== BATCH SCAN {total} URL ===\n\n")
        
        try:
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(scan_satu_url, url, f, total) for url in urls]
                for future in as_completed(futures):
                    pass
        except KeyboardInterrupt:
            print(f"\n\n{RED}Scan dihentikan manual{RESET}")
            f.write("\nScan dihentikan manual\n")
    
    print(f"\n\n{GREEN}[SELESAI]{RESET} Hasil: {output_file}")

if __name__ == "__main__":
    main()        tulis(f"Error: {e}")
    
    tulis("="*40)
    
    # Update progress bar
    with lock:
        scan_satu_url.counter += 1
        print_progress(scan_satu_url.counter, total)

scan_satu_url.counter = 0

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
    print(f"Thread: 10 URL barengan\n")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"=== BATCH SCAN {total} URL ===\n\n")
        
        try:
            # Threading: 10 worker jalan bareng
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(scan_satu_url, url, f, i, total) for i, url in enumerate(urls, 1)]
                for future in as_completed(futures):
                    pass  # progress udah diupdate di dalam fungsi
        except KeyboardInterrupt:
            print(f"\n\n{RED}Scan dihentikan manual{RESET}")
            f.write("\nScan dihentikan manual\n")
    
    print(f"\n\n{GREEN}[SELESAI]{RESET} Hasil: {output_file}")

if __name__ == "__main__":
    main()    total = len(urls)
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
