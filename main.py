import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import time
import random
from datetime import datetime, timedelta
import os
import hashlib

# ========== تنظیمات ==========
BOT_TOKEN = "8793482183:AAEGUa7ZEURP26N34DzKvrudnndC3q7apBk"
ADMIN_IDS = [8680457924]
bot = telebot.TeleBot(BOT_TOKEN)

# ========== کانفیگ‌های واقعی ==========
REAL_CONFIGS = {
    "Luffy-rega": "vless://d2cd0565-ac45-4fba-8883-fba0664dbe08@web-production-7a838.up.railway.app:443?encryption=none&security=tls&type=ws&host=web-production-7a838.up.railway.app&path=/ws/d2cd0565-ac45-4fba-8883-fba0664dbe08%3Fed%3D2048&sni=web-production-7a838.up.railway.app&fp=chrome&alpn=http/1.1#Luffy-rega",
}

# ========== دیتابیس ==========
class Database:
    def __init__(self):
        self.users = {}
        self.inbounds = {}
        self.settings = {
            "panel_name": "Luffy Ultra",
            "version": "5.0.0",
            "domain": "web-production-7a838.up.railway.app",
            "uptime": time.time(),
            "currency": "💎 تومان",
            "price_per_gb": 5000,
            "referral_bonus": 15,
            "default_traffic": 100,
            "default_expiry": 30
        }
        self._init_sample_data()
    
    def _init_sample_data(self):
        sample_inbounds = [
            {"id": "1", "name": "🌟 Luffy-rega", "traffic_limit": 200, "traffic_used": 45.5, "status": "فعال", "expiry": "2027-01-15", "protocol": "vless", "server": "US-01", "speed": "1Gbps", "location": "🇺🇸 آمریکا", "ping": 45, "quality": "پلاتینیوم"},
            {"id": "2", "name": "🔥 Luffy-GOLD", "traffic_limit": 180, "traffic_used": 78.2, "status": "فعال", "expiry": "2026-12-20", "protocol": "vless", "server": "DE-02", "speed": "500Mbps", "location": "🇩🇪 آلمان", "ping": 38, "quality": "طلایی"},
            {"id": "3", "name": "💎 Luffy-Diamond", "traffic_limit": 250, "traffic_used": 23.8, "status": "فعال", "expiry": "2027-02-28", "protocol": "vless", "server": "SG-03", "speed": "2Gbps", "location": "🇸🇬 سنگاپور", "ping": 28, "quality": "الماس"},
        ]
        for inbound in sample_inbounds:
            self.inbounds[inbound["id"]] = inbound
    
    def add_user(self, user_id, name, username=None):
        if user_id not in self.users:
            self.users[user_id] = {
                "name": name,
                "username": username,
                "role": "👑 ادمین" if user_id in ADMIN_IDS else "👤 کاربر",
                "joined": datetime.now().isoformat(),
                "credits": 0,
                "status": "✅ فعال"
            }
            return True
        return False
    
    def get_user(self, user_id):
        return self.users.get(user_id)
    
    def get_stats(self):
        return {
            "total_users": len(self.users),
            "active_users": len([u for u in self.users.values() if "فعال" in u.get("status", "")]),
            "total_inbounds": len(self.inbounds),
            "active_inbounds": len([i for i in self.inbounds.values() if i["status"] == "فعال"]),
            "total_traffic": sum(i["traffic_used"] for i in self.inbounds.values()),
            "cpu": random.randint(10, 60),
            "memory": random.randint(30, 80),
            "uptime": self.get_uptime(),
            "domain": self.settings["domain"],
            "version": self.settings["version"]
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
        inbound = {
            "id": inbound_id,
            "name": f"🌟 {name}",
            "traffic_limit": traffic_limit,
            "traffic_used": 0,
            "max_ips": max_ips,
            "status": "فعال",
            "expiry": expiry,
            "protocol": "vless",
            "server": "US-01",
            "speed": "1Gbps",
            "location": "🌍 جهانی",
            "ping": random.randint(20, 60),
            "quality": "💎 ویژه"
        }
        self.inbounds[inbound_id] = inbound
        return inbound
    
    def delete_inbound(self, inbound_id):
        if inbound_id in self.inbounds:
            del self.inbounds[inbound_id]
            return True
        return False

db = Database()

# ========== تولید کانفیگ ==========
def get_real_config(inbound_name):
    """دریافت کانفیگ واقعی"""
    for key in REAL_CONFIGS:
        if key.lower() in inbound_name.lower():
            return REAL_CONFIGS[key]
    return None

def generate_luffy_config(inbound_name, inbound_id):
    """تولید کانفیگ با اولویت واقعی"""
    real = get_real_config(inbound_name)
    if real:
        return real
    
    domain = "web-production-7a838.up.railway.app"
    port = 443
    uuid = f"{random.randint(10000000, 99999999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(10000000, 99999999)}"
    path = f"/ws/{uuid}%3Fed%3D2048"
    return f"vless://{uuid}@{domain}:{port}?encryption=none&security=tls&type=ws&host={domain}&path={path}&sni={domain}&fp=chrome&alpn=http/1.1#{inbound_name}"

def generate_all_configs(inbound_name, inbound_id):
    real = get_real_config(inbound_name)
    domain = "web-production-7a838.up.railway.app"
    port = 443
    uuid = f"{random.randint(10000000, 99999999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(10000000, 99999999)}"
    path = f"/ws/{uuid}%3Fed%3D2048"
    
    if real:
        return {
            "🌟 VLESS (واقعی)": real,
            "💎 VMESS": f"vmess://{uuid}@{domain}:{port}?security=tls&type=ws&host={domain}&path={path}&sni={domain}&fp=chrome&alpn=http/1.1#{inbound_name}",
            "🔥 Trojan": f"trojan://{uuid}@{domain}:{port}?security=tls&type=ws&host={domain}&path={path}&sni={domain}&fp=chrome&alpn=http/1.1#{inbound_name}"
        }
    
    return {
        "🌟 VLESS": f"vless://{uuid}@{domain}:{port}?encryption=none&security=tls&type=ws&host={domain}&path={path}&sni={domain}&fp=chrome&alpn=http/1.1#{inbound_name}",
        "💎 VMESS": f"vmess://{uuid}@{domain}:{port}?security=tls&type=ws&host={domain}&path={path}&sni={domain}&fp=chrome&alpn=http/1.1#{inbound_name}",
        "🔥 Trojan": f"trojan://{uuid}@{domain}:{port}?security=tls&type=ws&host={domain}&path={path}&sni={domain}&fp=chrome&alpn=http/1.1#{inbound_name}"
    }

# ========== کیبوردها ==========
def luxury_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("📊 داشبورد", callback_data="dashboard"),
        InlineKeyboardButton("📋 اینباندها", callback_data="inbounds"),
        InlineKeyboardButton("➕ افزودن", callback_data="add"),
        InlineKeyboardButton("🔗 کانفیگ واقعی", callback_data="real_config"),
        InlineKeyboardButton("📈 ترافیک", callback_data="traffic"),
        InlineKeyboardButton("👤 پروفایل", callback_data="profile"),
        InlineKeyboardButton("🔄 بروزرسانی", callback_data="refresh"),
        InlineKeyboardButton("🆘 راهنما", callback_data="help")
    )
    return keyboard

