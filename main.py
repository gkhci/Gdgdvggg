import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import json
import time
import random
from datetime import datetime, timedelta
import threading
import os
import hashlib
from collections import defaultdict

# ========== تنظیمات لاکچری ==========
BOT_TOKEN = "8793482183:AAEGUa7ZEURP26N34DzKvrudnndC3q7apBk"
ADMIN_IDS = [8680457924]
bot = telebot.TeleBot(BOT_TOKEN)

# ========== کلاس دیتابیس پیشرفته ==========
class UltraDatabase:
    def __init__(self):
        self.users = {}
        self.inbounds = {}
        self.servers = {}
        self.transactions = []
        self.tickets = []
        self.analytics = defaultdict(int)
        self.settings = {
            "panel_name": "Luffy Ultra",
            "version": "5.0.0",
            "domain": "web-production-7a838.up.railway.app",
            "uptime": time.time(),
            "maintenance": False,
            "theme": "dark",
            "currency": "💎 تومان",
            "price_per_gb": 5000,
            "referral_bonus": 15,
            "default_traffic": 100,
            "default_expiry": 30,
            "auto_backup": True
        }
        self._init_sample_data()
    
    def _init_sample_data(self):
        # اینباندهای لاکچری
        sample_inbounds = [
            {"id": "1", "name": "🌟 Luffy-Premium-USA", "traffic_limit": 200, "traffic_used": 45.5, "status": "فعال", 
             "expiry": "2027-01-15", "protocol": "vless", "server": "US-01", "speed": "1Gbps", 
             "location": "🇺🇸 آمریکا", "ping": 45, "users": 12, "quality": "پلاتینیوم"},
            {"id": "2", "name": "🔥 Luffy-GOLD-DE", "traffic_limit": 180, "traffic_used": 78.2, "status": "فعال", 
             "expiry": "2026-12-20", "protocol": "vless", "server": "DE-02", "speed": "500Mbps", 
             "location": "🇩🇪 آلمان", "ping": 38, "users": 8, "quality": "طلایی"},
            {"id": "3", "name": "💎 Luffy-Diamond-SG", "traffic_limit": 250, "traffic_used": 23.8, "status": "فعال", 
             "expiry": "2027-02-28", "protocol": "vless", "server": "SG-03", "speed": "2Gbps", 
             "location": "🇸🇬 سنگاپور", "ping": 28, "users": 15, "quality": "الماس"},
            {"id": "4", "name": "⚡ Luffy-ULTRA-JP", "traffic_limit": 300, "traffic_used": 5.3, "status": "غیرفعال", 
             "expiry": "2026-10-10", "protocol": "trojan", "server": "JP-04", "speed": "3Gbps", 
             "location": "🇯🇵 ژاپن", "ping": 55, "users": 3, "quality": "اولترا"},
            {"id": "5", "name": "🌟 Luffy-Premium-UK", "traffic_limit": 220, "traffic_used": 120.7, "status": "فعال", 
             "expiry": "2027-03-01", "protocol": "vmess", "server": "UK-05", "speed": "1.5Gbps", 
             "location": "🇬🇧 انگلیس", "ping": 42, "users": 20, "quality": "پلاتینیوم"},
            {"id": "6", "name": "🔥 Luffy-GOLD-FR", "traffic_limit": 160, "traffic_used": 8.1, "status": "فعال", 
             "expiry": "2027-01-30", "protocol": "vless", "server": "FR-06", "speed": "400Mbps", 
             "location": "🇫🇷 فرانسه", "ping": 48, "users": 5, "quality": "طلایی"},
        ]
        for inbound in sample_inbounds:
            self.inbounds[inbound["id"]] = inbound
        
        # سرورهای لاکچری
        self.servers = {
            "US-01": {"name": "🌟 آمريكا شمالی", "ip": "45.33.22.11", "status": "🟢 آنلاین", "load": 45},
            "DE-02": {"name": "🔥 آلمان مرکزی", "ip": "89.45.67.12", "status": "🟢 آنلاین", "load": 30},
            "SG-03": {"name": "💎 سنگاپور", "ip": "182.55.66.13", "status": "🟢 آنلاین", "load": 60},
            "JP-04": {"name": "⚡ ژاپن", "ip": "133.44.55.14", "status": "🔴 آفلاین", "load": 0},
            "UK-05": {"name": "🌟 انگلیس", "ip": "78.33.44.15", "status": "🟢 آنلاین", "load": 70},
            "FR-06": {"name": "🔥 فرانسه", "ip": "91.22.33.16", "status": "🟢 آنلاین", "load": 25},
        }
    
    def add_user(self, user_id, name, username=None):
        if user_id not in self.users:
            self.users[user_id] = {
                "name": name,
                "username": username,
                "role": "👑 ادمین" if user_id in ADMIN_IDS else "👤 کاربر",
                "joined": datetime.now().isoformat(),
                "last_seen": datetime.now().isoformat(),
                "traffic_used": 0,
                "traffic_limit": self.settings["default_traffic"],
                "expiry": (datetime.now() + timedelta(days=self.settings["default_expiry"])).isoformat(),
                "status": "✅ فعال",
                "referral_code": hashlib.md5(str(user_id).encode()).hexdigest()[:8],
                "referred_by": None,
                "credits": 0,
                "warnings": 0,
                "level": "🟢 عادی"
            }
            return True
        return False
    
    def get_user(self, user_id):
        return self.users.get(user_id)
    
    def get_stats(self):
        total_users = len(self.users)
        active_users = len([u for u in self.users.values() if "فعال" in u.get("status", "")])
        total_inbounds = len(self.inbounds)
        active_inbounds = len([i for i in self.inbounds.values() if i["status"] == "فعال"])
        total_traffic = sum(i["traffic_used"] for i in self.inbounds.values())
        total_transactions = len(self.transactions)
        total_tickets = len(self.tickets)
        
        online_servers = len([s for s in self.servers.values() if "آنلاین" in s["status"]])
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
            "domain": self.settings["domain"],
            "version": self.settings["version"],
            "maintenance": self.settings["maintenance"]
        }
    
    def get_uptime(self):
        seconds = int(time.time() - self.settings["uptime"])
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60
        return f"{days}d {hours}h {minutes}m"
    
    def create_inbound(self, name, traffic_limit, max_ips, days):
        inbound_id = str(len(self.inbounds) + 1)
        expiry = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
        qualities = ["🌟 پلاتینیوم", "💎 الماس", "🔥 طلایی", "⚡ اولترا"]
        servers = list(self.servers.keys())
        
        inbound = {
            "id": inbound_id,
            "name": f"{random.choice(['🌟','💎','🔥','⚡'])} {name}",
            "traffic_limit": traffic_limit,
            "traffic_used": 0,
            "max_ips": max_ips,
            "status": "فعال",
            "expiry": expiry,
            "protocol": random.choice(["vless", "vmess", "trojan"]),
            "server": random.choice(servers),
            "speed": random.choice(["500Mbps", "1Gbps", "2Gbps", "3Gbps"]),
            "location": self.servers[random.choice(servers)]["name"],
            "ping": random.randint(20, 60),
            "users": 0,
            "quality": random.choice(qualities),
            "created": datetime.now().isoformat()
        }
        self.inbounds[inbound_id] = inbound
        return inbound
    
    def delete_inbound(self, inbound_id):
        if inbound_id in self.inbounds:
            del self.inbounds[inbound_id]
            return True
        return False

