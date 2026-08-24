#!/usr/bin/env python3
"""
WEB CANLILIK KONTROL - Hedef erişilebilir mi?
Kullanım: python3 alive.py hedef.com
"""

import socket
import requests
import sys
import ssl
import urllib.parse
from urllib.parse import urlparse
import time
import subprocess

class AliveCheck:
    def __init__(self, target):
        self.target = target
        self.results = {
            'target': target,
            'alive': False,
            'ip': None,
            'ports': [],
            'http_status': None,
            'server': None,
            'ssl': False,
            'redirects': [],
            'response_time': None
        }
    
    def ping_test(self):
        """ICMP ping ile kontrol"""
        try:
            import subprocess
            result = subprocess.run(['ping', '-c', '1', '-W', '2', self.target], 
                                  capture_output=True, timeout=3)
            if result.returncode == 0:
                self.results['alive'] = True
                return True
        except:
            pass
        return False
    
    def dns_resolve(self):
        """DNS çözümleme"""
        try:
            ip = socket.gethostbyname(self.target)
            self.results['ip'] = ip
            return ip
        except:
            return None
    
    def port_check(self, port=80):
        """Belirli port açık mı?"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(2)
            result = sock.connect_ex((self.target, port))
            sock.close()
            if result == 0:
                return True
        except:
            pass
        return False
    
    def http_check(self):
        """HTTP/HTTPS isteği"""
        protocols = ['https', 'http']
        for protocol in protocols:
            try:
                url = f"{protocol}://{self.target}"
                start = time.time()
                r = requests.get(url, timeout=5, allow_redirects=True, verify=False)
                elapsed = time.time() - start
                
                self.results['alive'] = True
                self.results['http_status'] = r.status_code
                self.results['response_time'] = round(elapsed, 2)
                self.results['server'] = r.headers.get('Server', 'Bilinmiyor')
                self.results['ssl'] = protocol == 'https'
                
                if r.history:
                    self.results['redirects'] = [h.url for h in r.history] + [r.url]
                
                return True
            except requests.exceptions.SSLError:
                continue
            except:
                continue
        return False
    
    def port_scan(self):
        """Hızlı port tarama"""
        common_ports = [80, 443, 22, 21, 25, 3306, 8080, 8443, 53, 110, 143, 993, 995]
        open_ports = []
        
        for port in common_ports:
            if self.port_check(port):
                open_ports.append(port)
        
        self.results['ports'] = open_ports
        return open_ports
    
    def whois_check(self):
        """WHOIS bilgisi"""
        try:
            import whois
            w = whois.whois(self.target)
            return {
                'registrar': w.registrar,
                'creation_date': w.creation_date,
                'expiration_date': w.expiration_date
            }
        except:
            return None
    
    def full_check(self):
        """Tüm kontrolleri yap"""
        print(f"\n{'='*60}")
        print(f"[+] Hedef kontrol ediliyor: {self.target}")
        print(f"{'='*60}\n")
        
        # 1. Ping
        print("[*] Ping testi...")
        if self.ping_test():
            print("    ✅ Yanıt veriyor (ICMP)")
        else:
            print("    ❌ Ping yanıtı yok (firewall engelliyor olabilir)")
        
        # 2. DNS
        print("[*] DNS çözümleme...")
        ip = self.dns_resolve()
        if ip:
            print(f"    ✅ IP: {ip}")
        else:
            print("    ❌ DNS çözümlenemedi")
            print("\n[!] HEDEFE ERİŞİM YOK - DNS bulunamadı")
            self.print_summary()
            return
        
        # 3. HTTP/HTTPS
        print("[*] HTTP/HTTPS isteği...")
        if self.http_check():
            print(f"    ✅ HTTP durumu: {self.results['http_status']}")
            print(f"    ✅ Sunucu: {self.results['server']}")
            print(f"    ✅ Yanıt süresi: {self.results['response_time']} sn")
            if self.results['ssl']:
                print("    ✅ SSL/HTTPS aktif")
            if self.results['redirects']:
                print(f"    ✅ Yönlendirme var: {self.results['redirects']}")
        else:
            print("    ❌ HTTP/HTTPS yanıtı yok")
            print("\n[!] Web sunucusu çalışmıyor veya erişilemiyor")
            self.print_summary()
            return
        
        # 4. Port tarama
        print("[*] Port taraması...")
        ports = self.port_scan()
        if ports:
            print(f"    ✅ Açık portlar: {ports}")
        else:
            print("    ❌ Hiç port açık değil")
        
        # 5. WHOIS
        print("[*] WHOIS bilgisi...")
        whois_info = self.whois_check()
        if whois_info:
            print(f"    ✅ Kayıt: {whois_info.get('registrar', 'Bilinmiyor')}")
        
        # Sonuç
        self.print_summary()
    
    def print_summary(self):
        """Özet rapor"""
        print(f"\n{'='*60}")
        print("[+] KONTROL SONUCU")
        print(f"{'='*60}")
        
        if self.results['alive']:
            print("✅ HEDEF CANLI - Erişim var!")
            print(f"   URL: http{'s' if self.results['ssl'] else ''}://{self.target}")
            print(f"   IP: {self.results['ip']}")
            print(f"   Durum: {self.results['http_status']}")
            print(f"   Sunucu: {self.results['server']}")
            print(f"   Süre: {self.results['response_time']} sn")
            if self.results['ports']:
                print(f"   Açık portlar: {self.results['ports']}")
            if self.results['redirects']:
                print(f"   Yönlendirme: {self.results['redirects'][-1]}")
        else:
            print("❌ HEDEFE ERİŞİM YOK")
            print("   Olası nedenler:")
            print("   - Sunucu kapalı")
            print("   - Firewall engelliyor")
            print("   - DNS hatası")
            print("   - Yanlış URL")
        
        print(f"{'='*60}\n")

def main():
    if len(sys.argv) < 2:
        print("Kullanım: python3 alive.py <hedef>")
        print("Örnek: python3 alive.py google.com")
        print("Örnek: python3 alive.py 192.168.1.1")
        print("Örnek: python3 alive.py https://example.com")
        sys.exit(1)
    
    target = sys.argv[1]
    target = target.replace('http://', '').replace('https://', '').split('/')[0]
    
    check = AliveCheck(target)
    check.full_check()

if __name__ == "__main__":
    main()
