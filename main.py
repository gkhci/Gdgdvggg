import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import json
import time
import random
from datetime import datetime, timedelta
import threading
import os
import hashlib
import base64
from collections import defaultdict

# ========== تنظیمات ==========
BOT_TOKEN = "8793482183:AAEGUa7ZEURP26N34DzKvrudnndC3q7apBk"
ADMIN_IDS = [8680457924]
bot = telebot.TeleBot(BOT_TOKEN)

# ========== دیتابیس پیشرفته ==========
class AdvancedDatabase:
    def __init__(self):
        self.users = {}
        self.inbounds = {}
        self.servers = {}
        self.transactions = []
        self.tickets = []
        self.backups = []
        self.settings = {
            "panel_name": "X-Panel Ultra",
            "version": "5.0.0",
            "uptime": time.time(),
            "maintenance": False,
            "default_traffic": 100,
            "default_expiry": 30,
            "currency": "تومان",
            "price_per_gb": 5000,
            "referral_bonus": 10,
            "auto_backup": True
        }
        self._init_sample_data()
    
    def _init_sample_data(self):
        # اینباندهای پیشرفته
        sample_inbounds = [
            {"id": "1", "name": "VLESS-USA-Premium", "traffic_limit": 200, "traffic_used": 45.5, "status": "فعال", 
             "expiry": "2027-01-15", "protocol": "vless", "network": "ws", "server": "US-01", "speed": "1Gbps", 
             "location": "آمریکا", "ping": 150, "users": 12, "created": "2026-01-01"},
            {"id": "2", "name": "VLESS-GERMANY", "traffic_limit": 150, "traffic_used": 78.2, "status": "فعال", 
             "expiry": "2026-12-20", "protocol": "vless", "network": "grpc", "server": "DE-02", "speed": "500Mbps", 
             "location": "آلمان", "ping": 80, "users": 8, "created": "2026-02-15"},
            {"id": "3", "name": "VLESS-SINGAPORE", "traffic_limit": 180, "traffic_used": 23.8, "status": "فعال", 
             "expiry": "2027-02-28", "protocol": "vless", "network": "ws", "server": "SG-03", "speed": "2Gbps", 
             "location": "سنگاپور", "ping": 60, "users": 15, "created": "2026-03-10"},
            {"id": "4", "name": "TROJAN-JAPAN", "traffic_limit": 100, "traffic_used": 5.3, "status": "غیرفعال", 
             "expiry": "2026-10-10", "protocol": "trojan", "network": "tcp", "server": "JP-04", "speed": "300Mbps", 
             "location": "ژاپن", "ping": 120, "users": 3, "created": "2026-04-20"},
            {"id": "5", "name": "VMESS-UK-Premium", "traffic_limit": 250, "traffic_used": 120.7, "status": "فعال", 
             "expiry": "2027-03-01", "protocol": "vmess", "network": "ws", "server": "UK-05", "speed": "1.5Gbps", 
             "location": "انگلیس", "ping": 90, "users": 20, "created": "2026-05-05"},
            {"id": "6", "name": "VLESS-FRANCE", "traffic_limit": 130, "traffic_used": 8.1, "status": "فعال", 
             "expiry": "2027-01-30", "protocol": "vless", "network": "grpc", "server": "FR-06", "speed": "400Mbps", 
             "location": "فرانسه", "ping": 95, "users": 5, "created": "2026-06-12"},
        ]
        for inbound in sample_inbounds:
            self.inbounds[inbound["id"]] = inbound
        
        # سرورها
        self.servers = {
            "US-01": {"name": "آمریکا شمالی", "ip": "45.33.22.11", "status": "آنلاین", "load": 45},
            "DE-02": {"name": "آلمان مرکزی", "ip": "89.45.67.12", "status": "آنلاین", "load": 30},
            "SG-03": {"name": "سنگاپور", "ip": "182.55.66.13", "status": "آنلاین", "load": 60},
            "JP-04": {"name": "ژاپن", "ip": "133.44.55.14", "status": "آفلاین", "load": 0},
            "UK-05": {"name": "انگلیس", "ip": "78.33.44.15", "status": "آنلاین", "load": 70},
            "FR-06": {"name": "فرانسه", "ip": "91.22.33.16", "status": "آنلاین", "load": 25},
        }
    
    def add_user(self, user_id, name, username=None):
        if user_id not in self.users:
            self.users[user_id] = {
                "name": name,
                "username": username,
                "role": "admin" if user_id in ADMIN_IDS else "user",
                "joined": datetime.now().isoformat(),
                "last_seen": datetime.now().isoformat(),
                "traffic_used": 0,
                "traffic_limit": self.settings["default_traffic"],
                "expiry": (datetime.now() + timedelta(days=self.settings["default_expiry"])).isoformat(),
                "status": "active",
                "referral_code": hashlib.md5(str(user_id).encode()).hexdigest()[:8],
                "referred_by": None,
                "credits": 0,
                "warnings": 0,
                "notes": ""
            }
            return True
        return False
    
    def get_user(self, user_id):
        return self.users.get(user_id)
    
    def get_stats(self):
        total_users = len(self.users)
        active_users = len([u for u in self.users.values() if u.get("status") == "active"])
        total_inbounds = len(self.inbounds)
        active_inbounds = len([i for i in self.inbounds.values() if i["status"] == "فعال"])
        total_traffic = sum(i["traffic_used"] for i in self.inbounds.values())
        total_transactions = len(self.transactions)
        total_tickets = len(self.tickets)
        
        online_servers = len([s for s in self.servers.values() if s["status"] == "آنلاین"])
        total_servers = len(self.servers)
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "total_inbounds": total_inbounds,
            "active_inbounds": active_inbounds,
            "total_traffic": total_traffic,
            "total_transactions": total_transactions,
            "total_tickets": total_tickets,
            "online_servers": online_servers,
            "total_servers": total_servers,
            "cpu": random.randint(10, 60),
            "memory": random.randint(30, 80),
            "uptime": self.get_uptime(),
            "domain": "panel.x-panel.com",
            "version": self.settings["version"],
            "maintenance": self.settings["maintenance"]
        }
    
    def get_uptime(self):
        seconds = int(time.time() - self.settings["uptime"])
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60
        return f"{days}d {hours}h {minutes}m"
    
    def create_inbound(self, name, traffic_limit, max_ips, days, protocol=None, network=None, server=None):
        inbound_id = str(int(time.time()))
        expiry = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
        
        if not protocol:
            protocol = random.choice(["vless", "vmess", "trojan"])
        if not network:
            network = random.choice(["ws", "grpc", "tcp"])
        if not server:
            server = random.choice(list(self.servers.keys()))
        
        inbound = {
            "id": inbound_id,
            "name": name,
            "traffic_limit": traffic_limit,
            "traffic_used": 0,
            "max_ips": max_ips,
            "status": "فعال",
            "expiry": expiry,
            "protocol": protocol,
            "network": network,
            "server": server,
            "created": datetime.now().isoformat(),
            "users": 0,
            "speed": random.choice(["500Mbps", "1Gbps", "2Gbps"]),
            "location": self.servers.get(server, {}).get("name", "نامشخص"),
            "ping": random.randint(50, 200)
        }
        self.inbounds[inbound_id] = inbound
        return inbound
    
    def delete_inbound(self, inbound_id):
        if inbound_id in self.inbounds:
            del self.inbounds[inbound_id]
            return True
        return False
    
    def get_inbound_link(self, inbound_id):
        inbound = self.inbounds.get(inbound_id)
        if not inbound:
            return None
        domain = "web-production-1ca13.up.railway.app"
        port = 443
        path = f"/ws/{inbound_id}"
        uuid = f"{random.randint(10000000, 99999999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(10000000, 99999999)}"
        
        if inbound['protocol'] == "vless":
            return f"vless://{uuid}@{domain}:{port}?encryption=none&security=tls&type=ws&host={domain}&path={path}&sni={domain}&fp=chrome&alpn=http/1.1#{inbound['name']}"
        elif inbound['protocol'] == "vmess":
            return f"vmess://{uuid}@{domain}:{port}?security=tls&type=ws&host={domain}&path={path}&sni={domain}&fp=chrome&alpn=http/1.1#{inbound['name']}"
        else:
            return f"trojan://{uuid}@{domain}:{port}?security=tls&type=ws&host={domain}&path={path}&sni={domain}&fp=chrome&alpn=http/1.1#{inbound['name']}"
    
    def get_server_stats(self):
        stats = {}
        for server_id, server in self.servers.items():
            inbounds_on_server = [i for i in self.inbounds.values() if i.get("server") == server_id]
            stats[server_id] = {
                **server,
                "inbounds_count": len(inbounds_on_server),
                "total_traffic": sum(i["traffic_used"] for i in inbounds_on_server)
            }
        return stats

