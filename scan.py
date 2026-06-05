import requests
from bs4 import BeautifulSoup
import socket
from urllib.parse import urlparse
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
CYAN = '\033[96m'

lock = threading.Lock()

def tambah_skema(url):
    url = url.strip()
    if not url.startswith('http'):
        url = 'https://' + url
    return url

def get_isp(ip):
    try:
        url = f"http://ip-api.com/json/{ip}?fields=status,org"
        r = requests.get(url, timeout=5)
        data = r.json()
        if data['status'] == 'success':
            return data.get('org', 'Unknown')
    except:
        pass
    return 'Unknown'

def warna_status(code):
    if 200 <= code < 300:
        return f"{GREEN}{code}{RESET}"
    elif 300 <= code < 400:
        return f"{YELLOW}{code}{RESET}"
    else:
        return f"{RED}{code}{RESET}"

def scan_satu_url(url, f):
    def tulis(teks):
        with lock:
            f.write(teks + '\n')
            print(teks)

    url = tambah_skema(url)
    tulis(f"\n=== SCAN: {url} ===")

    try:
        domain = urlparse(url).netloc
        ip = socket.gethostbyname(domain)
        tulis(f"IP: {ip}")
        tulis(f"DNS: {domain} -> {ip}")

        isp = get_isp(ip)
        tulis(f"ISP: {isp}")

        with requests.get(url, timeout=15, stream=True, verify=False) as r:
            status = r.status_code
            tulis(f"Status: {warna_status(status)}")
            
            server = r.headers.get('Server', 'Not detected')
            tulis(f"Server: {server}")
            
            cf = 'Protected' if 'cloudflare' in str(r.headers).lower() else 'Unprotected'
            cf_warna = f"{GREEN}{cf}{RESET}" if cf == 'Protected' else f"{RED}{cf}{RESET}"
            tulis(f"Cloudflare: {cf_warna}")

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
        tulis(f"Error: {RED}{e}{RESET}")
    
    tulis("="*40)

def main():
    input_file = "list.txt"
    output_file = "hasil_scan.txt"
    MAX_URL = 30
    THREADS = 15
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file_list:
            urls = [line.strip() for line in file_list if line.strip()]
    except FileNotFoundError:
        print(f"{RED}Error: File {input_file} nggak ketemu{RESET}")
        return

    if len(urls) > MAX_URL:
        print(f"{YELLOW}Peringatan: URL lebih dari {MAX_URL}. Hanya {MAX_URL} pertama yang discan{RESET}")
        urls = urls[:MAX_URL]

    total = len(urls)
    print(f"{CYAN}Total URL: {total}{RESET}")
    print(f"Thread: {THREADS} URL barengan\n")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"=== BATCH SCAN {total} URL ===\n\n")
        
        try:
            with ThreadPoolExecutor(max_workers=THREADS) as executor:
                futures = [executor.submit(scan_satu_url, url, f) for url in urls]
                for future in as_completed(futures):
                    pass
        except KeyboardInterrupt:
            print(f"\n\n{RED}Scan dihentikan manual{RESET}")
            f.write("\nScan dihentikan manual\n")
    
    print(f"\n{GREEN}[SELESAI]{RESET} Hasil: {output_file}")

if __name__ == "__main__":
    main()    try:
        with open(input_file, 'r', encoding='utf-8') as file_list:
            urls = [line.strip() for line in file_list if line.strip()]
    except FileNotFoundError:
        print(f"{RED}Error: File {input_file} nggak ketemu{RESET}")
        return

    total = len(urls)
    print(f"{CYAN}Total URL: {total}{RESET}")
    print(f"Thread: 10 URL barengan\n")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"=== BATCH SCAN {total} URL ===\n\n")
        
        try:
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(scan_satu_url, url, f) for url in urls]
                for future in as_completed(futures):
                    pass
        except KeyboardInterrupt:
            print(f"\n\n{RED}Scan dihentikan manual{RESET}")
            f.write("\nScan dihentikan manual\n")
    
    print(f"\n{GREEN}[SELESAI]{RESET} Hasil: {output_file}")

if __name__ == "__main__":
    main()
EOF
