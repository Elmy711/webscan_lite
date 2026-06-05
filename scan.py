import requests
from bs4 import BeautifulSoup
import socket
from urllib.parse import urlparse
import urllib3
urllib3.disable_warnings()

GREEN = '\033[92m'
RED = '\033[91m'
YELLOW = '\033[93m'
RESET = '\033[0m'
CYAN = '\033[96m'

def tambah_skema(url):
    url = url.strip()
    if not url.startswith('http'):
        url = 'https://' + url
    return url

def get_isp(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,org", timeout=5)
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
    url = tambah_skema(url)
    f.write(f"\n{url}\n")
    print(f"\n{url}")

    try:
        domain = urlparse(url).netloc
        ip = socket.gethostbyname(domain)
        
        # DNS
        dns_line = f"DNS: {domain} -> {ip}"
        f.write(dns_line + '\n')
        print(dns_line)
        
        # ISP
        isp = get_isp(ip)
        isp_line = f"ISP: {isp}"
        f.write(isp_line + '\n')
        print(isp_line)

        with requests.get(url, timeout=15, verify=False) as r:
            status = r.status_code
            s = f"Status: {warna_status(status)}"
            f.write(s + '\n')
            print(s)
            
            server = r.headers.get('Server', 'Not detected')
            f.write(f"Server: {server}\n")
            print(f"Server: {server}")

            # Cloudflare
            headers_str = str(r.headers).lower()
            cf = 'Protected' if 'cloudflare' in headers_str else 'Unprotected'
            cf_warna = f"{GREEN}{cf}{RESET}" if cf == 'Protected' else f"{RED}{cf}{RESET}"
            cf_line = f"Cloudflare: {cf_warna}"
            f.write(cf_line + '\n')
            print(cf_line)

            soup = BeautifulSoup(r.text[:200000], 'html.parser')
            title = soup.title.string.strip() if soup.title else "No title"
            f.write(f"Title: {title}\n\n")
            print(f"Title: {title}")

    except Exception as e:
        err = f"Error: {RED}{e}{RESET}"
        f.write(err + '\n')
        print(err)
    
    f.write("-"*40 + '\n')

def main():
    input_file = "list.txt"
    output_file = "hasil_scan.txt"
    MAX_URL = 30
    
    try:
        with open(input_file, 'r', encoding='utf-8') as file_list:
            urls = [line.strip() for line in file_list if line.strip()]
    except FileNotFoundError:
        print(f"{RED}Error: File {input_file} nggak ketemu{RESET}")
        return

    urls = urls[:MAX_URL]
    total = len(urls)
    print(f"{CYAN}Total URL: {total}{RESET}\n")

    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"BATCH SCAN {total} URL\n")
        for url in urls:
            scan_satu_url(url, f)
    
    print(f"\n{GREEN}[SELESAI]{RESET} Hasil: {output_file}")

if __name__ == "__main__":
    main()        with open(input_file, 'r', encoding='utf-8') as file_list:
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
    main()        with open(input_file, 'r', encoding='utf-8') as file_list:
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
    main()        with open(input_file, 'r', encoding='utf-8') as file_list:
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
    main()       
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
