#!/usr/bin/env python3
"""
SİTE ÇÖKTÜ MÜ KONTROLÜ - BASİT VERSİYON
Kullanım: python3 check.py hedef.com
"""

import requests
import sys
import time
import socket
from urllib.parse import urlparse

# Renkler
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

def check_site(target):
    """Siteyi kontrol et"""
    
    print(f"\n{Colors.BLUE}{'='*50}{Colors.RESET}")
    print(f"{Colors.BOLD}[+] HEDEF: {target}{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*50}{Colors.RESET}\n")
    
    results = []
    
    # 1. Ping testi
    print(f"{Colors.YELLOW}[*] Ping kontrolü...{Colors.RESET}")
    try:
        if sys.platform.startswith('win'):
            cmd = f"ping -n 2 {target}"
        else:
            cmd = f"ping -c 2 {target}"
        
        import subprocess
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=5)
        
        if "time=" in result.stdout or "TTL" in result.stdout:
            print(f"    {Colors.GREEN}✅ Cevap veriyor{Colors.RESET}")
            results.append(("Ping", "✅ Çalışıyor"))
        else:
            print(f"    {Colors.RED}❌ Cevap yok{Colors.RESET}")
            results.append(("Ping", "❌ Çöktü"))
    except:
        print(f"    {Colors.RED}❌ Hata{Colors.RESET}")
        results.append(("Ping", "❌ Hata"))
    
    # 2. HTTP kontrolü
    print(f"{Colors.YELLOW}[*] HTTP kontrolü...{Colors.RESET}")
    try:
        url = f"http://{target}"
        start = time.time()
        r = requests.get(url, timeout=5)
        elapsed = time.time() - start
        
        if r.status_code == 200:
            print(f"    {Colors.GREEN}✅ HTTP 200 - {elapsed:.2f} sn{Colors.RESET}")
            results.append(("HTTP", f"✅ Çalışıyor ({elapsed:.2f} sn)"))
        elif r.status_code in [503, 504, 500]:
            print(f"    {Colors.RED}❌ HTTP {r.status_code} - SORUN VAR!{Colors.RESET}")
            results.append(("HTTP", f"❌ Çöktü ({r.status_code})"))
        else:
            print(f"    {Colors.YELLOW}⚠️ HTTP {r.status_code}{Colors.RESET}")
            results.append(("HTTP", f"⚠️ {r.status_code}"))
            
    except requests.exceptions.ConnectionError:
        print(f"    {Colors.RED}❌ Bağlantı hatası - ÇÖKMÜŞ OLABİLİR!{Colors.RESET}")
        results.append(("HTTP", "❌ Bağlantı yok"))
    except requests.exceptions.Timeout:
        print(f"    {Colors.RED}❌ Zaman aşımı - ÇÖKTÜ!{Colors.RESET}")
        results.append(("HTTP", "❌ Timeout"))
    except:
        print(f"    {Colors.RED}❌ Hata{Colors.RESET}")
        results.append(("HTTP", "❌ Hata"))
    
    # 3. HTTPS kontrolü
    print(f"{Colors.YELLOW}[*] HTTPS kontrolü...{Colors.RESET}")
    try:
        url = f"https://{target}"
        start = time.time()
        r = requests.get(url, timeout=5, verify=False)
        elapsed = time.time() - start
        
        if r.status_code == 200:
            print(f"    {Colors.GREEN}✅ HTTPS 200 - {elapsed:.2f} sn{Colors.RESET}")
            results.append(("HTTPS", f"✅ Çalışıyor ({elapsed:.2f} sn)"))
        elif r.status_code in [503, 504, 500]:
            print(f"    {Colors.RED}❌ HTTPS {r.status_code} - SORUN VAR!{Colors.RESET}")
            results.append(("HTTPS", f"❌ Çöktü ({r.status_code})"))
        else:
            print(f"    {Colors.YELLOW}⚠️ HTTPS {r.status_code}{Colors.RESET}")
            results.append(("HTTPS", f"⚠️ {r.status_code}"))
            
    except requests.exceptions.ConnectionError:
        print(f"    {Colors.RED}❌ Bağlantı hatası - ÇÖKMÜŞ OLABİLİR!{Colors.RESET}")
        results.append(("HTTPS", "❌ Bağlantı yok"))
    except requests.exceptions.Timeout:
        print(f"    {Colors.RED}❌ Zaman aşımı - ÇÖKTÜ!{Colors.RESET}")
        results.append(("HTTPS", "❌ Timeout"))
    except:
        print(f"    {Colors.RED}❌ Hata{Colors.RESET}")
        results.append(("HTTPS", "❌ Hata"))
    
    # 4. Port kontrolü (80)
    print(f"{Colors.YELLOW}[*] Port 80 kontrolü...{Colors.RESET}")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((target, 80))
        sock.close()
        
        if result == 0:
            print(f"    {Colors.GREEN}✅ Port 80 AÇIK{Colors.RESET}")
            results.append(("Port 80", "✅ Açık"))
        else:
            print(f"    {Colors.RED}❌ Port 80 KAPALI{Colors.RESET}")
            results.append(("Port 80", "❌ Kapalı"))
    except:
        print(f"    {Colors.RED}❌ Hata{Colors.RESET}")
        results.append(("Port 80", "❌ Hata"))
    
    # 5. Port kontrolü (443)
    print(f"{Colors.YELLOW}[*] Port 443 kontrolü...{Colors.RESET}")
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(3)
        result = sock.connect_ex((target, 443))
        sock.close()
        
        if result == 0:
            print(f"    {Colors.GREEN}✅ Port 443 AÇIK{Colors.RESET}")
            results.append(("Port 443", "✅ Açık"))
        else:
            print(f"    {Colors.RED}❌ Port 443 KAPALI{Colors.RESET}")
            results.append(("Port 443", "❌ Kapalı"))
    except:
        print(f"    {Colors.RED}❌ Hata{Colors.RESET}")
        results.append(("Port 443", "❌ Hata"))
    
    # SONUÇ
    print(f"\n{Colors.BLUE}{'='*50}{Colors.RESET}")
    print(f"{Colors.BOLD}[+] SONUÇ{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*50}{Colors.RESET}\n")
    
    # Özet tablosu
    for name, status in results:
        print(f"    {status}")
    
    # Karar
    print(f"\n{Colors.BLUE}{'='*50}{Colors.RESET}")
    
    # Kaç tane çöktü kontrolü
    crashed = [r for r in results if "Çöktü" in r[1] or "Kapalı" in r[1] or "Hata" in r[1] or "Bağlantı yok" in r[1]]
    
    if len(crashed) >= 3:
        print(f"{Colors.RED}{Colors.BOLD}❌ SİTE ÇÖKTÜ!{Colors.RESET}")
        print(f"{Colors.RED}   {len(crashed)}/5 test başarısız{Colors.RESET}")
    elif len(crashed) >= 1:
        print(f"{Colors.YELLOW}{Colors.BOLD}⚠️ SİTE YAVAŞ VEYA SORUNLU!{Colors.RESET}")
        print(f"{Colors.YELLOW}   {len(crashed)}/5 test başarısız{Colors.RESET}")
    else:
        print(f"{Colors.GREEN}{Colors.BOLD}✅ SİTE ÇALIŞIYOR!{Colors.RESET}")
        print(f"{Colors.GREEN}   Tüm testler başarılı{Colors.RESET}")
    
    print(f"{Colors.BLUE}{'='*50}{Colors.RESET}\n")

def main():
    # Komut satırından hedef al
    if len(sys.argv) > 1:
        target = sys.argv[1]
    else:
        print(f"{Colors.YELLOW}[+] Hedef girin (IP veya site adı):{Colors.RESET}")
        target = input("➜ ").strip()
    
    # Temizle
    target = target.replace('http://', '').replace('https://', '').split('/')[0]
    
    if not target:
        print(f"{Colors.RED}❌ Hedef girilmedi!{Colors.RESET}")
        sys.exit(1)
    
    check_site(target)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[+] İptal edildi.{Colors.RESET}")
