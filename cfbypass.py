#!/usr/bin/env python3
"""
CLOUDFLARE BYPASS V3 - GERÇEK IP BULUCU
Kullanım: python3 cfbypass.py 10000frogs.com
"""

import socket
import requests
import dns.resolver
import sys
import re
import json
import time
import subprocess
from urllib.parse import urlparse

class CloudflareBypass:
    def __init__(self, domain):
        self.domain = domain
        self.real_ips = set()
        self.cloudflare_ips = set()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
    def print_banner(self):
        print(f"""
╔══════════════════════════════════════════════════════════╗
║     CLOUDFLARE BYPASS - GERÇEK IP BULUCU V3            ║
║     Hedef: {self.domain:<35} ║
╚══════════════════════════════════════════════════════════╝
        """)
    
    # 1. DNS Tarihçesi (ViewDNS)
    def method_viewdns(self):
        print("[*] Yöntem 1: ViewDNS Tarihçesi...")
        try:
            url = f"https://api.viewdns.info/iphistory/?domain={self.domain}"
            r = self.session.get(url, timeout=10)
            if 'ip' in r.text:
                ips = re.findall(r'<ip>([^<]+)</ip>', r.text)
                for ip in ips:
                    if ip and not ip.startswith('103.169'):
                        self.real_ips.add(ip)
                        print(f"    ✅ ViewDNS: {ip}")
        except:
            print("    ❌ ViewDNS başarısız")
    
    # 2. CRT.SH - SSL Sertifika Günlükleri
    def method_crtsh(self):
        print("[*] Yöntem 2: CRT.SH SSL Günlükleri...")
        try:
            url = f"https://crt.sh/?q=%25.{self.domain}&output=json"
            r = self.session.get(url, timeout=10)
            data = r.json()
            for item in data:
                name = item.get('name_value', '')
                if name and '*' not in name:
                    try:
                        ip = socket.gethostbyname(name)
                        if ip and not ip.startswith('103.169'):
                            self.real_ips.add(ip)
                            print(f"    ✅ CRT.SH: {name} -> {ip}")
                    except:
                        pass
        except:
            print("    ❌ CRT.SH başarısız")
    
    # 3. SecurityTrails API (Ücretsiz)
    def method_securitytrails(self):
        print("[*] Yöntem 3: SecurityTrails...")
        try:
            # Web scraping (ücretsiz)
            url = f"https://securitytrails.com/domain/{self.domain}/history/a"
            r = self.session.get(url, timeout=10)
            ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', r.text)
            for ip in ips:
                if ip and not ip.startswith('103.169') and not ip.startswith('104.16'):
                    self.real_ips.add(ip)
                    print(f"    ✅ SecurityTrails: {ip}")
        except:
            print("    ❌ SecurityTrails başarısız")
    
    # 4. DNS Record'lar (MX, NS, TXT)
    def method_dns_records(self):
        print("[*] Yöntem 4: DNS Kayıtları...")
        record_types = ['MX', 'NS', 'TXT', 'CNAME', 'SOA']
        for record_type in record_types:
            try:
                answers = dns.resolver.resolve(self.domain, record_type)
                for rdata in answers:
                    try:
                        ip = socket.gethostbyname(str(rdata.exchange if hasattr(rdata, 'exchange') else rdata))
                        if ip and not ip.startswith('103.169'):
                            self.real_ips.add(ip)
                            print(f"    ✅ DNS {record_type}: {ip}")
                    except:
                        pass
            except:
                pass
    
    # 5. Subdomain Bruteforce
    def method_subdomains(self):
        print("[*] Yöntem 5: Subdomain Taraması...")
        subdomains = [
            'www', 'mail', 'admin', 'dev', 'test', 'api', 'docs', 'cdn', 'blog',
            'shop', 'forum', 'support', 'help', 'status', 'webmail', 'cpanel',
            'panel', 'portal', 'ftp', 'smtp', 'pop', 'imap', 'ns1', 'ns2',
            'direct', 'remote', 'manage', 'cp', 'whm', 'dns', 'mail2', 'web',
            'static', 'img', 'video', 'media', 'app', 'beta', 'demo', 'stage',
            'proxy', 'secure', 'vpn', 'cloud', 'backup', 'files', 'data', 'sql',
            'db', 'mysql', 'postgres', 'redis', 'elastic', 'kibana', 'grafana',
            'jenkins', 'gitlab', 'github', 'jira', 'confluence', 'wiki', 'docs',
            'devops', 'monitor', 'logging', 'metrics', 'analytics', 'stats',
            'report', 'dashboard', 'control', 'manage', 'operator', 'root',
            'system', 'network', 'gateway', 'router', 'firewall', 'auth',
            'oauth', 'sso', 'login', 'signup', 'register', 'account', 'profile',
            'settings', 'config', 'console', 'terminal', 'ssh', 'rdp', 'vnc'
        ]
        
        for sub in subdomains[:200]:
            try:
                full = f"{sub}.{self.domain}"
                ip = socket.gethostbyname(full)
                if ip and not ip.startswith('103.169') and not ip.startswith('104.16'):
                    self.real_ips.add(ip)
                    print(f"    ✅ Subdomain: {full} -> {ip}")
            except:
                pass
    
    # 6. HTTP/HTTPS Header'dan IP
    def method_http_headers(self):
        print("[*] Yöntem 6: HTTP Header Analizi...")
        try:
            # Cloudflare arkasından gerçek IP'yi gösteren header'lar
            headers_to_check = ['CF-Connecting-IP', 'X-Forwarded-For', 'X-Real-IP', 'CF-IPCountry', 'True-Client-IP']
            for protocol in ['https', 'http']:
                try:
                    r = self.session.get(f"{protocol}://{self.domain}", timeout=5)
                    for header in headers_to_check:
                        if header in r.headers:
                            ip = r.headers[header]
                            if ip and not ip.startswith('103.169'):
                                self.real_ips.add(ip)
                                print(f"    ✅ {header}: {ip}")
                except:
                    pass
        except:
            print("    ❌ Header analizi başarısız")
    
    # 7. Zone Transfer Deneme
    def method_zone_transfer(self):
        print("[*] Yöntem 7: Zone Transfer Denemesi...")
        try:
            ns_servers = dns.resolver.resolve(self.domain, 'NS')
            for ns in ns_servers:
                ns_ip = socket.gethostbyname(str(ns))
                try:
                    result = subprocess.run(
                        f"dig axfr {self.domain} @{ns_ip}",
                        shell=True, capture_output=True, text=True, timeout=5
                    )
                    ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', result.stdout)
                    for ip in ips:
                        if ip and not ip.startswith('103.169'):
                            self.real_ips.add(ip)
                            print(f"    ✅ Zone Transfer: {ip}")
                except:
                    pass
        except:
            print("    ❌ Zone Transfer başarısız")
    
    # 8. Shodan (Eğer CLI varsa)
    def method_shodan(self):
        print("[*] Yöntem 8: Shodan...")
        try:
            result = subprocess.run(
                f"shodan search hostname:{self.domain}",
                shell=True, capture_output=True, text=True, timeout=10
            )
            ips = re.findall(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', result.stdout)
            for ip in ips:
                if ip and not ip.startswith('103.169') and not ip.startswith('104.16'):
                    self.real_ips.add(ip)
                    print(f"    ✅ Shodan: {ip}")
        except:
            print("    ❌ Shodan başarısız")
    
    def run(self):
        self.print_banner()
        
        # Tüm yöntemleri çalıştır
        self.method_viewdns()
        self.method_crtsh()
        self.method_securitytrails()
        self.method_dns_records()
        self.method_subdomains()
        self.method_http_headers()
        self.method_zone_transfer()
        self.method_shodan()
        
        # Sonuçları göster
        print("\n" + "="*60)
        print("[+] SONUÇ")
        print("="*60)
        
        if self.real_ips:
            print(f"\n✅ {len(self.real_ips)} ADET GERÇEK IP BULUNDU:\n")
            for ip in sorted(self.real_ips):
                print(f"    🎯 {ip}")
            
            print(f"\n[!] Bu IP'leri dene:")
            for ip in sorted(self.real_ips):
                print(f"    curl -H 'Host: {self.domain}' http://{ip}")
                print(f"    nmap -p- -A {ip}")
        else:
            print("\n❌ GERÇEK IP BULUNAMADI")
            print("\n[!] Olası nedenler:")
            print("    - Tüm alt alan adları Cloudflare proxied")
            print("    - Sunucu tamamen Cloudflare arkasında")
            print("    - Tarihsel kayıtlar silinmiş")
            print("\n[!] Alternatif yöntemler:")
            print("    - Social Engineering (WHOIS'ten hosting sağlayıcısını bul)")
            print("    - Shodan/Censys üzerinden manuel arama")
            print("    - Sunucu sertifikasında IP arama")
            print("    - Google dork ile alt alan adları bulma")
        
        print("\n" + "="*60)
        print("[+] Tarama tamamlandı!")

def main():
    if len(sys.argv) < 2:
        print("Kullanım: python3 cfbypass.py <domain>")
        print("Örnek: python3 cfbypass.py 10000frogs.com")
        sys.exit(1)
    
    domain = sys.argv[1].replace('http://', '').replace('https://', '').split('/')[0]
    bypass = CloudflareBypass(domain)
    bypass.run()

if __name__ == "__main__":
    main()
