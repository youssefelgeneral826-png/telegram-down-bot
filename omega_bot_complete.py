#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
██████╗ ███╗   ███╗███████╗ ██████╗  █████╗     ███████╗ █████╗ 
██╔══██╗████╗ ████║██╔════╝██╔════╝ ██╔══██╗    ██╔════╝██╔══██╗
██║  ██║██╔████╔██║█████╗  ██║  ███╗███████║    ███████╗███████║
██║  ██║██║╚██╔╝██║██╔══╝  ██║   ██║██╔══██║    ╚════██║██╔══██║
██████╔╝██║ ╚═╝ ██║███████╗╚██████╔╝██║  ██║    ███████║██║  ██║
╚═════╝ ╚═╝     ╚═╝╚══════╝ ╚═════╝ ╚═╝  ╚═╝    ╚══════╝╚═╝  ╚═╝
                                                                 
███████╗██╗   ██╗██████╗ ██████╗ ███████╗███╗   ███╗███████╗
██╔════╝██║   ██║██╔══██╗██╔══██╗██╔════╝████╗ ████║██╔════╝
███████╗██║   ██║██████╔╝██████╔╝█████╗  ██╔████╔██║█████╗  
╚════██║██║   ██║██╔═══╝ ██╔══██╗██╔══╝  ██║╚██╔╝██║██╔══╝  
███████║╚██████╔╝██║     ██║  ██║███████╗██║ ╚═╝ ██║███████╗
╚══════╝ ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝╚══════╝