db = UltraDatabase()
# ========== تولید کانفیگ لاکچری ==========
def generate_luffy_config(inbound_name, inbound_id):
    domain = "web-production-7a838.up.railway.app"
    port = 443
    uuid = f"{random.randint(10000000, 99999999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(10000000, 99999999)}"
    path = f"/ws/{uuid}%3Fed%3D2048"
    
    return f"vless://{uuid}@{domain}:{port}?encryption=none&security=tls&type=ws&host={domain}&path={path}&sni={domain}&fp=chrome&alpn=http/1.1#{inbound_name}"

def generate_all_configs(inbound_name, inbound_id):
    domain = "web-production-7a838.up.railway.app"
    port = 443
    uuid = f"{random.randint(10000000, 99999999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(10000000, 99999999)}"
    path = f"/ws/{uuid}%3Fed%3D2048"
    
    return {
        "🌟 VLESS": f"vless://{uuid}@{domain}:{port}?encryption=none&security=tls&type=ws&host={domain}&path={path}&sni={domain}&fp=chrome&alpn=http/1.1#{inbound_name}",
        "💎 VMESS": f"vmess://{uuid}@{domain}:{port}?security=tls&type=ws&host={domain}&path={path}&sni={domain}&fp=chrome&alpn=http/1.1#{inbound_name}",
        "🔥 Trojan": f"trojan://{uuid}@{domain}:{port}?security=tls&type=ws&host={domain}&path={path}&sni={domain}&fp=chrome&alpn=http/1.1#{inbound_name}"
    }

# ========== کیبوردهای لاکچری ==========
def luxury_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("📊 داشبورد لوکس", callback_data="luxury_dashboard"),
        InlineKeyboardButton("📋 اینباندها", callback_data="luxury_inbounds"),
        InlineKeyboardButton("➕ افزودن", callback_data="luxury_add"),
        InlineKeyboardButton("🗄️ سرورها", callback_data="luxury_servers"),
        InlineKeyboardButton("📈 ترافیک", callback_data="luxury_traffic"),
        InlineKeyboardButton("🔗 کانفیگ", callback_data="luxury_config"),
        InlineKeyboardButton("💰 مالی", callback_data="luxury_finance"),
        InlineKeyboardButton("🎫 تیکت", callback_data="luxury_tickets"),
        InlineKeyboardButton("👥 کاربران", callback_data="luxury_users"),
        InlineKeyboardButton("⚙️ تنظیمات", callback_data="luxury_settings"),
        InlineKeyboardButton("🔄 بروزرسانی", callback_data="luxury_refresh"),
        InlineKeyboardButton("🆘 راهنما", callback_data="luxury_help")
    )
    return keyboard