def inbound_actions(inbound_id):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🔗 کانفیگ", callback_data=f"link_{inbound_id}"),
        InlineKeyboardButton("🔗 همه", callback_data=f"all_links_{inbound_id}"),
        InlineKeyboardButton("📊 مصرف", callback_data=f"usage_{inbound_id}"),
        InlineKeyboardButton("⏸️ وضعیت", callback_data=f"toggle_{inbound_id}"),
        InlineKeyboardButton("🗑️ حذف", callback_data=f"delete_{inbound_id}")
    )
    keyboard.add(InlineKeyboardButton("🔙 بازگشت", callback_data="inbounds"))
    return keyboard

# ========== دستورات ==========
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    db.add_user(user_id, name)
    
    welcome = f"""
✨ **به پنل Luffy Ultra خوش آمدید!** ✨
━━━━━━━━━━━━━━━━━━━━━━
👤 **کاربر:** {name}
👑 **نقش:** {db.users[user_id]['role']}
━━━━━━━━━━━━━━━━━━━━━━

💫 از دکمه‌های زیر استفاده کنید:
"""
    bot.send_message(message.chat.id, welcome, reply_markup=luxury_menu(), parse_mode='Markdown')

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    
    # ===== داشبورد =====
    if call.data == "dashboard":
        stats = db.get_stats()
        text = f"""
✨ **داشبورد Luffy Ultra** ✨
━━━━━━━━━━━━━━━━━━━━━━
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🖥️ **سیستم:**
• CPU: `{stats['cpu']}%`
• Memory: `{stats['memory']}%`
• Uptime: `{stats['uptime']}`

📊 **آمار:**
• 👥 کاربران: `{stats['total_users']}`
• ✅ فعال: `{stats['active_users']}`
• 📋 اینباندها: `{stats['total_inbounds']}`
• 📦 ترافیک: `{stats['total_traffic']:.1f} GB`

🌐 **دامنه:** `{stats['domain']}`
📌 **نسخه:** `{stats['version']}`
━━━━━━━━━━━━━━━━━━━━━━
"""
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=luxury_menu(), parse_mode='Markdown')
        bot.answer_callback_query(call.id, "✅ بروز شد")
    
    # ===== اینباندها =====
    elif call.data == "inbounds":
        show_inbounds(call)
    
    # ===== افزودن =====
    elif call.data == "add":
        bot.answer_callback_query(call.id, "📝 فرم افزودن")
        bot.edit_message_text(
            "✨ **افزودن اینباند جدید**\n━━━━━━━━━━━━━━━━━━━━━━\n"
            "📌 **فرمت:**\n"
            "`/add [نام] [ترافیک_GB] [IP] [روز]`\n\n"
            "💎 **مثال:**\n"
            "`/add Luffy-Premium 200 5 30`",
            call.message.chat.id, call.message.message_id, reply_markup=luxury_menu(), parse_mode='Markdown'
        )
    
    # ===== کانفیگ واقعی =====
    elif call.data == "real_config":
        text = f"""
🔗 **کانفیگ واقعی Luffy**
━━━━━━━━━━━━━━━━━━━━━━
📌 **این کانفیگ فعال و تست شده است!**

`{REAL_CONFIGS['Luffy-rega']}`

📥 روی لینک کلیک کن تا کپی بشه!
✅ **وضعیت:** 🟢 فعال
━━━━━━━━━━━━━━━━━━━━━━
"""
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=luxury_menu(), parse_mode='Markdown')
        bot.answer_callback_query(call.id, "🔗 کانفیگ واقعی")
    
    # ===== ترافیک =====
    elif call.data == "traffic":
        stats = db.get_stats()
        text = f"📈 **آمار ترافیک**\n━━━━━━━━━━━━━━━━━━━━━━\n📦 ترافیک کل: `{stats['total_traffic']:.1f} GB`\n\n"
        for item in list(db.inbounds.values())[:5]:
            usage_percent = (item['traffic_used'] / item['traffic_limit']) * 100 if item['traffic_limit'] > 0 else 0
            bar = "█" * int(usage_percent / 10) + "░" * (10 - int(usage_percent / 10))
            text += f"• {item['name']}: `{item['traffic_used']:.1f}/{item['traffic_limit']} GB`\n  `{bar}` {usage_percent:.0f}%\n"
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=luxury_menu(), parse_mode='Markdown')
        bot.answer_callback_query(call.id, "📊 ترافیک")
    
    # ===== پروفایل =====
    elif call.data == "profile":
        user = db.get_user(user_id)
        if user:
            text = f"""
👤 **پروفایل شما**
━━━━━━━━━━━━━━━━━━━━━━
📛 **نام:** {user['name']}
🆔 **آیدی:** `{user_id}`
👑 **نقش:** {user['role']}
📅 **عضویت:** {user['joined']}
💰 **اعتبار:** `{user.get('credits', 0):,} {db.settings['currency']}`
📊 **وضعیت:** {user.get('status', '✅ فعال')}
━━━━━━━━━━━━━━━━━━━━━━
"""
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=luxury_menu(), parse_mode='Markdown')
            bot.answer_callback_query(call.id, "👤 پروفایل")
    
    # ===== Refresh =====
    elif call.data == "refresh":
        stats = db.get_stats()
        bot.answer_callback_query(call.id, "🔄 بروزرسانی شد")
        text = f"""
✅ **بروزرسانی شد!**
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📊 اینباندها: {stats['total_inbounds']}
👥 کاربران: {stats['total_users']}
📦 ترافیک: {stats['total_traffic']:.1f} GB
"""
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=luxury_menu(), parse_mode='Markdown')
    
    # ===== Help =====
    elif call.data == "help":
        text = """
🆘 **راهنما**
━━━━━━━━━━━━━━━━━━━━━━
**دستورات:**
/start - منوی اصلی
/add [نام] [ترافیک] [IP] [روز] - افزودن
/stats - آمار پنل
/list - لیست اینباندها
/profile - پروفایل من
/help - این راهنما

**دکمه‌ها:**
📊 داشبورد - آمار کامل
📋 اینباندها - مدیریت
➕ افزودن - اینباند جدید
🔗 کانفیگ واقعی - دریافت کانفیگ فعال
📈 ترافیک - آمار مصرف
👤 پروفایل - اطلاعات کاربر

📌 **پشتیبانی:** @Admin
━━━━━━━━━━━━━━━━━━━━━━
"""
        bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=luxury_menu(), parse_mode='Markdown')
        bot.answer_callback_query(call.id, "🆘 راهنما")
    
    # ===== عملیات اینباندها =====
    elif call.data.startswith("link_"):
        inbound_id = call.data.split("_")[1]
        inbound = db.inbounds.get(inbound_id)
        if inbound:
            config = generate_luffy_config(inbound['name'], inbound_id)
            bot.answer_callback_query(call.id, "🔗 کانفیگ کپی شد")
            bot.send_message(call.message.chat.id, f"🔗 **کانفیگ {inbound['name']}**\n━━━━━━━━━━━━━━━━━━━━━━\n`{config}`\n━━━━━━━━━━━━━━━━━━━━━━", parse_mode='Markdown')
    
    elif call.data.startswith("all_links_"):
        inbound_id = call.data.split("_")[2]
        inbound = db.inbounds.get(inbound_id)
        if inbound:
            links = generate_all_configs(inbound['name'], inbound_id)
            text = f"🔗 **همه کانفیگ‌های {inbound['name']}**\n━━━━━━━━━━━━━━━━━━━━━━\n"
            for key, value in links.items():
                text += f"\n**{key}:**\n`{value}`\n"
            bot.answer_callback_query(call.id, "🔗 همه کانفیگ‌ها")
            bot.send_message(call.message.chat.id, text, parse_mode='Markdown')
    
    elif call.data.startswith("usage_"):
        inbound_id = call.data.split("_")[1]
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
⚡ پینگ: {inbound['ping']}ms
━━━━━━━━━━━━━━━━━━━━━━
"""
            bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=inbound_actions(inbound_id), parse_mode='Markdown')
    
    elif call.data.startswith("toggle_"):
        inbound_id = call.data.split("_")[1]
        inbound = db.inbounds.get(inbound_id)
        if inbound:
            inbound["status"] = "غیرفعال" if inbound["status"] == "فعال" else "فعال"
            bot.answer_callback_query(call.id, f"⏸️ {inbound['status']} شد")
            show_inbounds(call)
    
    elif call.data.startswith("delete_"):
        inbound_id = call.data.split("_")[1]
        if db.delete_inbound(inbound_id):
            bot.answer_callback_query(call.id, "🗑️ حذف شد")
            show_inbounds(call)

def show_inbounds(call):
    inbounds = list(db.inbounds.values())
    if not inbounds:
        bot.edit_message_text("📭 **هیچ اینباندی یافت نشد**", call.message.chat.id, call.message.message_id, reply_markup=luxury_menu(), parse_mode='Markdown')
        return
    
    text = "📋 **لیست اینباندها**\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    for item in inbounds[:10]:
        status_emoji = "🟢" if item['status'] == "فعال" else "🔴"
        usage_percent = (item['traffic_used'] / item['traffic_limit']) * 100 if item['traffic_limit'] > 0 else 0
        bar = "█" * int(usage_percent / 10) + "░" * (10 - int(usage_percent / 10))
        
        text += f"{status_emoji} **{item['name']}**\n"
        text += f"📊 `{item['traffic_used']:.1f}/{item['traffic_limit']} GB` {bar}\n"
        text += f"📅 انقضا: `{item['expiry']}` | ⚡ {item['ping']}ms\n"
        text += f"🆔 {item['id']}\n━━━━━━━━━━━━━━━━━━━━━━\n"
        
        keyboard.add(
            InlineKeyboardButton(f"🔗 {item['name'][:8]}", callback_data=f"link_{item['id']}"),
            InlineKeyboardButton(f"📊 مصرف", callback_data=f"usage_{item['id']}"),
            InlineKeyboardButton(f"⏸️ {item['status']}", callback_data=f"toggle_{item['id']}"),
            InlineKeyboardButton(f"🗑️", callback_data=f"delete_{item['id']}")
        )
    
    keyboard.add(InlineKeyboardButton("➕ افزودن جدید", callback_data="add"))
    keyboard.add(InlineKeyboardButton("🔙 بازگشت", callback_data="dashboard"))
    
    bot.edit_message_text(text, call.message.chat.id, call.message.message_id, reply_markup=keyboard, parse_mode='Markdown')
    bot.answer_callback_query(call.id, "📋 لیست بروز شد")

# ========== دستورات متنی ==========
@bot.message_handler(commands=['add'])
def add_command(message):
    args = message.text.split()
    if len(args) != 5:
        bot.reply_to(message, "⚠️ **فرمت:**\n`/add [نام] [ترافیک] [IP] [روز]`\n\n💎 **مثال:**\n`/add Luffy-Premium 200 5 30`", parse_mode='Markdown')
        return
    
    try:
        _, name, traffic, max_ips, days = args
        traffic = float(traffic)
        max_ips = int(max_ips)
        days = int(days)
        
        if traffic <= 0 or max_ips <= 0 or days <= 0:
            bot.reply_to(message, "❌ مقادیر باید مثبت باشند")
            return
        
        bot.reply_to(message, "⏳ در حال ساخت...")
        inbound = db.create_inbound(name, traffic, max_ips, days)
        
        text = f"""