db = AdvancedDatabase()

# ========== تولید کانفیگ پیشرفته ==========
def generate_advanced_config(inbound_name, inbound_id, protocol=None):
    domain = "web-production-1ca13.up.railway.app"
    port = 443
    path = f"/ws/{inbound_id}"
    uuid = f"{random.randint(10000000, 99999999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(10000000, 99999999)}"
    
    if not protocol:
        protocol = random.choice(["vless", "vmess", "trojan"])
    
    configs = {
        "vless": f"vless://{uuid}@{domain}:{port}?encryption=none&security=tls&type=ws&host={domain}&path={path}&sni={domain}&fp=chrome&alpn=http/1.1#{inbound_name}",
        "vmess": f"vmess://{uuid}@{domain}:{port}?security=tls&type=ws&host={domain}&path={path}&sni={domain}&fp=chrome&alpn=http/1.1#{inbound_name}",
        "trojan": f"trojan://{uuid}@{domain}:{port}?security=tls&type=ws&host={domain}&path={path}&sni={domain}&fp=chrome&alpn=http/1.1#{inbound_name}"
    }
    
    return configs

# ========== کیبوردهای پیشرفته ==========
def ultra_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("📊 داشبورد", callback_data="ultra_dashboard"),
        InlineKeyboardButton("📋 اینباندها", callback_data="ultra_inbounds"),
        InlineKeyboardButton("➕ افزودن", callback_data="ultra_add"),
        InlineKeyboardButton("🗄️ سرورها", callback_data="ultra_servers"),
        InlineKeyboardButton("📈 ترافیک", callback_data="ultra_traffic"),
        InlineKeyboardButton("📱 کانفیگ", callback_data="ultra_config"),
        InlineKeyboardButton("💰 مالی", callback_data="ultra_finance"),
        InlineKeyboardButton("🎫 تیکت‌ها", callback_data="ultra_tickets"),
        InlineKeyboardButton("👥 کاربران", callback_data="ultra_users"),
        InlineKeyboardButton("⚙️ تنظیمات", callback_data="ultra_settings"),
        InlineKeyboardButton("🔄 بروزرسانی", callback_data="ultra_refresh"),
        InlineKeyboardButton("🆘 راهنما", callback_data="ultra_help")
    )
    return keyboard

def inbound_detail_keyboard(inbound_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🔗 کانفیگ", callback_data=f"ultra_link_{inbound_id}"),
        InlineKeyboardButton("📊 مصرف", callback_data=f"ultra_usage_{inbound_id}"),
        InlineKeyboardButton("⏸️ تغییر وضعیت", callback_data=f"ultra_toggle_{inbound_id}"),
        InlineKeyboardButton("🗑️ حذف", callback_data=f"ultra_delete_{inbound_id}")
    )
    keyboard.add(InlineKeyboardButton("🔙 بازگشت", callback_data="ultra_inbounds"))
    return keyboard