def inbound_luxury_actions(inbound_id, name):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🔗 کانفیگ", callback_data=f"luxury_link_{inbound_id}"),
        InlineKeyboardButton("🔗 همه", callback_data=f"luxury_all_links_{inbound_id}"),
        InlineKeyboardButton("📊 مصرف", callback_data=f"luxury_usage_{inbound_id}"),
        InlineKeyboardButton("⏸️ وضعیت", callback_data=f"luxury_toggle_{inbound_id}"),
        InlineKeyboardButton("🗑️ حذف", callback_data=f"luxury_delete_{inbound_id}")
    )
    keyboard.add(InlineKeyboardButton("🔙 بازگشت", callback_data="luxury_inbounds"))
    return keyboard

def _status_emoji(value):
    if value < 40:
        return "🟢"
    elif value < 70:
        return "🟡"
    else:
        return "🔴"
        # ========== استارت ==========
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    username = message.from_user.username
    
    db.add_user(user_id, name, username)
    
    welcome = f"""
✨ **به پنل Luffy Ultra خوش آمدید!** ✨

━━━━━━━━━━━━━━━━━━━━━━
👤 **کاربر:** {name}
🆔 **آیدی:** `{user_id}`
👑 **نقش:** {db.users[user_id]['role']}
🔑 **کد معرف:** `{db.users[user_id]['referral_code']}`
━━━━━━━━━━━━━━━━━━━━━━

🌐 **دامنه:** `web-production-7a838.up.railway.app`
📌 **نسخه:** 5.0.0

💫 از دکمه‌های زیر استفاده کنید:
"""
    bot.send_message(
        message.chat.id,
        welcome,
        reply_markup=luxury_menu(),
        parse_mode='Markdown'
    )