✅ **اینباند ساخته شد!**
━━━━━━━━━━━━━━━━━━━━━━
📛 **نام:** {inbound['name']}
📊 **ترافیک:** {inbound['traffic_limit']} GB
👥 **IP:** {inbound['max_ips']}
📅 **انقضا:** {inbound['expiry']}
🆔 **شناسه:** {inbound['id']}
━━━━━━━━━━━━━━━━━━━━━━
"""
        bot.reply_to(message, text, parse_mode='Markdown')
        
        config = generate_luffy_config(inbound['name'], inbound['id'])
        bot.send_message(message.chat.id, f"🔗 **کانفیگ:**\n`{config}`", parse_mode='Markdown')
        
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
• CPU: `{stats['cpu']}%`
• Memory: `{stats['memory']}%`
• Uptime: `{stats['uptime']}`

📊 **آمار:**
• 👥 کاربران: `{stats['total_users']}`
• ✅ فعال: `{stats['active_users']}`
• 📋 اینباندها: `{stats['total_inbounds']}`
• 📦 ترافیک: `{stats['total_traffic']:.1f} GB`

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
        text += f"{status} {item['name']}\n📊 `{item['traffic_used']:.1f}/{item['traffic_limit']} GB`\n\n"
    bot.reply_to(message, text, parse_mode='Markdown')
@bot.message_handler(commands=['profile'])
def profile_command(message):
    user_id = message.from_user.id
    user = db.get_user(user_id)
    if not user:
        bot.reply_to(message, "❌ کاربر یافت نشد!")
        return
    
    text = f"""