# ========== دستور /start ==========
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    username = message.from_user.username
    
    if db.add_user(user_id, name, username):
        bot.send_message(
            message.chat.id,
            f"🌟 **به پنل X-Panel Ultra خوش آمدید!**\n\n"
            f"👤 کاربر: {name}\n"
            f"🆔 آیدی: {user_id}\n"
            f"👑 نقش: {'ادمین' if user_id in ADMIN_IDS else 'کاربر'}\n"
            f"🔑 کد معرف: `{db.users[user_id]['referral_code']}`\n\n"
            f"📌 از دکمه‌های زیر برای مدیریت استفاده کنید:",
            reply_markup=ultra_menu(),
            parse_mode='Markdown'
        )
    else:
        bot.send_message(
            message.chat.id,
            "👋 **خوش برگشتی!**",
            reply_markup=ultra_menu()
        )

# ========== مدیریت کامل دکمه‌ها ==========
@bot.callback_query_handler(func=lambda call: True)
def ultra_callback_handler(call):
    user_id = call.from_user.id
    
    # ===== داشبورد فوق پیشرفته =====
    if call.data == "ultra_dashboard":
        stats = db.get_stats()
        server_stats = db.get_server_stats()
        
        text = f"""
📊 **داشبورد X-Panel Ultra v{stats['version']}**

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🖥️ **وضعیت سیستم:**
• CPU: `{stats['cpu']}%` {"🟢" if stats['cpu'] < 50 else "🟡" if stats['cpu'] < 70 else "🔴"}
• Memory: `{stats['memory']}%` {"🟢" if stats['memory'] < 50 else "🟡" if stats['memory'] < 70 else "🔴"}
• Uptime: `{stats['uptime']}`
• وضعیت: {"🔧 تعمیرات" if stats['maintenance'] else "🟢 آنلاین"}

📊 **آمار کلی:**
• 👥 کاربران: `{stats['total_users']}`
• ✅ فعال: `{stats['active_users']}`
• 📋 اینباندها: `{stats['total_inbounds']}`
• 🟢 اینباند فعال: `{stats['active_inbounds']}`
• 📦 ترافیک کل: `{stats['total_traffic']:.1f} GB`
• 🗄️ سرورها: `{stats['online_servers']}/{stats['total_servers']} آنلاین`
• 💰 تراکنش‌ها: `{stats['total_transactions']}`
• 🎫 تیکت‌ها: `{stats['total_tickets']}`

🌐 **دامنه:** `{stats['domain']}`

📌 **پنل:** {'✅ فعال' if not stats['maintenance'] else '⛔ غیرفعال'}
"""
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=ultra_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "✅ داشبورد بروز شد")
    
    # ===== لیست اینباندها =====
    elif call.data == "ultra_inbounds":
        show_ultra_inbounds(call)
    
    # ===== افزودن اینباند =====
    elif call.data == "ultra_add":
        bot.answer_callback_query(call.id, "📝 فرم افزودن اینباند")
        bot.edit_message_text(
            "📝 **افزودن اینباند پیشرفته**\n\n"
            "📌 **فرمت ساده:**\n"
            "`/add [نام] [ترافیک_GB] [IP] [روز]`\n\n"
            "📌 **فرمت پیشرفته:**\n"
            "`/add_pro [نام] [ترافیک_GB] [IP] [روز] [پروتکل] [شبکه] [سرور]`\n\n"
            "📌 **پروتکل‌ها:** vless, vmess, trojan\n"
            "📌 **شبکه‌ها:** ws, grpc, tcp\n"
            "📌 **سرورها:** US-01, DE-02, SG-03, JP-04, UK-05, FR-06\n\n"
            "مثال پیشرفته:\n"
            "`/add_pro Premium-US 200 5 30 vless ws US-01`",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=ultra_menu(),
            parse_mode='Markdown'
        )
    
    # ===== سرورها =====
    elif call.data == "ultra_servers":
        server_stats = db.get_server_stats()
        text = "🗄️ **وضعیت سرورها:**\n\n"
        
        for server_id, server in server_stats.items():
            status_emoji = "🟢" if server["status"] == "آنلاین" else "🔴"
            load_bar = "█" * int(server["load"] / 10) + "░" * (10 - int(server["load"] / 10))
            text += f"{status_emoji} **{server['name']}**\n"
            text += f"📌 آیدی: `{server_id}`\n"
            text += f"📊 بار: `{server['load']}%` {load_bar}\n"
            text += f"📋 اینباندها: `{server['inbounds_count']}`\n"
            text += f"📦 ترافیک: `{server['total_traffic']:.1f} GB`\n"
            text += f"🌐 IP: `{server['ip']}`\n\n"
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=ultra_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "🗄️ وضعیت سرورها")
    
    # ===== ترافیک پیشرفته =====
    elif call.data == "ultra_traffic":
        stats = db.get_stats()
        text = f"""
📈 **آمار ترافیک پیشرفته**

📦 ترافیک کل: `{stats['total_traffic']:.1f} GB`

📊 **مصرف اینباندها:**

"""
        sorted_inbounds = sorted(db.inbounds.values(), key=lambda x: x['traffic_used'], reverse=True)
        for item in sorted_inbounds[:10]:
            usage_percent = (item['traffic_used'] / item['traffic_limit']) * 100 if item['traffic_limit'] > 0 else 0
            bar = "█" * int(usage_percent / 10) + "░" * (10 - int(usage_percent / 10))
            status = "🟢" if item['status'] == "فعال" else "🔴"
            text += f"{status} {item['name']}: `{item['traffic_used']:.1f}/{item['traffic_limit']} GB`\n"
            text += f"  `{bar}` {usage_percent:.0f}%\n"
        
        text += f"\n📌 {len(db.inbounds)} اینباند در سیستم وجود دارد."
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=ultra_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "📊 آمار ترافیک")
    
    # ===== کانفیگ =====
    elif call.data == "ultra_config":
        inbounds = list(db.inbounds.values())
        if not inbounds:
            bot.answer_callback_query(call.id, "❌ هیچ اینباندی یافت نشد")
            return
        
        inbound = random.choice(inbounds)
        configs = generate_advanced_config(inbound['name'], inbound['id'])
        
        text = f"""
🔐 **کانفیگ‌های {inbound['name']}**

📛 نام: {inbound['name']}
🆔 شناسه: {inbound['id']}
📌 وضعیت: {inbound['status']}
🗄️ سرور: {inbound['server']}
🌍 موقعیت: {inbound['location']}
📊 سرعت: {inbound['speed']}
⚡ پینگ: {inbound['ping']}ms

📌 **VLESS:**
`{configs['vless']}`

📌 **VMESS:**
`{configs['vmess']}`

📌 **Trojan:**
`{configs['trojan']}`

📥 هر کدوم رو که می‌خوای کپی کن!
"""
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=ultra_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "🔗 کانفیگ‌ها")
    
    # ===== مالی =====
    elif call.data == "ultra_finance":
        text = f"""
💰 **سیستم مالی X-Panel**

💵 **واحد پول:** {db.settings['currency']}
💲 **قیمت هر GB:** {db.settings['price_per_gb']:,} {db.settings['currency']}
🎁 **پاداش معرف:** {db.settings['referral_bonus']}%

📊 **آمار مالی:**
• کل تراکنش‌ها: `{len(db.transactions)}`
• اعتبار شما: `{db.users.get(user_id, {}).get('credits', 0):,} {db.settings['currency']}`

📌 **دستورات مالی:**
/credit - مشاهده اعتبار
/add_credit [مبلغ] - شارژ حساب (فقط ادمین)
/pay [مبلغ] - پرداخت
"""
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=ultra_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "💰 سیستم مالی")
    
    # ===== تیکت‌ها =====
    elif call.data == "ultra_tickets":
        text = """
🎫 **سیستم تیکت‌ها**

📌 **دستورات تیکت:**
/ticket [موضوع] - ایجاد تیکت جدید
/tickets - مشاهده تیکت‌های من
/reply [تیکت‌ID] [پاسخ] - پاسخ به تیکت
/close [تیکت‌ID] - بستن تیکت

📊 **وضعیت:** 🟢 فعال
"""
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=ultra_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "🎫 سیستم تیکت‌ها")
            # ===== کاربران =====
    elif call.data == "ultra_users":
        if user_id not in ADMIN_IDS:
            bot.answer_callback_query(call.id, "⛔ فقط ادمین!")
            return
        
        users = db.users
        if not users:
            bot.edit_message_text(
                "📭 هیچ کاربری یافت نشد",
                call.message.chat.id,
                call.message.message_id,
                reply_markup=ultra_menu()
            )
            return
        
        text = "👥 **لیست کاربران:**\n\n"
        for user_id, user in list(users.items())[:15]:
            text += f"• {user['name']} (@{user.get('username', 'ندارد')})\n"
            text += f"  🆔 {user_id} | {user['role']} | {user['status']}\n"
        
        text += f"\n📌 مجموع: {len(users)} کاربر"
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=ultra_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "👥 لیست کاربران")
    
    # ===== تنظیمات =====
    elif call.data == "ultra_settings":
        stats = db.get_stats()
        text = f"""
⚙️ **تنظیمات پنل Ultra**

🔹 نام پنل: X-Panel Ultra
🔹 نسخه: {stats['version']}
🔹 وضعیت: {'🟢 آنلاین' if not stats['maintenance'] else '🔧 تعمیرات'}

⚡ **تنظیمات:**
• ترافیک پیش‌فرض: `{db.settings['default_traffic']} GB`
• انقضای پیش‌فرض: `{db.settings['default_expiry']} روز`
• ارز: `{db.settings['currency']}`
• قیمت هر GB: `{db.settings['price_per_gb']:,} {db.settings['currency']}`
• پاداش معرف: `{db.settings['referral_bonus']}%`

🛠️ **ابزارها:**
• آپتایم: `{stats['uptime']}`
• CPU: `{stats['cpu']}%`
• RAM: `{stats['memory']}%`

📌 برای تغییر تنظیمات با ادمین تماس بگیرید.
"""
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=ultra_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "⚙️ تنظیمات")
    
    # ===== Refresh =====
    elif call.data == "ultra_refresh":
        stats = db.get_stats()
        bot.answer_callback_query(call.id, "🔄 بروزرسانی شد")
        text = f"""
✅ **پنل بروزرسانی شد!**

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📊 اینباندها: {stats['total_inbounds']}
👥 کاربران: {stats['total_users']}
📦 ترافیک: {stats['total_traffic']:.1f} GB
🗄️ سرورها: {stats['online_servers']}/{stats['total_servers']}
"""
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=ultra_menu(),
            parse_mode='Markdown'
        )
    
    # ===== Help =====
    elif call.data == "ultra_help":
        text = """
🆘 **راهنمای کامل Ultra Panel**

📌 **دستورات اصلی:**
/start - منوی اصلی
/add [نام] [ترافیک] [IP] [روز] - افزودن اینباند
/add_pro [نام] [ترافیک] [IP] [روز] [پروتکل] [شبکه] [سرور] - افزودن پیشرفته
/stats - آمار پنل
/list - لیست اینباندها
/status - وضعیت سیستم
/help - این راهنما

📌 **دستورات کاربری:**
/profile - پروفایل من
/config - کانفیگ من
/credit - اعتبار من
/ticket [موضوع] - تیکت جدید

📌 **دستورات ادمین:**
/users - لیست کاربران
/reset_traffic - ریست ترافیک
/add_sample - افزودن نمونه
/backup - بکاپ
/set_config [key] [value] - تغییر تنظیمات

📌 **دکمه‌های اصلی:**
📊 داشبورد - آمار کامل
📋 اینباندها - مدیریت
➕ افزودن - اینباند جدید
🗄️ سرورها - وضعیت سرورها
📈 ترافیک - آمار مصرف
📱 کانفیگ - دریافت کانفیگ
💰 مالی - سیستم مالی
🎫 تیکت‌ها - پشتیبانی
👥 کاربران - مدیریت کاربران
⚙️ تنظیمات - تنظیمات پنل

📌 **پشتیبانی:** @XPanelSupport
"""
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=ultra_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "🆘 راهنما")
    
    # ===== عملیات اینباندها =====
    elif call.data.startswith("ultra_link_"):
        inbound_id = call.data.split("_")[2]
        inbound = db.inbounds.get(inbound_id)
        if inbound:
            configs = generate_advanced_config(inbound['name'], inbound_id)
            bot.answer_callback_query(call.id, "🔗 کانفیگ‌ها ارسال شد")
            text = f"""
🔗 **کانفیگ‌های {inbound['name']}**

**VLESS:**
`{configs['vless']}`

**VMESS:**
`{configs['vmess']}`

**Trojan:**
`{configs['trojan']}`
"""
            bot.send_message(
                call.message.chat.id,
                text,
                parse_mode='Markdown'
            )
        else:
            bot.answer_callback_query(call.id, "❌ اینباند یافت نشد")
    
    elif call.data.startswith("ultra_usage_"):
        inbound_id = call.data.split("_")[2]
        inbound = db.inbounds.get(inbound_id)
        if inbound:
            usage_percent = (inbound['traffic_used'] / inbound['traffic_limit']) * 100 if inbound['traffic_limit'] > 0 else 0
            bar = "█" * int(usage_percent / 10) + "░" * (10 - int(usage_percent / 10))
            text = f"""
📊 **آمار مصرف {inbound['name']}**

📦 مصرف: `{inbound['traffic_used']:.1f} / {inbound['traffic_limit']} GB`
📊 درصد: `{usage_percent:.1f}%`
{bar}

📅 انقضا: `{inbound['expiry']}`
📌 وضعیت: `{inbound['status']}`
🗄️ سرور: `{inbound['server']}`
🌍 موقعیت: `{inbound['location']}`
⚡ پینگ: `{inbound['ping']}ms`
📊 سرعت: `{inbound['speed']}`
👥 کاربران: `{inbound['users']}`
"""
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=inbound_detail_keyboard(inbound_id),
                parse_mode='Markdown'
            )
        else:
            bot.answer_callback_query(call.id, "❌ اینباند یافت نشد")
    
    elif call.data.startswith("ultra_toggle_"):
        inbound_id = call.data.split("_")[2]
        inbound = db.inbounds.get(inbound_id)
        if inbound:
            inbound["status"] = "غیرفعال" if inbound["status"] == "فعال" else "فعال"
            bot.answer_callback_query(call.id, f"⏸️ اینباند {inbound['status']} شد")
            show_ultra_inbounds(call)
        else:
            bot.answer_callback_query(call.id, "❌ اینباند یافت نشد")
    
    elif call.data.startswith("ultra_delete_"):
        inbound_id = call.data.split("_")[2]
        if db.delete_inbound(inbound_id):
            bot.answer_callback_query(call.id, "🗑️ اینباند حذف شد")
            show_ultra_inbounds(call)
        else:
            bot.answer_callback_query(call.id, "❌ خطا در حذف")