# ========== مدیریت کامل دکمه‌ها ==========
@bot.callback_query_handler(func=lambda call: True)
def luxury_callback(call):
    user_id = call.from_user.id
    
    # ===== داشبورد لوکس =====
    if call.data == "luxury_dashboard":
        stats = db.get_stats()
        text = f"""
✨ **داشبورد Luffy Ultra** ✨
━━━━━━━━━━━━━━━━━━━━━━
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
━━━━━━━━━━━━━━━━━━━━━━

🖥️ **وضعیت سیستم:**
• CPU: `{stats['cpu']}%` {_status_emoji(stats['cpu'])}
• Memory: `{stats['memory']}%` {_status_emoji(stats['memory'])}
• Uptime: `{stats['uptime']}`
• وضعیت: {'🟢 آنلاین' if not stats['maintenance'] else '🔧 تعمیرات'}

📊 **آمار کلی:**
• 👥 کاربران: `{stats['total_users']}`
• ✅ فعال: `{stats['active_users']}`
• 📋 اینباندها: `{stats['total_inbounds']}`
• 🟢 فعال: `{stats['active_inbounds']}`
• 📦 ترافیک: `{stats['total_traffic']:.1f} GB`
• 🗄️ سرورها: `{stats['online_servers']}/{stats['total_servers']} 🟢`
• 💰 تراکنش‌ها: `{stats['total_transactions']}`
• 🎫 تیکت‌ها: `{stats['total_tickets']}`

🌐 **دامنه:** `{stats['domain']}`
📌 **نسخه:** `{stats['version']}`
━━━━━━━━━━━━━━━━━━━━━━
"""
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=luxury_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "✅ داشبورد بروز شد")
    
    # ===== لیست اینباندها =====
    elif call.data == "luxury_inbounds":
        show_luxury_inbounds(call)
    
    # ===== افزودن =====
    elif call.data == "luxury_add":
        bot.answer_callback_query(call.id, "📝 فرم افزودن")
        bot.edit_message_text(
            "✨ **افزودن اینباند جدید**\n━━━━━━━━━━━━━━━━━━━━━━\n"
            "📌 **فرمت:**\n"
            "`/add [نام] [ترافیک_GB] [IP] [روز]`\n\n"
            "💎 **مثال:**\n"
            "`/add Luffy-Premium 200 5 30`\n\n"
            "🌟 اینباند با بهترین کیفیت ساخته می‌شود!",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=luxury_menu(),
            parse_mode='Markdown'
        )
    
    # ===== سرورها =====
    elif call.data == "luxury_servers":
        text = "🗄️ **وضعیت سرورهای لوکس**\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
        for server_id, server in db.servers.items():
            load_bar = "█" * int(server["load"] / 10) + "░" * (10 - int(server["load"] / 10))
            text += f"{server['status']} **{server['name']}**\n"
            text += f"📊 بار: `{server['load']}%` {load_bar}\n"
            text += f"🌐 IP: `{server['ip']}`\n\n"
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=luxury_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "🗄️ سرورها")
    
    # ===== ترافیک =====
    elif call.data == "luxury_traffic":
        stats = db.get_stats()
        text = f"📈 **آمار ترافیک لوکس**\n━━━━━━━━━━━━━━━━━━━━━━\n📦 ترافیک کل: `{stats['total_traffic']:.1f} GB`\n\n"
        
        sorted_inbounds = sorted(db.inbounds.values(), key=lambda x: x['traffic_used'], reverse=True)
        for item in sorted_inbounds[:8]:
            usage_percent = (item['traffic_used'] / item['traffic_limit']) * 100 if item['traffic_limit'] > 0 else 0
            bar = "█" * int(usage_percent / 10) + "░" * (10 - int(usage_percent / 10))
            status = "🟢" if item['status'] == "فعال" else "🔴"
            text += f"{status} {item['name']}\n"
            text += f"`{item['traffic_used']:.1f}/{item['traffic_limit']} GB` {bar} {usage_percent:.0f}%\n"
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=luxury_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "📊 ترافیک")
    
    # ===== کانفیگ =====
    elif call.data == "luxury_config":
        inbounds = list(db.inbounds.values())
        if not inbounds:
            bot.answer_callback_query(call.id, "❌ اینباندی یافت نشد")
            return
        
        inbound = random.choice(inbounds)
        configs = generate_all_configs(inbound['name'], inbound['id'])
        
        text = f"""
🔐 **کانفیگ‌های {inbound['name']}**
━━━━━━━━━━━━━━━━━━━━━━
📛 **نام:** {inbound['name']}
📌 **وضعیت:** {inbound['status']}
🗄️ **سرور:** {inbound['server']}
🌍 **موقعیت:** {inbound['location']}
⚡ **پینگ:** {inbound['ping']}ms
━━━━━━━━━━━━━━━━━━━━━━

🌟 **VLESS:**
`{configs['🌟 VLESS']}`

💎 **VMESS:**
`{configs['💎 VMESS']}`

🔥 **Trojan:**
`{configs['🔥 Trojan']}`
━━━━━━━━━━━━━━━━━━━━━━
"""
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=luxury_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "🔗 کانفیگ‌ها")
    
    # ===== مالی =====
    elif call.data == "luxury_finance":
        user = db.get_user(user_id)
        text = f"""
💰 **سیستم مالی لوکس**
━━━━━━━━━━━━━━━━━━━━━━
💵 **واحد:** {db.settings['currency']}
💲 **قیمت هر GB:** `{db.settings['price_per_gb']:,} {db.settings['currency']}`
🎁 **پاداش معرف:** `{db.settings['referral_bonus']}%`

📊 **آمار شما:**
• اعتبار: `{user.get('credits', 0):,} {db.settings['currency']}`

📌 **دستورات:**
/credit - اعتبار من
/add_credit [مبلغ] - شارژ (ادمین)
━━━━━━━━━━━━━━━━━━━━━━
"""
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=luxury_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "💰 مالی")
    
    # ===== تیکت =====
    elif call.data == "luxury_tickets":
        text = """
🎫 **سیستم تیکت‌های پشتیبانی**
━━━━━━━━━━━━━━━━━━━━━━
📌 **دستورات:**
/ticket [موضوع] - تیکت جدید
/tickets - لیست تیکت‌ها
/reply [ID] [پاسخ] - پاسخ
/close [ID] - بستن تیکت

📊 **وضعیت:** 🟢 فعال
━━━━━━━━━━━━━━━━━━━━━━
"""
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=luxury_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "🎫 تیکت‌ها")
    
    # ===== کاربران =====
    elif call.data == "luxury_users":
        if user_id not in ADMIN_IDS:
            bot.answer_callback_query(call.id, "⛔ فقط ادمین!")
            return
        
        users = db.users
        if not users:
            bot.edit_message_text("📭 هیچ کاربری یافت نشد", call.message.chat.id, call.message.message_id, reply_markup=luxury_menu())
            return
        
        text = "👥 **لیست کاربران لوکس**\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
        for user_id, user in list(users.items())[:10]:
            text += f"• {user['name']} (@{user.get('username', 'ندارد')})\n"
            text += f"  🆔 {user_id} | {user['role']}\n"
        
        text += f"\n📌 مجموع: {len(users)} کاربر"
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=luxury_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "👥 کاربران")
    
    # ===== تنظیمات =====
    elif call.data == "luxury_settings":
        stats = db.get_stats()
        text = f"""
⚙️ **تنظیمات پنل لوکس**
━━━━━━━━━━━━━━━━━━━━━━
🔹 **نام:** Luffy Ultra
🔹 **نسخه:** {stats['version']}
🔹 **وضعیت:** {'🟢 آنلاین' if not stats['maintenance'] else '🔧 تعمیرات'}

⚡ **تنظیمات:**
• ترافیک پیش‌فرض: `{db.settings['default_traffic']} GB`
• انقضا: `{db.settings['default_expiry']} روز`
• ارز: `{db.settings['currency']}`
• قیمت: `{db.settings['price_per_gb']:,} {db.settings['currency']}`
• پاداش: `{db.settings['referral_bonus']}%`

🛠️ **سیستم:**
• آپتایم: `{stats['uptime']}`
• CPU: `{stats['cpu']}%`
• RAM: `{stats['memory']}%`
━━━━━━━━━━━━━━━━━━━━━━
"""
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=luxury_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "⚙️ تنظیمات")
    
    # ===== Refresh =====
    elif call.data == "luxury_refresh":
        stats = db.get_stats()
        bot.answer_callback_query(call.id, "🔄 بروزرسانی شد")
        text = f"""
✅ **پنل بروزرسانی شد!**
━━━━━━━━━━━━━━━━━━━━━━
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📊 اینباندها: {stats['total_inbounds']}
👥 کاربران: {stats['total_users']}
📦 ترافیک: {stats['total_traffic']:.1f} GB
🗄️ سرورها: {stats['online_servers']}/{stats['total_servers']}
━━━━━━━━━━━━━━━━━━━━━━
"""
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=luxury_menu(),
            parse_mode='Markdown'
        )
    
    # ===== Help =====
    elif call.data == "luxury_help":
        text = """
🆘 **راهنمای کامل Luffy Ultra**
━━━━━━━━━━━━━━━━━━━━━━
📌 **دستورات اصلی:**
/start - منوی لوکس
/add [نام] [ترافیک] [IP] [روز] - افزودن
/stats - آمار پنل
/list - لیست اینباندها
/status - وضعیت سیستم
/help - این راهنما

📌 **دستورات کاربری:**
/profile - پروفایل من
/credit - اعتبار من
/ticket [موضوع] - تیکت جدید

📌 **دستورات ادمین:**
/users - لیست کاربران
/add_credit [مبلغ] - شارژ
/traffic_reset - ریست ترافیک
/backup - بکاپ

📌 **دکمه‌ها:**
📊 داشبورد - آمار کامل
📋 اینباندها - مدیریت
➕ افزودن - اینباند جدید
🗄️ سرورها - وضعیت
📈 ترافیک - آمار مصرف
🔗 کانفیگ - دریافت
💰 مالی - سیستم مالی
🎫 تیکت‌ها - پشتیبانی
👥 کاربران - مدیریت
⚙️ تنظیمات - پنل

📌 **پشتیبانی:** @LuffySupport
━━━━━━━━━━━━━━━━━━━━━━
"""
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=luxury_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "🆘 راهنما")
    
    # ===== عملیات اینباندها =====
    elif call.data.startswith("luxury_link_"):
        inbound_id = call.data.split("_")[2]
        inbound = db.inbounds.get(inbound_id)
        if inbound:
            config = generate_luffy_config(inbound['name'], inbound_id)
            bot.answer_callback_query(call.id, "🔗 کانفیگ کپی شد")
            bot.send_message(
                call.message.chat.id,
                f"🔗 **کانفیگ {inbound['name']}**\n━━━━━━━━━━━━━━━━━━━━━━\n`{config}`\n━━━━━━━━━━━━━━━━━━━━━━",
                parse_mode='Markdown'
            )
    
    elif call.data.startswith("luxury_all_links_"):
        inbound_id = call.data.split("_")[3]
        inbound = db.inbounds.get(inbound_id)
        if inbound:
            links = generate_all_configs(inbound['name'], inbound_id)
            text = f"""
🔗 **همه کانفیگ‌های {inbound['name']}**
━━━━━━━━━━━━━━━━━━━━━━
🌟 **VLESS:**
`{links['🌟 VLESS']}`

💎 **VMESS:**
`{links['💎 VMESS']}`

🔥 **Trojan:**
`{links['🔥 Trojan']}`
━━━━━━━━━━━━━━━━━━━━━━
"""
            bot.answer_callback_query(call.id, "🔗 همه کانفیگ‌ها")
            bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
    
    elif call.data.startswith("luxury_usage_"):
        inbound_id = call.data.split("_")[2]
        inbound = db.inbounds.get(inbound_id)
        if inbound:
            usage_percent = (inbound['traffic_used'] / inbound['traffic_limit']) * 100 if inbound['traffic_limit'] > 0 else 0
            bar = "█" * int(usage_percent / 10) + "░" * (10 - int(usage_percent / 10))
            text = f"""
📊 **مصرف {inbound['name']}**
━━━━━━━━━━━━━━━━━━━━━━
📦 مصرف: `{inbound['traffic_used']:.1f} / {inbound['traffic_limit']} GB`
📊 درصد: `{usage_percent:.1f}%`
{bar}

📅 انقضا: `{inbound['expiry']}`
📌 وضعیت: `{inbound['status']}`
🗄️ سرور: {inbound['server']}
🌍 موقعیت: {inbound['location']}
⚡ پینگ: {inbound['ping']}ms
📊 سرعت: {inbound['speed']}
━━━━━━━━━━━━━━━━━━━━━━
"""
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=inbound_luxury_actions(inbound_id, inbound['name']),
                parse_mode='Markdown'
            )
    
    elif call.data.startswith("luxury_toggle_"):
        inbound_id = call.data.split("_")[2]
        inbound = db.inbounds.get(inbound_id)
        if inbound:
            inbound["status"] = "غیرفعال" if inbound["status"] == "فعال" else "فعال"
            bot.answer_callback_query(call.id, f"⏸️ {inbound['status']} شد")
            show_luxury_inbounds(call)
    
    elif call.data.startswith("luxury_delete_"):
        inbound_id = call.data.split("_")[2]
        if db.delete_inbound(inbound_id):
            bot.answer_callback_query(call.id, "🗑️ حذف شد")
            show_luxury_inbounds(call)