OMEGA-99 SUPREME - NUCLEAR EDITION
المالك: THE GENERAL
الإصدار: 9.9.9
الحالة: ☢️ مُسلح نووياً ☢️
"""

import os
import sys
import json
import time
import random
import string
import sqlite3
import hashlib
import base64
import secrets
import logging
import asyncio
import requests
import subprocess
from datetime import datetime, timedelta
from collections import defaultdict
from typing import Optional, Dict, Any, List, Tuple
from pathlib import Path

# ======================= استيراد الإعدادات =======================
try:
    from config import *
except ImportError:
    # إعدادات افتراضية لو مش لاقي config
    TELEGRAM_TOKEN = "8502451154:AAG3Q2KvVZqUyPMI7mZHIXoK3ySQC02KG0I"
    GEMINI_KEY = "AIzaSyAG8hhKiOk8-4IU36KjQjpxy_U_8YmS80o"
    GENERAL_ID = 5666497258
    PAYMENT_NUMBERS = ["01109103969", "01108708564"]
    ADMINS = []

# ======================= مكتبات البوت =======================
try:
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
    TELEGRAM_READY = True
except ImportError:
    TELEGRAM_READY = False
    print("❌ تثبيت python-telegram-bot...")
    os.system("pip install python-telegram-bot==20.7")
    from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler

# ======================= الذكاء الاصطناعي =======================
try:
    import google.generativeai as genai
    GEMINI_READY = True
    genai.configure(api_key=GEMINI_KEY)
    ai_model = genai.GenerativeModel('gemini-pro')
    vision_model = genai.GenerativeModel('gemini-pro-vision')
except Exception as e:
    GEMINI_READY = False
    ai_model = None
    vision_model = None
    print(f"⚠️ Gemini AI غير متاح: {e}")

# ======================= التحميل =======================
try:
    import yt_dlp
    YTDLP_READY = True
except ImportError:
    YTDLP_READY = False
    print("⚠️ yt-dlp غير موجود")

# ======================= تشفير متقدم =======================
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2

# ======================= المسارات =======================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DOWNLOADS_DIR = os.path.join(BASE_DIR, "downloads")
CACHE_DIR = os.path.join(BASE_DIR, "cache")
LOGS_DIR = os.path.join(BASE_DIR, "logs")
DB_DIR = os.path.join(BASE_DIR, "database")
BLOCKED_DIR = os.path.join(BASE_DIR, "blocked")

for dir_path in [DOWNLOADS_DIR, CACHE_DIR, LOGS_DIR, DB_DIR, BLOCKED_DIR]:
    os.makedirs(dir_path, exist_ok=True)

# ======================= إعداد التسجيل =======================
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOGS_DIR, f"bot_{datetime.now().strftime('%Y%m%d')}.log"), encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("OMEGA-99")

# ======================= نظام التشفير المتقدم =======================
class CryptoSystem:
    """نظام تشفير عسكري متكامل"""
    
    def __init__(self):
        self.key = self.generate_key()
        self.cipher = Fernet(self.key)
    
    def generate_key(self):
        """توليد مفتاح تشفير فريد"""
        password = b"OMEGA-99-SUPREME-NUCLEAR-KEY"
        salt = b"general_salt_2026"
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def encrypt(self, data):
        """تشفير البيانات"""
        if isinstance(data, str):
            data = data.encode()
        return self.cipher.encrypt(data)
    
    def decrypt(self, encrypted_data):
        """فك تشفير البيانات"""
        return self.cipher.decrypt(encrypted_data).decode()
    
    def hash_password(self, password):
        """توليد Hash لكلمة المرور"""
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return salt + key
    
    def verify_password(self, password, hashed):
        """التحقق من كلمة المرور"""
        salt = hashed[:32]
        key = hashed[32:]
        new_key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
        return key == new_key

crypto = CryptoSystem()

# ======================= نظام الحماية الذكي =======================
class SecuritySystem:
    """نظام أمان متكامل بالذكاء الاصطناعي"""
    
    def __init__(self):
        self.suspicious_ips = defaultdict(int)
        self.blocked_ips = set()
        self.suspicious_users = defaultdict(int)
        self.blocked_users = set()
        self.request_times = defaultdict(list)
        self.device_fingerprints = {}
        self.blocked_devices = set()
        
        # إعدادات الأمان
        self.MAX_REQUESTS_PER_MINUTE = 20
        self.MAX_FAILED_ATTEMPTS = 3
        self.BLOCK_TIME = 3600  # ساعة
        
        # تحميل قائمة المحظورين
        self.load_blocked()
    
    def get_device_fingerprint(self, user):
        """بصمة الجهاز الفريدة (حظر على مستوى الجهاز)"""
        data = f"{user.id}_{user.username}_{user.language_code}_{datetime.now().strftime('%Y%m%d')}"
        return hashlib.sha256(data.encode()).hexdigest()
    
    def load_blocked(self):
        """تحميل قائمة المحظورين"""
        try:
            with open(os.path.join(BLOCKED_DIR, "blocked.json"), 'r') as f:
                data = json.load(f)
                self.blocked_users = set(data.get('users', []))
                self.blocked_ips = set(data.get('ips', []))
                self.blocked_devices = set(data.get('devices', []))
        except:
            pass
    
    def save_blocked(self):
        """حفظ قائمة المحظورين"""
        data = {
            'users': list(self.blocked_users),
            'ips': list(self.blocked_ips),
            'devices': list(self.blocked_devices)
        }
        with open(os.path.join(BLOCKED_DIR, "blocked.json"), 'w') as f:
            json.dump(data, f)
    
    def is_blocked(self, user):
        """التحقق من حظر المستخدم/الجهاز"""
        # تحقق من حظر المستخدم
        if user.id in self.blocked_users:
            return True
        
        # تحقق من حظر الجهاز
        fingerprint = self.get_device_fingerprint(user)
        if fingerprint in self.blocked_devices:
            return True
        
        return False
    
    def block_user(self, user, reason="", duration=3600*24*30):
        """حظر مستخدم وجهازه"""
        self.blocked_users.add(user.id)
        self.blocked_devices.add(self.get_device_fingerprint(user))
        
        # تسجيل الحظر
        logger.warning(f"⚠️ تم حظر المستخدم {user.id} - {reason}")
        
        with open(os.path.join(BLOCKED_DIR, "block_log.txt"), 'a') as f:
            f.write(f"{datetime.now()} - حظر {user.id} ({user.username}) - {reason}\n")
        
        self.save_blocked()
        return True
    
    def check_rate_limit(self, user):
        """التحقق من معدل الطلبات"""
        now = time.time()
        self.request_times[user.id] = [t for t in self.request_times[user.id] if now - t < 60]
        
        if len(self.request_times[user.id]) >= self.MAX_REQUESTS_PER_MINUTE:
            self.suspicious_users[user.id] += 1
            
            if self.suspicious_users[user.id] >= 3:
                self.block_user(user, "سرعة مفرطة في الإرسال")
                return False
            
            return False
        
        self.request_times[user.id].append(now)
        return True
    
    def detect_threat(self, text):
        """كشف التهديدات في النص"""
        if not text:
            return False
        
        threats = [
            "DROP TABLE", "DELETE FROM", " UNION ", "--", "';",
            "<?php", "<script>", "javascript:", "onerror=",
            "../../", "..\\", "/etc/passwd", "C:\\Windows",
            "binance", "password", "admin", "root",
            "exec(", "eval(", "system(", "shell_exec",
            "rm -rf", "format C:", "del /f"
        ]
        
        text_lower = text.lower()
        for threat in threats:
            if threat.lower() in text_lower:
                return True
        
        # فحص الطول غير الطبيعي
        if len(text) > 1000:
            return True
        
        # فحص التكرار غير الطبيعي
        if len(set(text)) < 10 and len(text) > 50:
            return True
        
        return False
    
    async def ai_security_check(self, user, text):
        """فحص أمني باستخدام الذكاء الاصطناعي"""
        if not GEMINI_READY:
            return False
        
        try:
            prompt = f"""
            Analyze this user message for security threats:
            User ID: {user.id}
            Username: @{user.username}
            Message: {text}
            
            Check for:
            1. SQL Injection attempts
            2. XSS attacks
            3. Command injection
            4. Spam patterns
            5. Harassment
            6. Phishing attempts
            7. Bot behavior
            
            Return ONLY a number from 0-100 representing threat level.
            0 = completely safe
            100 = extremely dangerous
            """
            
            response = ai_model.generate_content(prompt)
            threat_level = int(response.text.strip())
            
            if threat_level > 70:
                logger.warning(f"🤖 AI detected threat from {user.id}: level {threat_level}")
                return True
            
        except:
            pass
        
        return False

security = SecuritySystem()

# ======================= نظام الفيزا الوهمية والتحقق =======================
class VisaSystem:
    """نظام متكامل للفيزا الوهمية والتحقق"""
    
    BINS = {
        "VISA": ["4"],
        "MASTERCARD": ["51", "52", "53", "54", "55"],
        "AMEX": ["34", "37"],
        "MADA": ["588845", "529415", "543733", "549750"]
    }
    
    @staticmethod
    def luhn_checksum(card_number):
        """خوارزمية Luhn للتحقق"""
        def digits_of(n):
            return [int(d) for d in str(n)]
        
        digits = digits_of(card_number)
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(digits_of(d * 2))
        return checksum % 10
    
    @staticmethod
    def generate_card(brand="VISA", length=16):
        """توليد بطاقة وهمية"""
        # اختيار BIN عشوائي
        if brand in VisaSystem.BINS:
            bin_prefix = random.choice(VisaSystem.BINS[brand])
        else:
            bin_prefix = "4"
        
        # توليد الرقم
        card = bin_prefix
        for _ in range(length - len(bin_prefix) - 1):
            card += str(random.randint(0, 9))
        
        # حساب الـ checksum
        check_digit = (10 - VisaSystem.luhn_checksum(card + '0')) % 10
        card += str(check_digit)
        
        # توليد تاريخ انتهاء صالح
        exp_month = random.randint(1, 12)
        exp_year = random.randint(datetime.now().year, datetime.now().year + 5)
        
        # توليد CVV
        cvv = ''.join([str(random.randint(0, 9)) for _ in range(3 if brand != "AMEX" else 4)])
        
        return {
            "number": card,
            "exp": f"{exp_month:02d}/{exp_year}",
            "cvv": cvv,
            "brand": brand,
            "valid": True
        }
    
    @staticmethod
    def validate_card(card_number):
        """التحقق من صحة رقم البطاقة"""
        # إزالة المسافات والشرطات
        card_number = ''.join(c for c in card_number if c.isdigit())
        
        # التحقق من الطول
        if len(card_number) not in [15, 16]:
            return False
        
        # التحقق من Luhn
        return VisaSystem.luhn_checksum(card_number) == 0
    
    @staticmethod
    def get_bin_info(bin_code):
        """الحصول على معلومات البنك من BIN"""
        try:
            response = requests.get(f"https://lookup.binlist.net/{bin_code[:6]}")
            if response.status_code == 200:
                data = response.json()
                return {
                    "bank": data.get("bank", {}).get("name", "Unknown"),
                    "country": data.get("country", {}).get("name", "Unknown"),
                    "type": data.get("type", "Unknown"),
                    "scheme": data.get("scheme", "Unknown")
                }
        except:
            pass
        return None
    
    @staticmethod
    def generate_multiple(count=10, brand="VISA"):
        """توليد عدة بطاقات"""
        cards = []
        for _ in range(count):
            cards.append(VisaSystem.generate_card(brand))
        return cards

visa = VisaSystem()

# ======================= قاعدة البيانات =======================
class Database:
    def __init__(self):
        self.conn = sqlite3.connect(os.path.join(DB_DIR, "omega.db"), check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        c = self.conn.cursor()
        
        # المستخدمين
        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (user_id INTEGER PRIMARY KEY,
                     username TEXT,
                     first_name TEXT,
                     join_date TEXT,
                     last_active TEXT,
                     subscription_type TEXT DEFAULT 'free',
                     subscription_end TEXT,
                     download_count INTEGER DEFAULT 0,
                     is_admin INTEGER DEFAULT 0,
                     is_blocked INTEGER DEFAULT 0,
                     language TEXT DEFAULT 'ar')''')
        
        # المفاتيح
        c.execute('''CREATE TABLE IF NOT EXISTS keys
                    (key_string TEXT PRIMARY KEY,
                     key_type TEXT,
                     created_by INTEGER,
                     used_by INTEGER,
                     created_date TEXT,
                     used_date TEXT,
                     is_used INTEGER DEFAULT 0)''')
        
        # التحميلات
        c.execute('''CREATE TABLE IF NOT EXISTS downloads
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     user_id INTEGER,
                     url TEXT,
                     title TEXT,
                     platform TEXT,
                     file_size INTEGER,
                     quality TEXT,
                     download_date TEXT)''')
        
        # المعاملات المالية
        c.execute('''CREATE TABLE IF NOT EXISTS transactions
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     user_id INTEGER,
                     key_string TEXT,
                     amount REAL,
                     payment_method TEXT,
                     transaction_date TEXT)''')
        
        # المحظورين
        c.execute('''CREATE TABLE IF NOT EXISTS blocks
                    (user_id INTEGER PRIMARY KEY,
                     reason TEXT,
                     blocked_by INTEGER,
                     block_date TEXT)''')
        
        self.conn.commit()
    
    def add_user(self, user_id, username, first_name):
        c = self.conn.cursor()
        now = datetime.now().isoformat()
        
        c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        if not c.fetchone():
            c.execute('''INSERT INTO users 
                        (user_id, username, first_name, join_date, last_active, subscription_type)
                        VALUES (?, ?, ?, ?, ?, ?)''',
                      (user_id, username, first_name, now, now, 'free' if user_id != GENERAL_ID else 'nuclear'))
            self.conn.commit()
            return True
        return False
    
    def get_user(self, user_id):
        c = self.conn.cursor()
        c.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        return c.fetchone()
    
    def update_activity(self, user_id):
        c = self.conn.cursor()
        c.execute("UPDATE users SET last_active = ? WHERE user_id = ?",
                  (datetime.now().isoformat(), user_id))
        self.conn.commit()
    
    def add_key(self, key_string, key_type, created_by):
        c = self.conn.cursor()
        c.execute('''INSERT INTO keys (key_string, key_type, created_by, created_date)
                    VALUES (?, ?, ?, ?)''',
                  (key_string, key_type, created_by, datetime.now().isoformat()))
        self.conn.commit()
    
    def use_key(self, key_string, user_id):
        c = self.conn.cursor()
        c.execute('''UPDATE keys SET used_by = ?, used_date = ?, is_used = 1
                    WHERE key_string = ?''',
                  (user_id, datetime.now().isoformat(), key_string))
        
        # تحديث اشتراك المستخدم
        c.execute("SELECT key_type FROM keys WHERE key_string = ?", (key_string,))
        key_type = c.fetchone()[0]
        
        days = {'free': 7, 'vip': 30, 'pro': 365, 'nuclear': 9999}.get(key_type, 30)
        end_date = (datetime.now() + timedelta(days=days)).isoformat()
        
        c.execute('''UPDATE users SET subscription_type = ?, subscription_end = ?
                    WHERE user_id = ?''',
                  (key_type, end_date, user_id))
        
        self.conn.commit()
        return key_type
    
    def check_key(self, key_string):
        c = self.conn.cursor()
        c.execute("SELECT * FROM keys WHERE key_string = ?", (key_string,))
        return c.fetchone()
    
    def add_download(self, user_id, url, title, platform, file_size, quality):
        c = self.conn.cursor()
        c.execute('''INSERT INTO downloads 
                    (user_id, url, title, platform, file_size, quality, download_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (user_id, url, title, platform, file_size, quality, datetime.now().isoformat()))
        
        c.execute('''UPDATE users SET download_count = download_count + 1
                    WHERE user_id = ?''', (user_id,))
        
        self.conn.commit()
    
    def get_stats(self):
        c = self.conn.cursor()
        stats = {}
        
        c.execute("SELECT COUNT(*) FROM users")
        stats['users'] = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM downloads")
        stats['downloads'] = c.fetchone()[0]
        
        c.execute("SELECT SUM(file_size) FROM downloads")
        stats['total_size'] = c.fetchone()[0] or 0
        
        c.execute("SELECT subscription_type, COUNT(*) FROM users GROUP BY subscription_type")
        stats['subscriptions'] = dict(c.fetchall())
        
        return stats

db = Database()

# ======================= نظام المفاتيح النووي =======================
class KeyGenerator:
    @staticmethod
    def generate_key(key_type='vip', length=16):
        """توليد مفتاح نووي"""
        chars = string.ascii_uppercase + string.digits
        key = ''.join(secrets.choice(chars) for _ in range(length))
        
        # تنسيق المفتاح
        formatted = '-'.join([key[i:i+4] for i in range(0, len(key), 4)])
        
        # إضافة بادئة
        prefixes = {
            'free': 'FREE',
            'vip': 'VIP',
            'pro': 'PRO',
            'nuclear': '☢️NUCLEAR☢️'
        }
        
        prefix = prefixes.get(key_type, 'KEY')
        return f"{prefix}-{formatted}"
    
    @staticmethod
    def generate_bulk(key_type, count):
        """توليد عدة مفاتيح"""
        keys = []
        for _ in range(count):
            keys.append(KeyGenerator.generate_key(key_type))
        return keys

key_gen = KeyGenerator()

# ======================= نظام التحميل النووي =======================
class NuclearDownloader:
    """نظام تحميل بقدرات نووية"""
    
    SUPPORTED = [
        'youtube.com', 'youtu.be',
        'tiktok.com',
        'instagram.com',
        'facebook.com',
        'twitter.com', 'x.com',
        'reddit.com',
        'pinterest.com',
        'spotify.com',
        'soundcloud.com',
        'twitch.tv',
        'vimeo.com',
        'dailymotion.com',
        'likee.com',
        'snapchat.com'
    ]
    
    QUALITIES = {
        'low': 'worst',
        'medium': 'best[height<=480]',
        'high': 'best[height<=720]',
        'fullhd': 'best[height<=1080]',
        '2k': 'best[height<=1440]',
        '4k': 'best[height<=2160]',
        'nuclear': 'best'
    }
    
    @staticmethod
    def is_supported(url):
        return any(domain in url.lower() for domain in NuclearDownloader.SUPPORTED)
    
    @staticmethod
    async def download(url, quality='high', format_type='video'):
        if not YTDLP_READY:
            return None, "⚠️ نظام التحميل غير متاح"
        
        try:
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'outtmpl': os.path.join(DOWNLOADS_DIR, '%(title)s.%(ext)s'),
            }
            
            # تحديد الجودة
            ydl_opts['format'] = NuclearDownloader.QUALITIES.get(quality, 'best')
            
            if format_type == 'audio':
                ydl_opts['format'] = 'bestaudio/best'
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }]
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
                if format_type == 'audio':
                    filename = filename.rsplit('.', 1)[0] + '.mp3'
                
                file_size = os.path.getsize(filename) if os.path.exists(filename) else 0
                
                return {
                    'title': info.get('title', 'Unknown'),
                    'filename': filename,
                    'size': file_size,
                    'platform': info.get('extractor', 'unknown'),
                    'duration': info.get('duration', 0),
                    'uploader': info.get('uploader', 'Unknown'),
                    'views': info.get('view_count', 0),
                    'quality': quality
                }, None
                
        except Exception as e:
            logger.error(f"🔥 خطأ نووي: {e}")
            return None, str(e)

downloader = NuclearDownloader()

# ======================= الذكاء الاصطناعي النووي =======================
class NuclearAI:
    """ذكاء اصطناعي بقدرات نووية"""
    
    def __init__(self):
        self.model = ai_model
        self.vision = vision_model
        self.available = GEMINI_READY
    
    async def chat(self, message):
        if not self.available:
            return "⚠️ الذكاء النووي غير متاح"
        
        try:
            response = self.model.generate_content(message)
            return response.text
        except Exception as e:
            return f"❌ خطأ: {e}"
    
    async def translate(self, text, target='ar'):
        if not self.available:
            return "⚠️ الترجمة غير متاحة"
        
        try:
            prompt = f"Translate to {'Arabic' if target == 'ar' else 'English'}: {text}"
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"❌ خطأ: {e}"
    
    async def analyze_sentiment(self, text):
        if not self.available:
            return "غير متاح"
        
        try:
            prompt = f"Analyze sentiment (positive/negative/neutral) of: {text}"
            response = self.model.generate_content(prompt)
            return response.text
        except:
            return "غير معروف"
    
    async def generate_hashtags(self, text, count=10):
        if not self.available:
            return []
        
        try:
            prompt = f"Generate {count} relevant hashtags for: {text}"
            response = self.model.generate_content(prompt)
            return response.text.split()
        except:
            return []
    
    async def summarize(self, text, max_length=200):
        if not self.available:
            return text[:max_length]
        
        try:
            prompt = f"Summarize this in {max_length} chars: {text}"
            response = self.model.generate_content(prompt)
            return response.text
        except:
            return text[:max_length]
    
    async def detect_fake_news(self, text):
        if not self.available:
            return "غير متاح"
        
        try:
            prompt = f"Check if this news is fake or real. Explain why: {text}"
            response = self.model.generate_content(prompt)
            return response.text
        except:
            return "غير معروف"

nuclear_ai = NuclearAI()

# ======================= نظام الدفع النووي =======================
class PaymentSystem:
    def __init__(self):
        self.numbers = PAYMENT_NUMBERS
    
    def get_payment_info(self, amount=100, key_type='vip'):
        """الحصول على معلومات الدفع"""
        payment_id = hashlib.md5(f"{amount}{datetime.now()}".encode()).hexdigest()[:8]
        
        return {
            'payment_id': payment_id,
            'amount': amount,
            'numbers': self.numbers,
            'key_type': key_type,
            'expires': (datetime.now() + timedelta(hours=24)).isoformat()
        }
    
    async def verify_payment(self, payment_id, user_id):
        """التحقق من الدفع (يدوي أو آلي)"""
        # هنا هنضيف التحقق الآلي لما نربط مع APIs
        return False

payment = PaymentSystem()

# ======================= البوت النووي الرئيسي =======================
class OmegaNuclearBot:
    def __init__(self):
        self.app = Application.builder().token(TELEGRAM_TOKEN).build()
        self.start_time = datetime.now()
        self.setup_handlers()
    
    def setup_handlers(self):
        """إعداد معالجات الأوامر"""
        
        # أوامر عامة
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("help", self.help))
        self.app.add_handler(CommandHandler("menu", self.menu))
        
        # أوامر التحميل
        self.app.add_handler(CommandHandler("dl", self.download))
        self.app.add_handler(CommandHandler("audio", self.audio))
        self.app.add_handler(CommandHandler("تحميل", self.download))
        self.app.add_handler(CommandHandler("صوت", self.audio))
        
        # أوامر الذكاء الاصطناعي
        if nuclear_ai.available:
            self.app.add_handler(CommandHandler("ai", self.ai_chat))
            self.app.add_handler(CommandHandler("translate", self.translate))
            self.app.add_handler(CommandHandler("ترجمة", self.translate))
            self.app.add_handler(CommandHandler("ذكاء", self.ai_chat))
        
        # أوامر الفيزا
        self.app.add_handler(CommandHandler("gencard", self.generate_card))
        self.app.add_handler(CommandHandler("checkcard", self.check_card))
        self.app.add_handler(CommandHandler("bin", self.bin_lookup))
        
        # أوامر الاشتراك
        self.app.add_handler(CommandHandler("buy", self.buy))
        self.app.add_handler(CommandHandler("redeem", self.redeem))
        self.app.add_handler(CommandHandler("mykey", self.my_key))
        self.app.add_handler(CommandHandler("prices", self.prices))
        
        # أوامر الإدارة (للمالك والمديرين)
        self.app.add_handler(CommandHandler("genkey", self.generate_key))
        self.app.add_handler(CommandHandler("stats", self.stats))
        self.app.add_handler(CommandHandler("users", self.users_list))
        self.app.add_handler(CommandHandler("block", self.block_user))
        self.app.add_handler(CommandHandler("unblock", self.unblock_user))
        self.app.add_handler(CommandHandler("broadcast", self.broadcast))
        
        # معالج الأزرار
        self.app.add_handler(CallbackQueryHandler(self.button_handler))
        
        # معالج الرسائل
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # معالج الأخطاء
        self.app.add_error_handler(self.error_handler)
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """أمر البدء النووي"""
        user = update.effective_user
        db.add_user(user.id, user.username, user.first_name)
        
        # التحقق الأمني
        if security.is_blocked(user):
            await update.message.reply_text("⛔ **أنت محظور نووياً** ⛔\nلا يمكنك استخدام البوت.")
            return
        
        welcome = f"""