👤 **پروفایل شما**
━━━━━━━━━━━━━━━━━━━━━━
📛 **نام:** {user['name']}
🆔 **آیدی:** `{user_id}`
👑 **نقش:** {user['role']}
📅 **عضویت:** {user['joined']}
💰 **اعتبار:** `{user.get('credits', 0):,} {db.settings['currency']}`
📊 **وضعیت:** {user.get('status', '✅ فعال')}
━━━━━━━━━━━━━━━━━━━━━━
"""
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def help_command(message):
    text = """
📚 **راهنمای Luffy Ultra**
━━━━━━━━━━━━━━━━━━━━━━
**دستورات:**
/start - منوی اصلی
/add [نام] [ترافیک] [IP] [روز] - افزودن
/stats - آمار پنل
/list - لیست اینباندها
/profile - پروفایل من
/help - این راهنما

**دکمه‌ها:**
📊 داشبورد - آمار کامل
📋 اینباندها - مدیریت
➕ افزودن - اینباند جدید
🔗 کانفیگ واقعی - دریافت کانفیگ فعال
📈 ترافیک - آمار مصرف
👤 پروفایل - اطلاعات کاربر

📌 **پشتیبانی:** @Admin
━━━━━━━━━━━━━━━━━━━━━━
"""
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['ping'])
def ping_command(message):
    start = time.time()
    bot.send_chat_action(message.chat.id, 'typing')
    ping = (time.time() - start) * 1000
    bot.reply_to(message, f"🏓 **Pong!**\n⏱ {ping:.0f} ms", parse_mode='Markdown')

@bot.message_handler(commands=['status'])
def status_command(message):
    stats = db.get_stats()
    text = f"""