def show_luxury_inbounds(call):
    inbounds = list(db.inbounds.values())
    
    if not inbounds:
        bot.edit_message_text(
            "📭 **هیچ اینباندی یافت نشد**",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=luxury_menu(),
            parse_mode='Markdown'
        )
        return
    
    text = "📋 **اینباندهای لوکس**\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    for item in inbounds[:10]:
        status_emoji = "🟢" if item['status'] == "فعال" else "🔴"
        usage_percent = (item['traffic_used'] / item['traffic_limit']) * 100 if item['traffic_limit'] > 0 else 0
        bar = "█" * int(usage_percent / 10) + "░" * (10 - int(usage_percent / 10))
        
        text += f"{status_emoji} **{item['name']}**\n"
        text += f"📊 `{item['traffic_used']:.1f}/{item['traffic_limit']} GB` {bar}\n"
        text += f"📅 انقضا: `{item['expiry']}` | 🔗 {item['protocol']}\n"
        text += f"🗄️ {item['server']} | 🌍 {item['location']} | ⚡ {item['ping']}ms\n"
        text += f"🏷️ {item['quality']} | 📶 {item['speed']}\n"
        text += f"🆔 {item['id']}\n━━━━━━━━━━━━━━━━━━━━━━\n"
        
        if item['id']:
            keyboard.add(
                InlineKeyboardButton(f"🔗 {item['name'][:10]}", callback_data=f"luxury_link_{item['id']}"),
                InlineKeyboardButton(f"📊 مصرف", callback_data=f"luxury_usage_{item['id']}"),
                InlineKeyboardButton(f"⏸️ {item['status']}", callback_data=f"luxury_toggle_{item['id']}"),
                InlineKeyboardButton(f"🗑️ حذف", callback_data=f"luxury_delete_{item['id']}")
            )
    
    keyboard.add(InlineKeyboardButton("➕ افزودن جدید", callback_data="luxury_add"))
    keyboard.add(InlineKeyboardButton("🔙 بازگشت", callback_data="luxury_dashboard"))
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard,
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id, "📋 لیست بروز شد")