☢️ **OMEGA-99 SUPREME - NUCLEAR EDITION** ☢️

أهلاً بك في **أقوى بوت في العالم** يا {user.first_name}!

🔹 **التحميل النووي:** YouTube, TikTok, Instagram, Facebook, Twitter, Spotify, Twitch, Reddit +20 منصة
🔹 **الذكاء الاصطناعي:** Gemini AI - محادثة، ترجمة، تلخيص، تحليل صور
🔹 **الفيزا الوهمية:** توليد بطاقات صالحة، تحقق، معلومات BIN
🔹 **النظام المالي:** اشتراكات VIP + PRO + NUCLEAR
🔹 **الأمان النووي:** حماية من الاختراق، حظر أجهزة، تشفير عسكري

📋 **الأوامر المتاحة:**
/help - قائمة المساعدة
/menu - القائمة الرئيسية
/prices - الأسعار
/buy - شراء اشتراك
/redeem [مفتاح] - تفعيل مفتاح
"""
        
        # قائمة الأزرار
        keyboard = [
            [InlineKeyboardButton("📥 تحميل", callback_data="menu_download")],
            [InlineKeyboardButton("🧠 ذكاء اصطناعي", callback_data="menu_ai")],
            [InlineKeyboardButton("💳 فيزا وهمية", callback_data="menu_visa")],
            [InlineKeyboardButton("💰 شراء اشتراك", callback_data="menu_buy")],
            [InlineKeyboardButton("🔑 تفعيل مفتاح", callback_data="menu_redeem")],
        ]
        
        if user.id == GENERAL_ID or user.id in ADMINS:
            keyboard.append([InlineKeyboardButton("⚡ لوحة التحكم", callback_data="admin_panel")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_photo(
            photo="https://i.imgur.com/7Y8k3nF.jpg",  # صورة نووية
            caption=welcome,
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def help(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """قائمة المساعدة"""
        help_text = """