def show_ultra_inbounds(call):
    inbounds = list(db.inbounds.values())
    
    if not inbounds:
        bot.edit_message_text(
            "📭 **هیچ اینباندی یافت نشد**\n\n"
            "برای افزودن، از دکمه ➕ استفاده کنید.",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=ultra_menu(),
            parse_mode='Markdown'
        )
        return
    
    text = "📋 **لیست اینباندها:**\n\n"
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    for item in inbounds[:15]:
        status_emoji = "🟢" if item['status'] == "فعال" else "🔴"
        usage_percent = (item['traffic_used'] / item['traffic_limit']) * 100 if item['traffic_limit'] > 0 else 0
        bar = "█" * int(usage_percent / 10) + "░" * (10 - int(usage_percent / 10))
        
        text += f"{status_emoji} **{item['name']}**\n"
        text += f"📊 `{item['traffic_used']:.1f}/{item['traffic_limit']} GB` {bar}\n"
        text += f"📅 انقضا: `{item['expiry']}` | 🔗 {item['protocol']}\n"
        text += f"🗄️ {item['server']} | 🌍 {item['location']} | ⚡ {item['ping']}ms\n"
        text += f"🆔 {item['id']}\n\n"
        
        if item['id']:
            keyboard.add(
                InlineKeyboardButton(f"📊 {item['name']}", callback_data=f"ultra_usage_{item['id']}"),
                InlineKeyboardButton(f"🔗 کانفیگ", callback_data=f"ultra_link_{item['id']}"),
                InlineKeyboardButton(f"⏸️ {item['status']}", callback_data=f"ultra_toggle_{item['id']}"),
                InlineKeyboardButton(f"🗑️ حذف", callback_data=f"ultra_delete_{item['id']}")
            )
    
    keyboard.add(InlineKeyboardButton("➕ افزودن جدید", callback_data="ultra_add"))
    keyboard.add(InlineKeyboardButton("🔙 بازگشت", callback_data="ultra_dashboard"))
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard,
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id, "📋 لیست اینباندها")