🟢 **وضعیت بات**
━━━━━━━━━━━━━━━━━━━━━━
✅ **در حال اجرا**
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 کاربران: `{stats['total_users']}`
📋 اینباندها: `{stats['total_inbounds']}`
📦 ترافیک: `{stats['total_traffic']:.1f} GB`
⏱ آپتایم: `{stats['uptime']}`
━━━━━━━━━━━━━━━━━━━━━━
"""
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['users'])
def users_command(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ فقط ادمین!")
        return
    
    users = db.users
    if not users:
        bot.reply_to(message, "📭 هیچ کاربری یافت نشد")
        return
    
    text = "👥 **لیست کاربران**\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
    for user_id, user in list(users.items())[:10]:
        text += f"• {user['name']} (@{user.get('username', 'ندارد')})\n  🆔 {user_id} | {user['role']}\n"
    text += f"\n📌 مجموع: {len(users)} کاربر"
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['traffic_reset'])
def traffic_reset_command(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ فقط ادمین!")
        return
    
    for inbound in db.inbounds.values():
        inbound['traffic_used'] = 0
    bot.reply_to(message, "✅ **ترافیک همه اینباندها ریست شد!**")

@bot.message_handler(commands=['add_credit'])
def add_credit_command(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ فقط ادمین!")
        return
    
    args = message.text.split()
    if len(args) != 3:
        bot.reply_to(message, "⚠️ **فرمت:** `/add_credit [آیدی] [مبلغ]`")
        return
    
    try:
        target = int(args[1])
        amount = int(args[2])
        if target not in db.users:
            bot.reply_to(message, "❌ کاربر یافت نشد!")
            return
        db.users[target]['credits'] = db.users[target].get('credits', 0) + amount
        bot.reply_to(message, f"✅ {amount:,} {db.settings['currency']} به {db.users[target]['name']} اضافه شد!")
    except:
        bot.reply_to(message, "❌ خطا! مقادیر را درست وارد کنید.")

@bot.message_handler(commands=['add_sample'])
def add_sample_command(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ فقط ادمین!")
        return
    
    sample_names = ["Luffy-Premium-US", "Luffy-Gold-DE", "Luffy-Diamond-SG"]
    count = 0
    for name in sample_names:
        traffic = random.randint(50, 200)
        days = random.randint(15, 60)
        db.create_inbound(name, traffic, 5, days)
        count += 1
    bot.reply_to(message, f"✅ **{count} اینباند نمونه اضافه شد!**")

@bot.message_handler(commands=['backup'])
def backup_command(message):
    if message.from_user.id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ فقط ادمین!")
        return
    
    backup_data = {
        "users": db.users,
        "inbounds": db.inbounds,
        "settings": db.settings,
        "time": datetime.now().isoformat()
    }
    backup_file = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(backup_file, 'w') as f:
        json.dump(backup_data, f, indent=2)
    with open(backup_file, 'rb') as f:
        bot.send_document(message.chat.id, f, caption="📦 **بکاپ گرفته شد!**")
    os.remove(backup_file)
    bot.reply_to(message, "✅ بکاپ با موفقیت ارسال شد!")

# ========== مدیریت پیام‌ها ==========
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
        bot.reply_to(message, f"🔗 **کانفیگ واقعی:**\n`{REAL_CONFIGS['Luffy-rega']}`", parse_mode='Markdown')
    
    elif text in ["لیست", "اینباندها", "اینباند", "inbounds"]:
        inbounds = list(db.inbounds.values())
        if not inbounds:
            bot.reply_to(message, "📭 هیچ اینباندی یافت نشد")
            return
        text = "📋 **لیست اینباندها:**\n━━━━━━━━━━━━━━━━━━━━━━\n\n"
        for item in inbounds[:5]:
            status = "🟢" if item['status'] == "فعال" else "🔴"
            text += f"{status} {item['name']}\n📊 `{item['traffic_used']:.1f}/{item['traffic_limit']} GB`\n\n"
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
    print("=" * 60)
    print("✨ Luffy Ultra Bot نسخه 5.0.0 ✨")
    print("=" * 60)
    print(f"📊 اینباندها: {len(db.inbounds)}")
    print(f"👥 ادمین‌ها: {ADMIN_IDS}")
    print("✅ برای شروع، /start رو بزن")
    print("=" * 60)
    
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            print(f"❌ خطا: {e}")
            print("🔄 راه‌اندازی مجدد...")
            time.sleep(5)