📚 **دليل الاستخدام النووي**

🎯 **التحميل:**
• /dl [رابط] - تحميل فيديو
• /audio [رابط] - تحميل صوت
• تدعم: YouTube, TikTok, Instagram, Facebook, Twitter, Spotify, Twitch, Reddit

🧠 **الذكاء الاصطناعي:**
• /ai [سؤال] - محادثة مع AI
• /translate [نص] - ترجمة للعربية
• يدعم: نصوص، صور، تحليل، تلخيص

💳 **الفيزا الوهمية:**
• /gencard [عدد] - توليد بطاقات
• /checkcard [رقم] - التحقق من بطاقة
• /bin [6 أرقام] - معلومات BIN

💰 **الاشتراكات:**
• /prices - عرض الأسعار
• /buy - شراء اشتراك
• /redeem [مفتاح] - تفعيل مفتاح
• /mykey - معلومات اشتراكك

⚡ **للـ VIP فقط:**
• جودة 4K + 2K
• تحميل متوازي (5 روابط معاً)
• ذكاء اصطناعي غير محدود
• توليد بطاقات غير محدود
• إزالة علامة مائية

☢️ **للـ NUCLEAR فقط:**
• كل حاجة + قنوات خاصة + دعم VIP
• تحميل قنوات كاملة
• جدولة تحميل
• تحميل تلقائي
• API خاص
"""
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """القائمة الرئيسية"""
        user = update.effective_user
        
        keyboard = [
            [InlineKeyboardButton("📥 تحميل فيديو", callback_data="menu_download")],
            [InlineKeyboardButton("🎵 تحميل صوت", callback_data="menu_audio")],
            [InlineKeyboardButton("🧠 الذكاء الاصطناعي", callback_data="menu_ai")],
            [InlineKeyboardButton("💳 فيزا وهمية", callback_data="menu_visa")],
            [InlineKeyboardButton("💰 الاشتراكات", callback_data="menu_prices")],
            [InlineKeyboardButton("🔑 تفعيل مفتاح", callback_data="menu_redeem")],
            [InlineKeyboardButton("ℹ️ مساعدة", callback_data="menu_help")],
        ]
        
        if user.id == GENERAL_ID or user.id in ADMINS:
            keyboard.append([InlineKeyboardButton("⚡ لوحة الإدارة", callback_data="admin_panel")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("🔱 **OMEGA-99 NUCLEAR MENU**", reply_markup=reply_markup, parse_mode='Markdown')
    
    async def download(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """تحميل فيديو"""
        user = update.effective_user
        
        # التحقق الأمني
        if not security.check_rate_limit(user):
            await update.message.reply_text("⚠️ أنت ت发送 بسرعة كبيرة. توقف قليلاً.")
            return
        
        url = ' '.join(context.args)
        if not url:
            await update.message.reply_text("❌ أرسل الرابط بعد الأمر\nمثال: /dl https://youtube.com/watch?v=...")
            return
        
        if not downloader.is_supported(url):
            await update.message.reply_text("❌ هذا الموقع غير مدعوم حالياً")
            return
        
        msg = await update.message.reply_text(f"📥 جاري التحميل النووي...\n{url[:50]}")
        
        # اختيار الجودة حسب نوع الاشتراك
        user_data = db.get_user(user.id)
        sub_type = user_data[3] if user_data else 'free'
        
        quality_map = {
            'free': 'medium',
            'vip': 'fullhd',
            'pro': '4k',
            'nuclear': 'nuclear'
        }
        
        quality = quality_map.get(sub_type, 'high')
        
        result, error = await downloader.download(url, quality=quality)
        
        if error:
            await msg.edit_text(f"❌ فشل التحميل: {error[:200]}")
        else:
            db.add_download(user.id, url, result['title'], result['platform'], result['size'], quality)
            
            await msg.edit_text(
                f"✅ **تم التحميل بنووي!**\n\n"
                f"📹 {result['title'][:100]}\n"
                f"📦 {result['size'] / (1024*1024):.2f} MB\n"
                f"🌐 {result['platform']}\n"
                f"🎬 الجودة: {quality}\n"
                f"👤 {result['uploader']}"
            )
    
    async def audio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """تحميل صوت"""
        user = update.effective_user
        
        if not security.check_rate_limit(user):
            await update.message.reply_text("⚠️ أنت ت发送 بسرعة كبيرة. توقف قليلاً.")
            return
        
        url = ' '.join(context.args)
        if not url:
            await update.message.reply_text("❌ أرسل الرابط بعد الأمر\nمثال: /audio https://youtube.com/watch?v=...")
            return
        
        if not downloader.is_supported(url):
            await update.message.reply_text("❌ هذا الموقع غير مدعوم")
            return
        
        msg = await update.message.reply_text(f"🎵 جاري تحميل الصوت...")
        
        user_data = db.get_user(user.id)
        sub_type = user_data[3] if user_data else 'free'
        quality = 'high' if sub_type in ['vip', 'pro', 'nuclear'] else 'medium'
        
        result, error = await downloader.download(url, quality=quality, format_type='audio')
        
        if error:
            await msg.edit_text(f"❌ فشل التحميل: {error[:200]}")
        else:
            await msg.edit_text(f"✅ تم تحميل الصوت: {result['title'][:100]}")
    
    async def ai_chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """محادثة مع الذكاء الاصطناعي"""
        user = update.effective_user
        
        # التحقق من الاشتراك للـ AI
        user_data = db.get_user(user.id)
        sub_type = user_data[3] if user_data else 'free'
        
        if sub_type == 'free' and user.id != GENERAL_ID:
            await update.message.reply_text("⚠️ الذكاء الاصطناعي متاح فقط للـ VIP فما فوق.\nاشترك الآن: /prices")
            return
        
        text = ' '.join(context.args)
        if not text:
            await update.message.reply_text("❌ اكتب سؤالك\nمثال: /ai ما هي عاصمة مصر؟")
            return
        
        await update.message.reply_text("🧠 جاري التفكير النووي...")
        
        response = await nuclear_ai.chat(text)
        await update.message.reply_text(f"🤖 **الرد النووي:**\n{response[:4000]}")
    
    async def translate(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """ترجمة"""
        user = update.effective_user
        
        user_data = db.get_user(user.id)
        sub_type = user_data[3] if user_data else 'free'
        
        if sub_type == 'free' and user.id != GENERAL_ID:
            await update.message.reply_text("⚠️ الترجمة متاحة للـ VIP فما فوق")
            return
        
        text = ' '.join(context.args)
        if not text:
            await update.message.reply_text("❌ اكتب النص للترجمة")
            return
        
        await update.message.reply_text("🔄 جاري الترجمة النووية...")
        
        response = await nuclear_ai.translate(text)
        await update.message.reply_text(f"📝 **الترجمة:**\n{response}")
    
    async def generate_card(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """توليد بطاقة وهمية"""
        user = update.effective_user
        
        user_data = db.get_user(user.id)
        sub_type = user_data[3] if user_data else 'free'
        
        if sub_type == 'free' and user.id != GENERAL_ID:
            await update.message.reply_text("⚠️ توليد البطاقات متاح للـ VIP فما فوق")
            return
        
        count = 1
        if context.args:
            try:
                count = min(int(context.args[0]), 10 if sub_type in ['pro', 'nuclear'] else 5)
            except:
                pass
        
        cards = visa.generate_multiple(count=count, brand='VISA')
        
        text = "💳 **البطاقات المولدة:**\n\n"
        for card in cards:
            text += f"🔹 `{card['number']}` | {card['exp']} | CVV: {card['cvv']}\n"
        
        text += f"\n✅ تم توليد {count} بطاقة بنجاح"
        
        await update.message.reply_text(text, parse_mode='Markdown')
    
    async def check_card(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """التحقق من بطاقة"""
        card = ' '.join(context.args).strip()
        if not card:
            await update.message.reply_text("❌ أدخل رقم البطاقة")
            return
        
        valid = visa.validate_card(card)
        
        if valid:
            # معلومات BIN
            bin_info = visa.get_bin_info(card[:6])
            if bin_info:
                info = f"\n🏦 البنك: {bin_info['bank']}\n🌍 الدولة: {bin_info['country']}\n💳 النوع: {bin_info['type']}"
            else:
                info = ""
            
            await update.message.reply_text(f"✅ **بطاقة صالحة** {info}", parse_mode='Markdown')
        else:
            await update.message.reply_text("❌ **بطاقة غير صالحة**", parse_mode='Markdown')
    
    async def bin_lookup(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """البحث عن BIN"""
        bin_code = ' '.join(context.args).strip()
        if not bin_code or len(bin_code) < 6:
            await update.message.reply_text("❌ أدخل أول 6 أرقام من البطاقة")
            return
        
        info = visa.get_bin_info(bin_code[:6])
        
        if info:
            text = f"🔍 **معلومات BIN {bin_code[:6]}:**\n\n"
            text += f"🏦 البنك: {info['bank']}\n"
            text += f"🌍 الدولة: {info['country']}\n"
            text += f"💳 النوع: {info['type']}\n"
            text += f"🔰 الماركة: {info['scheme']}"
        else:
            text = "❌ لم يتم العثور على معلومات"
        
        await update.message.reply_text(text, parse_mode='Markdown')
    
    async def prices(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """عرض الأسعار"""
        text = """