# ========== دستورات پیشرفته ==========
@bot.message_handler(commands=['add_pro'])
def add_pro_command(message):
    user_id = message.from_user.id
    args = message.text.split()
    
    if len(args) != 8:
        bot.reply_to(
            message,
            "⚠️ **فرمت پیشرفته:**\n"
            "`/add_pro [نام] [ترافیک_GB] [IP] [روز] [پروتکل] [شبکه] [سرور]`\n\n"
            "📌 **پروتکل‌ها:** vless, vmess, trojan\n"
            "📌 **شبکه‌ها:** ws, grpc, tcp\n"
            "📌 **سرورها:** US-01, DE-02, SG-03, JP-04, UK-05, FR-06\n\n"
            "مثال:\n"
            "`/add_pro Premium-US 200 5 30 vless ws US-01`",
            parse_mode='Markdown'
        )
        return
    
    try:
        _, name, traffic, max_ips, days, protocol, network, server = args
        traffic = float(traffic)
        max_ips = int(max_ips)
        days = int(days)
        
        if traffic <= 0 or max_ips <= 0 or days <= 0:
            bot.reply_to(message, "❌ همه مقادیر باید مثبت باشند")
            return
        
        if protocol not in ["vless", "vmess", "trojan"]:
            bot.reply_to(message, "❌ پروتکل نامعتبر! (vless, vmess, trojan)")
            return
        
        if network not in ["ws", "grpc", "tcp"]:
            bot.reply_to(message, "❌ شبکه نامعتبر! (ws, grpc, tcp)")
            return
        
        if server not in db.servers:
            bot.reply_to(message, f"❌ سرور نامعتبر! سرورهای موجود: {', '.join(db.servers.keys())}")
            return
        
        bot.reply_to(message, "⏳ در حال ساخت اینباند پیشرفته...")
        inbound = db.create_inbound(name, traffic, max_ips, days, protocol, network, server)
        
        configs = generate_advanced_config(inbound['name'], inbound['id'], protocol)
        
        text = f"""
✅ **اینباند پیشرفته ساخته شد!**

📛 نام: {inbound['name']}
📊 ترافیک: {inbound['traffic_limit']} GB
👥 حداکثر IP: {inbound['max_ips']}
📅 انقضا: {inbound['expiry']}
🔌 پروتکل: {inbound['protocol']}
🌐 شبکه: {inbound['network']}
🗄️ سرور: {inbound['server']} ({inbound['location']})
⚡ پینگ: {inbound['ping']}ms
📊 سرعت: {inbound['speed']}
🆔 شناسه: {inbound['id']}

📌 **کانفیگ {protocol}:**
`{configs[protocol]}`
"""
        bot.reply_to(message, text, parse_mode='Markdown')
        
    except ValueError:
        bot.reply_to(message, "❌ مقادیر عددی را درست وارد کنید")
    except Exception as e:
        bot.reply_to(message, f"❌ خطا: {str(e)}")