# ========== دستورات متنی ==========
@bot.message_handler(commands=['add'])
def add_command(message):
    args = message.text.split()
    if len(args) != 5:
        bot.reply_to(
            message,
            "⚠️ **فرمت:**\n`/add [نام] [ترافیک] [IP] [روز]`\n\n"
            "💎 **مثال:**\n`/add Luffy-Premium 200 5 30`",
            parse_mode='Markdown'
        )
        return
    
    try:
        _, name, traffic, max_ips, days = args
        traffic = float(traffic)
        max_ips = int(max_ips)
        days = int(days)
        
        if traffic <= 0 or max_ips <= 0 or days <= 0:
            bot.reply_to(message, "❌ مقادیر باید مثبت باشند")
            return
        
        bot.reply_to(message, "⏳ در حال ساخت اینباند لوکس...")
        inbound = db.create_inbound(name, traffic, max_ips, days)
        
        text = f"""
✅ **اینباند لوکس ساخته شد!**
━━━━━━━━━━━━━━━━━━━━━━
📛 **نام:** {inbound['name']}
📊 **ترافیک:** {inbound['traffic_limit']} GB
👥 **IP:** {inbound['max_ips']}
📅 **انقضا:** {inbound['expiry']}
🔌 **پروتکل:** {inbound['protocol']}
🗄️ **سرور:** {inbound['server']}
🌍 **موقعیت:** {inbound['location']}
⚡ **پینگ:** {inbound['ping']}ms
📶 **سرعت:** {inbound['speed']}
🏷️ **کیفیت:** {inbound['quality']}
🆔 **شناسه:** {inbound['id']}
━━━━━━━━━━━━━━━━━━━━━━
"""
        bot.reply_to(message, text, parse_mode='Markdown')
        
        config = generate_luffy_config(inbound['name'], inbound['id'])
        bot.send_message(
            message.chat.id,
            f"🔗 **کانفیگ لوفی:**\n`{config}`",
            parse_mode='Markdown'
        )
        
    except ValueError:
        bot.reply_to(message, "❌ مقادیر عددی را درست وارد کنید")
    except Exception as e:
        bot.reply_to(message, f"❌ خطا: {str(e)}")