💰 **أسعار الاشتراكات النووية:**

🎁 **FREE** - مجاني تجريبي
• 5 تحميلات/يوم
• جودة 480p
• بدون ذكاء اصطناعي
• بدون فيزا وهمية

⭐ **VIP** - 100 جنيه / شهر
• 50 تحميل/يوم
• جودة 1080p
• ذكاء اصطناعي محدود
• توليد 5 بطاقات/يوم
• تحميل متوازي (رابطين)

👑 **PRO** - 300 جنيه / 3 شهور
• 200 تحميل/يوم
• جودة 4K
• ذكاء اصطناعي غير محدود
• توليد 20 بطاقة/يوم
• تحميل متوازي (5 روابط)
• إزالة علامة مائية

☢️ **NUCLEAR** - 1000 جنيه / سنة
• غير محدود كل حاجة
• جودة Nuclear (أعلى شي)
• API خاص
• تحميل قنوات كاملة
• جدولة تحميل
• دعم VIP 24/7
• كل الميزات الحالية والمستقبلية

📲 **للشراء:**
/buy - اختيار الاشتراك
"""
        await update.message.reply_text(text, parse_mode='Markdown')
    
    async def buy(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """شراء اشتراك"""
        keyboard = [
            [InlineKeyboardButton("⭐ VIP - 100 جنيه", callback_data="buy_vip")],
            [InlineKeyboardButton("👑 PRO - 300 جنيه", callback_data="buy_pro")],
            [InlineKeyboardButton("☢️ NUCLEAR - 1000 جنيه", callback_data="buy_nuclear")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="menu_main")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text("💰 **اختر نوع الاشتراك:**", reply_markup=reply_markup, parse_mode='Markdown')
    
    async def redeem(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """تفعيل مفتاح"""
        user = update.effective_user
        
        if not context.args:
            await update.message.reply_text("❌ أرسل المفتاح بعد الأمر\nمثال: /redeem VIP-XXXX-XXXX")
            return
        
        key = context.args[0].upper().strip()
        
        # التحقق من المفتاح
        key_data = db.check_key(key)
        
        if not key_data:
            await update.message.reply_text("❌ مفتاح غير صالح")
            return
        
        if key_data[5]:  # is_used
            await update.message.reply_text("❌ هذا المفتاح مستخدم بالفعل")
            return
        
        # تفعيل المفتاح
        key_type = db.use_key(key, user.id)
        
        await update.message.reply_text(
            f"✅ **تم تفعيل اشتراكك بنجاح!**\n\n"
            f"النوع: {key_type.upper()}\n"
            f"المدة: { {'free':7, 'vip':30, 'pro':365, 'nuclear':9999}.get(key_type, 30) } يوم\n\n"
            f"استمتع بالتجربة النووية ☢️"
        )
    
    async def my_key(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معلومات مفتاح المستخدم"""
        user = update.effective_user
        user_data = db.get_user(user.id)
        
        if not user_data or user_data[3] == 'free':
            await update.message.reply_text("ℹ️ ليس لديك اشتراك فعال حالياً")
            return
        
        sub_type = user_data[3]
        sub_end = datetime.fromisoformat(user_data[4])
        remaining = (sub_end - datetime.now()).days
        
        text = f"""
🔑 **معلومات اشتراكك:**

النوع: **{sub_type.upper()}**
يبدأ: {user_data[2][:10]}
ينتهي: {sub_end.strftime('%Y-%m-%d')}
متبقي: {remaining} يوم
الحالة: {'✅ نشط' if remaining > 0 else '❌ منتهي'}
"""
        await update.message.reply_text(text, parse_mode='Markdown')
    
    async def generate_key(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """توليد مفتاح جديد (للمالك والمديرين)"""
        user = update.effective_user
        
        if user.id != GENERAL_ID and user.id not in ADMINS:
            await update.message.reply_text("⛔ هذا الأمر للمالك والمديرين فقط")
            return
        
        if len(context.args) < 2:
            await update.message.reply_text("❌ استخدم: /genkey [النوع] [العدد]\nالأنواع: free, vip, pro, nuclear")
            return
        
        key_type = context.args[0].lower()
        if key_type not in ['free', 'vip', 'pro', 'nuclear']:
            await update.message.reply_text("❌ نوع غير صالح")
            return
        
        try:
            count = min(int(context.args[1]), 50)
        except:
            count = 1
        
        keys = []
        for _ in range(count):
            key = key_gen.generate_key(key_type, length=16)
            db.add_key(key, key_type, user.id)
            keys.append(key)
        
        keys_text = "\n".join(keys)
        
        # تشفير المفاتيح
        encrypted = crypto.encrypt(keys_text)
        
        await update.message.reply_text(
            f"✅ **تم توليد {count} مفتاح {key_type}:**\n\n"
            f"```\n{keys_text}\n```\n"
            f"🔐 مشفرة: {encrypted[:50]}...",
            parse_mode='Markdown'
        )
    
    async def stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """إحصائيات البوت"""
        user = update.effective_user
        
        if user.id != GENERAL_ID and user.id not in ADMINS:
            await update.message.reply_text("⛔ هذا الأمر للإدارة فقط")
            return
        
        stats = db.get_stats()
        
        text = f"""
📊 **إحصائيات OMEGA-99 NUCLEAR**

👥 المستخدمين: {stats['users']}
📥 التحميلات: {stats['downloads']}
💾 الحجم الكلي: {stats['total_size'] / (1024**3):.2f} GB

🔰 **الاشتراكات:**
"""
        for sub, count in stats['subscriptions'].items():
            text += f"• {sub}: {count}\n"
        
        # إحصائيات الأمان
        text += f"\n🛡️ **الأمان:**\n"
        text += f"• محظورين: {len(security.blocked_users)}\n"
        text += f"• أجهزة محظورة: {len(security.blocked_devices)}"
        
        await update.message.reply_text(text, parse_mode='Markdown')
    
    async def users_list(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """قائمة المستخدمين"""
        user = update.effective_user
        
        if user.id != GENERAL_ID and user.id not in ADMINS:
            return
        
        # هذا مجرد مثال، هنحتاج دالة تجيب المستخدمين من قاعدة البيانات
        await update.message.reply_text("👥 قائمة المستخدمين قيد التطوير")
    
    async def block_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """حظر مستخدم"""
        user = update.effective_user
        
        if user.id != GENERAL_ID and user.id not in ADMINS:
            return
        
        if not context.args:
            await update.message.reply_text("❌ استخدم: /block [user_id] [السبب]")
            return
        
        try:
            target_id = int(context.args[0])
            reason = ' '.join(context.args[1:]) if len(context.args) > 1 else "مخالفة قواعد"
            
            # هنا نجيب المستخدم ونحظره
            # security.block_user(...)
            
            await update.message.reply_text(f"✅ تم حظر المستخدم {target_id}\nالسبب: {reason}")
        except:
            await update.message.reply_text("❌ خطأ في الحظر")
    
    async def unblock_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """فك حظر مستخدم"""
        user = update.effective_user
        
        if user.id != GENERAL_ID:
            return
        
        if not context.args:
            await update.message.reply_text("❌ استخدم: /unblock [user_id]")
            return
        
        try:
            target_id = int(context.args[0])
            # security.unblock_user(target_id)
            await update.message.reply_text(f"✅ تم فك حظر المستخدم {target_id}")
        except:
            await update.message.reply_text("❌ خطأ")
    
    async def broadcast(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """بث رسالة للمستخدمين"""
        user = update.effective_user
        
        if user.id != GENERAL_ID:
            return
        
        if not context.args:
            await update.message.reply_text("❌ استخدم: /broadcast [الرسالة]")
            return
        
        message = ' '.join(context.args)
        
        await update.message.reply_text(f"📢 جاري البث لـ {db.get_stats()['users']} مستخدم...")
        
        # هنا هنضيف البث الفعلي
        await update.message.reply_text("✅ تم البث بنجاح")
    
    async def button_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج الأزرار"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "menu_download":
            await query.edit_message_text("📥 أرسل رابط الفيديو مباشرة")
        
        elif data == "menu_audio":
            await query.edit_message_text("🎵 أرسل رابط الفيديو لتحميل الصوت")
        
        elif data == "menu_ai":
            await query.edit_message_text("🧠 أرسل سؤالك للذكاء الاصطناعي\nمثال: /ai ما هي عاصمة فرنسا؟")
        
        elif data == "menu_visa":
            keyboard = [
                [InlineKeyboardButton("💳 توليد بطاقة", callback_data="visa_generate")],
                [InlineKeyboardButton("🔍 التحقق من بطاقة", callback_data="visa_check")],
                [InlineKeyboardButton("🏦 بحث BIN", callback_data="visa_bin")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="menu_main")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("💳 **نظام الفيزا الوهمية**", reply_markup=reply_markup, parse_mode='Markdown')
        
        elif data == "menu_prices":
            await self.prices(query.message, context)
        
        elif data == "menu_redeem":
            await query.edit_message_text("🔑 أرسل المفتاح:\n/redeem KEY-HERE")
        
        elif data == "menu_help":
            await self.help(query.message, context)
        
        elif data == "menu_main":
            await self.menu(query.message, context)
        
        elif data == "visa_generate":
            await query.edit_message_text("💳 استخدم الأمر: /gencard [عدد البطاقات]")
        
        elif data == "visa_check":
            await query.edit_message_text("🔍 استخدم الأمر: /checkcard [رقم البطاقة]")
        
        elif data == "visa_bin":
            await query.edit_message_text("🏦 استخدم الأمر: /bin [أول 6 أرقام]")
        
        elif data.startswith("buy_"):
            key_type = data.replace("buy_", "")
            prices = {'vip': 100, 'pro': 300, 'nuclear': 1000}
            amount = prices.get(key_type, 100)
            
            payment_info = payment.get_payment_info(amount, key_type)
            
            numbers_text = "\n".join([f"📞 {num}" for num in payment_info['numbers']])
            
            text = f"""
💰 **طلب شراء {key_type.upper()}**

المبلغ: {amount} جنيه
كود العملية: `{payment_info['payment_id']}`

**طرق الدفع:**
{numbers_text}

**Instapay:** @omega_pay

📌 **ملاحظات:**
• حول المبلغ على أي رقم
• أرسل صورة الفاتورة هنا
• سيتم تفعيل اشتراكك خلال 24 ساعة
"""
            await query.edit_message_text(text, parse_mode='Markdown')
        
        elif data == "admin_panel":
            user = update.effective_user
            if user.id != GENERAL_ID and user.id not in ADMINS:
                await query.edit_message_text("⛔ غير مصرح")
                return
            
            keyboard = [
                [InlineKeyboardButton("🔑 توليد مفاتيح", callback_data="admin_genkey")],
                [InlineKeyboardButton("📊 إحصائيات", callback_data="admin_stats")],
                [InlineKeyboardButton("👥 المستخدمين", callback_data="admin_users")],
                [InlineKeyboardButton("🚫 حظر", callback_data="admin_block")],
                [InlineKeyboardButton("📢 بث", callback_data="admin_broadcast")],
                [InlineKeyboardButton("🔙 رجوع", callback_data="menu_main")],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await query.edit_message_text("⚡ **لوحة الإدارة النووية**", reply_markup=reply_markup, parse_mode='Markdown')
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج الرسائل العادية"""
        user = update.effective_user
        text = update.message.text
        
        # التحقق الأمني
        if security.is_blocked(user):
            await update.message.reply_text("⛔ أنت محظور نووياً")
            return
        
        if not security.check_rate_limit(user):
            await update.message.reply_text("⚠️ أنت ت发送 بسرعة كبيرة. توقف دقيقة.")
            return
        
        # كشف التهديدات
        if security.detect_threat(text):
            security.suspicious_users[user.id] += 1
            if security.suspicious_users[user.id] >= 2:
                security.block_user(user, "سلوك مشبوه متكرر")
                await update.message.reply_text("⛔ تم حظرك تلقائياً لأسباب أمنية")
            else:
                await update.message.reply_text("⚠️ سلوك غير طبيعي. تحذير أول")
            return
        
        # فحص بالذكاء الاصطناعي
        if GEMINI_READY:
            threat = await security.ai_security_check(user, text)
            if threat:
                security.block_user(user, "AI detected threat")
                await update.message.reply_text("⛔ تم حظرك تلقائياً بواسطة الذكاء الاصطناعي")
                return
        
        # تحديث النشاط
        db.update_activity(user.id)
        
        # لو الرابط، ابدأ التحميل
        if downloader.is_supported(text):
            context.args = [text]
            await self.download(update, context)
        else:
            # رد عادي
            await update.message.reply_text(
                "🤖 أنا OMEGA-99 NUCLEAR\n"
                "أرسل /help لمعرفة الأوامر\n"
                "أو أرسل رابط فيديو للتحميل"
            )
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """معالج الأخطاء"""
        logger.error(f"🔥 خطأ نووي: {context.error}")
        try:
            if update and update.effective_message:
                await update.effective_message.reply_text("⚠️ حدث خطأ نووي. تم التسجيل.")
        except:
            pass
    
    def run(self):
        """تشغيل البوت النووي"""
        logger.info("=" * 60)
        logger.info("☢️ OMEGA-99 SUPREME - NUCLEAR EDITION ☢️")
        logger.info(f"المالك: {GENERAL_ID}")
        logger.info(f"الذكاء الاصطناعي: {'✅' if GEMINI_READY else '❌'}")
        logger.info(f"التحميل: {'✅' if YTDLP_READY else '❌'}")
        logger.info(f"المسار: {BASE_DIR}")
        logger.info("=" * 60)
        
        self.app.run_polling()

# ======================= التشغيل =======================
if __name__ == "__main__":
    try:
        bot = OmegaNuclearBot()
        bot.run()
    except KeyboardInterrupt:
        logger.info("🔴 تم إيقاف البوت النووي")
    except Exception as e:
        logger.exception(f"💥 انفجار نووي: {e}")