# ========== سایر دستورات ==========
@bot.message_handler(commands=['add'])
def add_command(message):
    args = message.text.split()
    if len(args) != 5:
        bot.reply_to(
            message,
            "⚠️ **فرمت ساده:**\n"
            "`/add [نام] [ترافیک_GB] [حداکثر_IP] [روز_اعتبار]`\n\n"
            "مثال:\n"
            "`/add ایران-تهران 150 5 30`\n\n"
            "📌 برای تنظیمات پیشرفته از `/add_pro` استفاده کنید.",
            parse_mode='Markdown'
        )
        return
    
    try:
        _, name, traffic, max_ips, days = args
        traffic = float(traffic)
        max_ips = int(max_ips)
        days = int(days)
        
        if traffic <= 0 or max_ips <= 0 or days <= 0:
            bot.reply_to(message, "❌ همه مقادیر باید مثبت باشند")
            return
        
        bot.reply_to(message, "⏳ در حال ساخت اینباند...")
        inbound = db.create_inbound(name, traffic, max_ips, days)
        
        configs = generate_advanced_config(inbound['name'], inbound['id'])
        
        text = f"""
✅ **اینباند ساخته شد!**

📛 نام: {inbound['name']}
📊 ترافیک: {inbound['traffic_limit']} GB
👥 حداکثر IP: {inbound['max_ips']}
📅 انقضا: {inbound['expiry']}
🔌 پروتکل: {inbound['protocol']}
🌐 شبکه: {inbound['network']}
🗄️ سرور: {inbound['server']}
🆔 شناسه: {inbound['id']}

📌 **کانفیگ VLESS:**
`{configs['vless']}`
"""
        bot.reply_to(message, text, parse_mode='Markdown')
        
    except ValueError:
        bot.reply_to(message, "❌ مقادیر عددی را درست وارد کنید")
    except Exception as e:
        bot.reply_to(message, f"❌ خطا: {str(e)}")