@bot.message_handler(commands=['stats'])
def stats_command(message):
    stats = db.get_stats()
    text = f"""
📊 **آمار Luffy Ultra**
━━━━━━━━━━━━━━━━━━━━━━
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🖥️ **سیستم:**
• CPU: `{stats['cpu']}%` {_status_emoji(stats['cpu'])}
• Memory: `{stats['memory']}%` {_status_emoji(stats['memory'])}
• Uptime: `{stats['uptime']}`

📊 **آمار:**
• 👥 کاربران: `{stats['total_users']}`
• ✅ فعال: `{stats['active_users']}`
• 📋 اینباندها: `{stats['total_inbounds']}`
• 📦 ترافیک: `{stats['total_traffic']:.1f} GB`
• 🗄️ سرورها: `{stats['online_servers']}/{stats['total_servers']}`

🌐 **دامنه:** `{stats['domain']}`
📌 **نسخه:** `{stats['version']}`
━━━━━━━━━━━━━━━━━━━━━━
"""
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['list'])
def list_command(message):
    inbounds = list(db.inbounds.values())
    if not inbounds:
        bot.reply_to(message, "📭 هیچ اینباندی یافت نشد")
        return
    
    text = "📋 **لیست اینباندها:**\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    for item in inbounds[:10]:
        status = "🟢" if item['status'] == "فعال" else "🔴"
        text += f"{status} {item['name']}\n"
        text += f"📊 `{item['traffic_used']:.1f}/{item['traffic_limit']} GB` | ⚡ {item['ping']}ms\n\n"
    
    text += f"📌 {len(inbounds)} اینباند"
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['profile'])
def profile_command(message):
    user_id = message.from_user.id
    user = db.get_user(user_id)
    if not user:
        bot.reply_to(message, "❌ کاربر یافت نشد!")
        return
    
    text = f"""
👤 **پروفایل لوکس**
━━━━━━━━━━━━━━━━━━━━━━
📛 **نام:** {user['name']}
🆔 **آیدی:** `{user_id}`
👑 **نقش:** {user['role']}
📅 **عضویت:** {user['joined']}
🔑 **کد معرف:** `{user['referral_code']}`

📊 **آمار:**
• ترافیک: `{user.get('traffic_used', 0):.1f} GB`
• محدودیت: `{user.get('traffic_limit', 0)} GB`
• اعتبار: `{user.get('credits', 0):,} {db.settings['currency']}`
• وضعیت: {user.get('status', '❌')}

📌 اینباندها: `{len(db.inbounds)}`
━━━━━━━━━━━━━━━━━━━━━━
"""
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def help_command(message):
    text = """
📚 **راهنمای Luffy Ultra**
━━━━━━━━━━━━━━━━━━━━━━
**دستورات اصلی:**
/start - منوی لوکس
/add [نام] [ترافیک] [IP] [روز] - افزودن
/stats - آمار پنل
/list - لیست اینباندها
/profile - پروفایل من
/help - این راهنما
**دکمه‌ها:**
📊 داشبورد - آمار کامل
📋 اینباندها - مدیریت
➕ افزودن - اینباند جدید
🗄️ سرورها - وضعیت
📈 ترافیک - آمار مصرف
🔗 کانفیگ - دریافت
💰 مالی - سیستم مالی
🎫 تیکت‌ها - پشتیبانی
👥 کاربران - مدیریت
⚙️ تنظیمات - پنل

**ویژگی‌های لوکس:**
✅ شبیه‌سازی دقیق لوفی
✅ کانفیگ با فرمت اصلی
✅ طراحی مدرن و شیک
✅ دکمه‌های شیشه‌ای
✅ پشتیبانی کامل
━━━━━━━━━━━━━━━━━━━━━━
📌 **پشتیبانی:** @LuffySupport
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
    
    text = "👥 **لیست کاربران لوکس**\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    for user_id, user in list(users.items())[:10]:
        text += f"• {user['name']} (@{user.get('username', 'ندارد')})\n"
        text += f"  🆔 {user_id} | {user['role']}\n"
    
    text += f"\n📌 مجموع: {len(users)} کاربر"
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['traffic_reset'])
def traffic_reset_command(message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ فقط ادمین!")
        return
    
    for inbound in db.inbounds.values():
        inbound['traffic_used'] = 0
    
    bot.reply_to(message, "✅ **ترافیک همه اینباندها ریست شد!**")

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

@bot.message_handler(commands=['add_sample'])
def add_sample_command(message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ فقط ادمین!")
        return
    
    sample_names = ["Luffy-Premium-US", "Luffy-Gold-DE", "Luffy-Diamond-SG", "Luffy-Ultra-JP", "Luffy-Premium-UK"]
    count = 0
    for name in sample_names:
        traffic = random.randint(50, 200)
        days = random.randint(15, 60)
        db.create_inbound(name, traffic, 5, days)
        count += 1
    
    bot.reply_to(message, f"✅ **{count} اینباند نمونه لوکس اضافه شد!**")

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
        bot.send_document(message.chat.id, f, caption="📦 **بکاپ کامل لوکس گرفته شد!**")
    
    os.remove(backup_file)
    bot.reply_to(message, "✅ بکاپ با موفقیت ارسال شد!")

@bot.message_handler(commands=['ping'])
def ping_command(message):
    start_time = time.time()
    bot.send_chat_action(message.chat.id, 'typing')
    end_time = time.time()
    ping = (end_time - start_time) * 1000
    bot.reply_to(message, f"🏓 **Pong!**\n⏱ زمان پاسخ: `{ping:.0f} ms`", parse_mode='Markdown')

@bot.message_handler(commands=['status'])
def status_command(message):
    stats = db.get_stats()
    text = f"""