@bot.message_handler(commands=['profile'])
def profile_command(message):
    user_id = message.from_user.id
    user = db.get_user(user_id)
    if not user:
        bot.reply_to(message, "❌ کاربر یافت نشد!")
        return
    
    text = f"""
👤 **پروفایل کاربری**

📛 نام: {user['name']}
🆔 آیدی: {user_id}
👑 نقش: {user['role']}
📅 تاریخ عضویت: {user['joined']}
🔑 کد معرف: `{user['referral_code']}`

📊 **آمار:**
• ترافیک مصرفی: `{user.get('traffic_used', 0):.1f} GB`
• محدودیت: `{user.get('traffic_limit', 0)} GB`
• اعتبار: `{user.get('credits', 0):,} {db.settings['currency']}`
• وضعیت: {'✅ فعال' if user.get('status') == 'active' else '⛔ غیرفعال'}

📌 تعداد اینباندها: `{len(db.inbounds)}`
"""
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['credit'])
def credit_command(message):
    user_id = message.from_user.id
    user = db.get_user(user_id)
    if not user:
        bot.reply_to(message, "❌ کاربر یافت نشد!")
        return
    
    text = f"""
💰 **اعتبار شما**

💵 اعتبار فعلی: `{user.get('credits', 0):,} {db.settings['currency']}`
💲 قیمت هر GB: `{db.settings['price_per_gb']:,} {db.settings['currency']}`
🎁 پاداش معرف: `{db.settings['referral_bonus']}%`

📌 **دستورات:**
/credit - مشاهده اعتبار
/add_credit [مبلغ] - شارژ (فقط ادمین)

📊 ترافیک قابل خرید: `{user.get('credits', 0) / db.settings['price_per_gb']:.1f} GB`
"""
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['stats'])
def stats_command(message):
    stats = db.get_stats()
    text = f"""
📊 **آمار پنل Ultra**

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🖥️ **سیستم:**
• CPU: `{stats['cpu']}%`
• Memory: `{stats['memory']}%`
• Uptime: `{stats['uptime']}`

📊 **آمار:**
• 👥 کاربران: `{stats['total_users']}`
• ✅ فعال: `{stats['active_users']}`
• 📋 اینباندها: `{stats['total_inbounds']}`
• 🟢 فعال: `{stats['active_inbounds']}`
• 📦 ترافیک کل: `{stats['total_traffic']:.1f} GB`
• 🗄️ سرورها: `{stats['online_servers']}/{stats['total_servers']}`

🌐 دامنه: `{stats['domain']}`
📌 نسخه: `{stats['version']}`
"""
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['list'])
def list_command(message):
    inbounds = list(db.inbounds.values())
    if not inbounds:
        bot.reply_to(message, "📭 هیچ اینباندی یافت نشد")
        return
    
    text = "📋 **لیست اینباندها:**\n\n"
    for item in inbounds[:10]:
        status = "🟢" if item['status'] == "فعال" else "🔴"
        text += f"{status} {item['name']}: `{item['traffic_used']:.1f}/{item['traffic_limit']} GB`\n"
        text += f"  🗄️ {item['server']} | 🌍 {item['location']} | ⚡ {item['ping']}ms\n"
    
    text += f"\n📌 {len(inbounds)} اینباند در سیستم وجود دارد."
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['status'])
def status_command(message):
    stats = db.get_stats()
    text = f"""
🟢 **وضعیت سیستم**

✅ **در حال اجرا**
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 **آمار:**
• 👥 کاربران: `{stats['total_users']}`
• 📋 اینباندها: `{stats['total_inbounds']}`
• 📦 ترافیک: `{stats['total_traffic']:.1f} GB`
• ⏱ آپتایم: `{stats['uptime']}`
• 🗄️ سرورها: `{stats['online_servers']}/{stats['total_servers']}`

🖥️ **سیستم:**
• CPU: `{stats['cpu']}%`
• RAM: `{stats['memory']}%`

📌 **وضعیت:** 🟢 پایدار
"""
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['ping'])
def ping_command(message):
    start_time = time.time()
    bot.send_chat_action(message.chat.id, 'typing')
    end_time = time.time()
    ping = (end_time - start_time) * 1000
    bot.reply_to(message, f"🏓 **Pong!**\n⏱ زمان پاسخ: `{ping:.0f} ms`", parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def help_command(message):
    text = """
📚 **راهنمای کامل X-Panel Ultra**

**دستورات اصلی:**
/start - منوی اصلی
/add [نام] [ترافیک] [IP] [روز] - افزودن اینباند
/add_pro - افزودن اینباند پیشرفته
/stats - آمار پنل
/list - لیست اینباندها
/status - وضعیت سیستم
/help - این راهنما

**دستورات کاربری:**
/profile - پروفایل من
/credit - اعتبار من

**دستورات ادمین:**
/users - لیست کاربران
/add_credit [مبلغ] - شارژ کاربر
/reset_traffic - ریست ترافیک
/add_sample - افزودن نمونه
/backup - بکاپ

**دکمه‌های اصلی:**
📊 داشبورد - آمار کامل
📋 اینباندها - مدیریت
➕ افزودن - اینباند جدید
🗄️ سرورها - وضعیت سرورها
📈 ترافیک - آمار مصرف
📱 کانفیگ - دریافت کانفیگ
💰 مالی - سیستم مالی
🎫 تیکت‌ها - پشتیبانی
👥 کاربران - مدیریت کاربران
⚙️ تنظیمات - تنظیمات پنل

📌 **پشتیبانی:** @XPanelSupport
"""
    bot.reply_to(message, text, parse_mode='Markdown')

# ========== دستورات ادمین ==========
@bot.message_handler(commands=['users'])
def users_command(message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ فقط ادمین!")
        return
    
    users = db.users
    if not users:
        bot.reply_to(message, "📭 هیچ کاربری یافت نشد")
        return
    
    text = "👥 **لیست کاربران:**\n\n"
    for user_id, user in list(users.items())[:15]:
        text += f"• {user['name']} (@{user.get('username', 'ندارد')})\n"
        text += f"  🆔 {user_id} | {user['role']} | {user['status']}\n"
    
    text += f"\n📌 مجموع: {len(users)} کاربر"
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['reset_traffic'])
def reset_traffic_command(message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ فقط ادمین!")
        return
    
    for inbound in db.inbounds.values():
        inbound['traffic_used'] = 0
    
    bot.reply_to(message, "✅ **ترافیک همه اینباندها ریست شد!**")

@bot.message_handler(commands=['add_sample'])
def add_sample_command(message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ فقط ادمین!")
        return
    
    sample_names = ["Premium-US", "Premium-DE", "Premium-SG", "Premium-JP", "Premium-UK", "Premium-FR"]
    count = 0
    for name in sample_names:
        traffic = random.randint(50, 200)
        days = random.randint(15, 60)
        db.create_inbound(name, traffic, 5, days)
        count += 1
    
    bot.reply_to(message, f"✅ **{count} اینباند نمونه با موفقیت اضافه شد!**")

@bot.message_handler(commands=['backup'])
def backup_command(message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ فقط ادمین!")
        return
    
    backup_data = {
        "users": db.users,
        "inbounds": db.inbounds,
        "servers": db.servers,
        "settings": db.settings,
        "transactions": db.transactions,
        "tickets": db.tickets,
        "backup_time": datetime.now().isoformat()
    }
    
    backup_file = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(backup_file, 'w') as f:
        json.dump(backup_data, f, indent=2)
    
    with open(backup_file, 'rb') as f:
        bot.send_document(message.chat.id, f, caption="📦 **بکاپ کامل گرفته شد!**")
    
    os.remove(backup_file)
    bot.reply_to(message, "✅ بکاپ با موفقیت ارسال شد!")

@bot.message_handler(commands=['add_credit'])
def add_credit_command(message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ فقط ادمین!")
        return
    
    args = message.text.split()
    if len(args) != 3:
        bot.reply_to(message, "⚠️ **فرمت:** `/add_credit [کاربر_آیدی] [مبلغ]`")
            return
    
    try:
        target_user = int(args[1])
        amount = int(args[2])
        
        if target_user not in db.users:
            bot.reply_to(message, "❌ کاربر یافت نشد!")
            return
        
        db.users[target_user]['credits'] = db.users[target_user].get('credits', 0) + amount
        
        bot.reply_to(
            message,
            f"✅ **{amount:,} {db.settings['currency']} به حساب کاربر {db.users[target_user]['name']} اضافه شد!**"
        )
        
    except ValueError:
        bot.reply_to(message, "❌ مقادیر عددی را درست وارد کنید!")

@bot.message_handler(commands=['set_config'])
def set_config_command(message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ فقط ادمین!")
        return
    
    args = message.text.split()
    if len(args) != 3:
        bot.reply_to(
            message,
            "⚠️ **فرمت:** `/set_config [key] [value]`\n\n"
            "📌 **کلیدهای موجود:**\n"
            "• `default_traffic` - ترافیک پیش‌فرض\n"
            "• `default_expiry` - انقضای پیش‌فرض\n"
            "• `price_per_gb` - قیمت هر GB\n"
            "• `referral_bonus` - پاداش معرف\n"
            "• `currency` - واحد پول\n"
            "• `maintenance` - وضعیت تعمیرات (True/False)"
        )
        return
    
    key = args[1]
    value = args[2]
    
    if key not in db.settings:
        bot.reply_to(message, f"❌ کلید '{key}' معتبر نیست!")
        return
    
    # تبدیل مقدار به نوع مناسب
    if key == "maintenance":
        value = value.lower() == "true"
    elif key in ["default_traffic", "default_expiry", "price_per_gb", "referral_bonus"]:
        try:
            value = int(value)
        except:
            bot.reply_to(message, "❌ مقدار باید عدد باشد!")
            return
    
    db.settings[key] = value
    bot.reply_to(message, f"✅ **تنظیمات {key} به '{value}' تغییر کرد!**")

# ========== مدیریت پیام‌های معمولی ==========
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text.lower()
    
    if text in ["سلام", "سلامی", "درود", "hi", "hello", "سلام عليكم"]:
        bot.reply_to(message, f"👋 سلام {message.from_user.first_name} جان! به X-Panel Ultra خوش آمدی!")
    
    elif text in ["خوبی", "چطوری", "حالت چطوره", "how are you", "چطورین"]:
        bot.reply_to(message, "🤖 من خوبم! ممنون که پرسیدی! تو چطوری؟")
    
    elif text in ["ممنون", "مرسی", "متشکرم", "thanks", "تشکر"]:
        bot.reply_to(message, "🙏 خواهش می‌کنم! خوشحالم که می‌تونم کمک کنم!")
    
    elif text in ["کمک", "help", "راهنما", "راهنمایی"]:
        bot.reply_to(message, "🆘 برای راهنما، /help رو بزن!")
    
    elif text in ["وضعیت", "status", "اوضاع", "اوضاع چطوره"]:
        stats = db.get_stats()
        bot.reply_to(message, f"🟢 همه چیز عالیه!\n📊 {stats['total_inbounds']} اینباند فعال\n👥 {stats['total_users']} کاربر")
    
    elif text in ["کانفیگ", "config", "لینک", "کانفیک"]:
        inbounds = list(db.inbounds.values())
        if inbounds:
            inbound = random.choice(inbounds)
            configs = generate_advanced_config(inbound['name'], inbound['id'])
            bot.reply_to(message, f"🔗 **کانفیگ {inbound['name']}:**\n`{configs['vless']}`", parse_mode='Markdown')
        else:
            bot.reply_to(message, "❌ هیچ اینباندی یافت نشد!")
    
    elif text in ["لیست", "اینباندها", "اینباند", "inbounds"]:
        inbounds = list(db.inbounds.values())
        if not inbounds:
            bot.reply_to(message, "📭 هیچ اینباندی یافت نشد")
            return
        
        text = "📋 **لیست اینباندها:**\n\n"
        for item in inbounds[:5]:
            status = "🟢" if item['status'] == "فعال" else "🔴"
            text += f"{status} {item['name']}: `{item['traffic_used']:.1f}/{item['traffic_limit']} GB`\n"
        bot.reply_to(message, text, parse_mode='Markdown')
    
    elif text in ["خداحافظ", "خدافظ", "bye", "goodbye", "بای"]:
        bot.reply_to(message, f"👋 خداحافظ {message.from_user.first_name} جان! موفق باشی!")
    
    else:
        responses = [
            "🤔 متوجه نشدم! برای راهنما /help رو بزن.",
            "😅 منظورت رو کامل متوجه نشدم! لطفاً واضح‌تر بگو.",
            "🧐 اینو نمی‌دونم! از منوی دکمه‌ها استفاده کن.",
            "📌 برای دیدن راهنما، /help رو بزن.",
            "🤖 من یه بات فوق‌پیشرفته هستم! دستورات رو ببین."
        ]
        bot.reply_to(message, random.choice(responses))

# ========== اجرا با مدیریت خطا ==========
if __name__ == "__main__":
    print("=" * 70)
    print("🚀 X-Panel Ultra Bot نسخه 5.0.0")
    print("=" * 70)
    print(f"📊 تعداد اینباندها: {len(db.inbounds)}")
    print(f"🗄️ تعداد سرورها: {len(db.servers)}")
    print(f"👥 ادمین‌ها: {ADMIN_IDS}")
    print("✅ برای شروع، /start رو در تلگرام بزن")
    print("=" * 70)
    
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=60)
        except Exception as e:
            print(f"❌ خطا: {e}")
            print("🔄 راه‌اندازی مجدد در 5 ثانیه...")
            time.sleep(5)
            continue