🟢 **وضعیت بات لوکس**
━━━━━━━━━━━━━━━━━━━━━━
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
━━━━━━━━━━━━━━━━━━━━━━
"""
    bot.reply_to(message, text, parse_mode='Markdown')

# ========== مدیریت پیام‌های معمولی ==========
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text.lower()
    
    if text in ["سلام", "سلامی", "درود", "hi", "hello", "سلام عليكم"]:
        bot.reply_to(message, f"✨ سلام {message.from_user.first_name} جان! به Luffy Ultra خوش آمدی! 🌟")
    
    elif text in ["خوبی", "چطوری", "حالت چطوره", "how are you", "چطورین"]:
        bot.reply_to(message, "🌟 من عالی‌ام! ممنون که پرسیدی! تو چطوری؟ 💫")
    
    elif text in ["ممنون", "مرسی", "متشکرم", "thanks", "تشکر"]:
        bot.reply_to(message, "🙏 خواهش می‌کنم! خوشحالم که می‌تونم کمک کنم! ✨")
    
    elif text in ["کمک", "help", "راهنما", "راهنمایی"]:
        bot.reply_to(message, "🆘 برای راهنما، /help رو بزن!")
    
    elif text in ["وضعیت", "status", "اوضاع", "اوضاع چطوره"]:
        stats = db.get_stats()
        bot.reply_to(message, f"🌟 همه چیز عالیه!\n📊 {stats['total_inbounds']} اینباند فعال\n👥 {stats['total_users']} کاربر")
    
    elif text in ["کانفیگ", "config", "لینک", "کانفیک"]:
        inbounds = list(db.inbounds.values())
        if inbounds:
            inbound = random.choice(inbounds)
            config = generate_luffy_config(inbound['name'], inbound['id'])
            bot.reply_to(message, f"🔗 **کانفیگ {inbound['name']}:**\n`{config}`", parse_mode='Markdown')
        else:
            bot.reply_to(message, "❌ هیچ اینباندی یافت نشد!")
    
    elif text in ["لیست", "اینباندها", "اینباند", "inbounds"]:
        inbounds = list(db.inbounds.values())
        if not inbounds:
            bot.reply_to(message, "📭 هیچ اینباندی یافت نشد")
            return
        
        text = "📋 **لیست اینباندها:**\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
        for item in inbounds[:5]:
            status = "🟢" if item['status'] == "فعال" else "🔴"
            text += f"{status} {item['name']}\n"
            text += f"📊 `{item['traffic_used']:.1f}/{item['traffic_limit']} GB`\n\n"
        bot.reply_to(message, text, parse_mode='Markdown')
    
    elif text in ["خداحافظ", "خدافظ", "bye", "goodbye", "بای"]:
        bot.reply_to(message, f"👋 خداحافظ {message.from_user.first_name} جان! موفق باشی! 🌟")
    
    else:
        responses = [
            "✨ متوجه نشدم! برای راهنما /help رو بزن.",
            "💎 منظورت رو کامل متوجه نشدم! لطفاً واضح‌تر بگو.",
            "🌟 اینو نمی‌دونم! از منوی دکمه‌ها استفاده کن.",
            "🔥 برای دیدن راهنما، /help رو بزن.",
            "⚡ من یه بات لوکس هستم! دستورات رو ببین."
        ]
        bot.reply_to(message, random.choice(responses))

# ========== اجرا ==========
if __name__ == "__main__":
    print("=" * 70)
    print("✨ Luffy Ultra Bot نسخه 5.0.0 ✨")
    print("=" * 70)
    print(f"📊 تعداد اینباندها: {len(db.inbounds)}")
    print(f"🗄️ تعداد سرورها: {len(db.servers)}")
    print(f"👥 ادمین‌ها: {ADMIN_IDS}")
    print("✅ برای شروع، /start رو بزن")
    print("=" * 70)
    
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=60)
        except Exception as e:
            print(f"❌ خطا: {e}")
            print("🔄 راه‌اندازی مجدد در 5 ثانیه...")
            time.sleep(5)
            continue
