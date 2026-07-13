import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import json
import time
import random
from datetime import datetime, timedelta
import threading
import os

# ========== تنظیمات ==========
BOT_TOKEN = "8793482183:AAEGUa7ZEURP26N34DzKvrudnndC3q7apBk"
ADMIN_IDS = [8680457924]  # آیدی عددی خودت رو بذار

bot = telebot.TeleBot(BOT_TOKEN)

# ========== دیتابیس شبیه‌سازی شده ==========
class Database:
    def __init__(self):
        self.users = {}  # {user_id: {name, role, joined}}
        self.inbounds = {}  # {inbound_id: {name, traffic, status, ...}}
        self.traffic_logs = []
        self.settings = {
            "panel_name": "X-Panel",
            "version": "3.0.0",
            "uptime": time.time()
        }
        self._init_sample_data()
    
    def _init_sample_data(self):
        # اینباندهای نمونه
        sample_inbounds = [
            {"id": "1", "name": "VLESS-USA", "traffic_limit": 100, "traffic_used": 23.5, "status": "فعال", "expiry": "2026-12-31", "protocol": "vless", "network": "ws"},
            {"id": "2", "name": "VLESS-GERMANY", "traffic_limit": 200, "traffic_used": 45.2, "status": "فعال", "expiry": "2026-11-15", "protocol": "vless", "network": "grpc"},
            {"id": "3", "name": "VLESS-SINGAPORE", "traffic_limit": 150, "traffic_used": 12.8, "status": "فعال", "expiry": "2027-01-20", "protocol": "vless", "network": "ws"},
            {"id": "4", "name": "TROJAN-JAPAN", "traffic_limit": 80, "traffic_used": 5.3, "status": "غیرفعال", "expiry": "2026-09-10", "protocol": "trojan", "network": "tcp"},
            {"id": "5", "name": "VMESS-UK", "traffic_limit": 120, "traffic_used": 67.1, "status": "فعال", "expiry": "2026-10-05", "protocol": "vmess", "network": "ws"},
        ]
        
        for inbound in sample_inbounds:
            self.inbounds[inbound["id"]] = inbound
    
    def add_user(self, user_id, name):
        if user_id not in self.users:
            self.users[user_id] = {
                "name": name,
                "role": "admin" if user_id in ADMIN_IDS else "user",
                "joined": datetime.now().isoformat(),
                "last_seen": datetime.now().isoformat()
            }
            return True
        return False
    
    def get_user(self, user_id):
        return self.users.get(user_id)
    
    def get_stats(self):
        total_users = len(self.users)
        active_users = len([u for u in self.users.values() if u.get("status") != "expired"])
        total_inbounds = len(self.inbounds)
        active_inbounds = len([i for i in self.inbounds.values() if i["status"] == "فعال"])
        total_traffic = sum(i["traffic_used"] for i in self.inbounds.values())
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "total_inbounds": total_inbounds,
            "active_inbounds": active_inbounds,
            "total_traffic": total_traffic,
            "cpu": random.randint(10, 60),
            "memory": random.randint(30, 80),
            "uptime": self.get_uptime(),
            "domain": "panel.x-panel.com",
            "version": self.settings["version"]
        }
    
    def get_uptime(self):
        seconds = int(time.time() - self.settings["uptime"])
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60
        return f"{days}d {hours}h {minutes}m"
    
    def create_inbound(self, name, traffic_limit, max_ips, days):
        inbound_id = str(int(time.time()))
        expiry = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
        
        inbound = {
            "id": inbound_id,
            "name": name,
            "traffic_limit": traffic_limit,
            "traffic_used": 0,
            "max_ips": max_ips,
            "status": "فعال",
            "expiry": expiry,
            "protocol": random.choice(["vless", "vmess", "trojan"]),
            "network": random.choice(["ws", "grpc", "tcp"]),
            "created": datetime.now().isoformat()
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
        return f"{inbound['protocol']}://{random.randint(100, 999)}.x-panel.com:443?uuid={random.randint(100000, 999999)}&security=tls&network={inbound['network']}"

db = Database()

# ========== کیبوردهای شیشه‌ای ==========
def main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("📊 داشبورد", callback_data="dashboard"),
        InlineKeyboardButton("📋 اینباندها", callback_data="list_inbounds"),
        InlineKeyboardButton("➕ افزودن اینباند", callback_data="add_inbound"),
        InlineKeyboardButton("📈 ترافیک", callback_data="traffic"),
        InlineKeyboardButton("⚙️ تنظیمات", callback_data="settings"),
        InlineKeyboardButton("👤 پروفایل", callback_data="profile"),
        InlineKeyboardButton("📱 کانفیگ من", callback_data="my_config"),
        InlineKeyboardButton("🔄 بروزرسانی", callback_data="refresh"),
        InlineKeyboardButton("🆘 راهنما", callback_data="help")
    )
    return keyboard

def inbound_actions(inbound_id, name):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🔗 لینک کانفیگ", callback_data=f"link_{inbound_id}"),
        InlineKeyboardButton("🗑️ حذف", callback_data=f"delete_{inbound_id}"),
        InlineKeyboardButton("⏸️ غیرفعال", callback_data=f"disable_{inbound_id}"),
        InlineKeyboardButton("📊 آمار مصرف", callback_data=f"usage_{inbound_id}")
    )
    keyboard.add(InlineKeyboardButton("🔙 بازگشت", callback_data="list_inbounds"))
    return keyboard

# ========== دستور /start ==========
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    
    db.add_user(user_id, name)
    
    welcome = f"""
🌟 **به پنل مدیریت X-Panel خوش آمدید!**

👤 کاربر: {name}
🆔 آیدی: {user_id}
👑 نقش: {'ادمین' if user_id in ADMIN_IDS else 'کاربر'}

📌 از دکمه‌های زیر برای مدیریت استفاده کنید:
"""
    
    bot.send_message(
        message.chat.id,
        welcome,
        reply_markup=main_menu(),
        parse_mode='Markdown'
    )

# ========== مدیریت دکمه‌ها ==========
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    
    # --- داشبورد ---
    if call.data == "dashboard":
        stats = db.get_stats()
        text = f"""
📊 **داشبورد X-Panel**

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🖥️ **وضعیت سیستم:**
• CPU: `{stats['cpu']}%`
• Memory: `{stats['memory']}%`
• Uptime: `{stats['uptime']}`

📊 **آمار کلی:**
• 👥 کاربران: `{stats['total_users']}`
• ✅ فعال: `{stats['active_users']}`
• 📋 اینباندها: `{stats['total_inbounds']}`
• 📦 ترافیک کل: `{stats['total_traffic']:.1f} GB`

🌐 **دامنه:** `{stats['domain']}`
📌 **نسخه:** `{stats['version']}`
"""
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "✅ داشبورد بروز شد")
    
    # --- لیست اینباندها ---
    elif call.data == "list_inbounds":
        show_inbounds(call)
    
    # --- افزودن اینباند ---
    elif call.data == "add_inbound":
        bot.answer_callback_query(call.id, "📝 فرم افزودن اینباند")
        bot.edit_message_text(
            "📝 **افزودن اینباند جدید**\n\n"
            "فرمت:\n"
            "`/add [نام] [ترافیک_GB] [حداکثر_IP] [روز_اعتبار]`\n\n"
            "مثال:\n"
            "`/add ایران-تهران 150 5 30`\n\n"
            "📌 اینباند جدید با پروتکل تصادفی (VLESS/VMESS/Trojan) ساخته می‌شود.",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )
    
    # --- ترافیک ---
    elif call.data == "traffic":
        stats = db.get_stats()
        text = f"""
📈 **آمار ترافیک**

📦 ترافیک کل: `{stats['total_traffic']:.1f} GB`

📊 **مصرف اینباندها:**

"""
        for item in list(db.inbounds.values())[:10]:
            usage_percent = (item['traffic_used'] / item['traffic_limit']) * 100 if item['traffic_limit'] > 0 else 0
            bar = "█" * int(usage_percent / 10) + "░" * (10 - int(usage_percent / 10))
            text += f"• {item['name']}: `{item['traffic_used']:.1f}/{item['traffic_limit']} GB`\n"
            text += f"  `{bar}` {usage_percent:.0f}%\n"
        
        text += f"\n📌 {len(db.inbounds)} اینباند در سیستم وجود دارد."
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "📊 آمار ترافیک نمایش داده شد")
    
    # --- تنظیمات ---
    elif call.data == "settings":
        text = """
⚙️ **تنظیمات پنل**

🔹 نام پنل: X-Panel
🔹 نسخه: 3.0.0
🔹 وضعیت: 🟢 آنلاین

⚡ **تنظیمات پیشرفته:**
• تعداد کاربران: {total_users}
• اینباندها: {total_inbounds}
• ترافیک کل: {total_traffic:.1f} GB

🛠️ **ابزارها:**
• آپتایم: {uptime}
• CPU: {cpu}%
• RAM: {memory}%

📌 برای تغییر تنظیمات با ادمین تماس بگیرید.
"""
        stats = db.get_stats()
        text = text.format(**stats)
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "⚙️ تنظیمات نمایش داده شد")
    
    # --- پروفایل ---
    elif call.data == "profile":
        user = db.get_user(user_id)
        if user:
            text = f"""
👤 **پروفایل کاربری**

📛 نام: {user['name']}
🆔 آیدی: {user_id}
👑 نقش: {user['role']}
📅 تاریخ عضویت: {user['joined']}

🔐 وضعیت: {'✅ فعال' if user_id in ADMIN_IDS else '🔵 کاربر عادی'}

📊 تعداد اینباندها: {len(db.inbounds)}
"""
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=main_menu(),
                parse_mode='Markdown'
            )
            bot.answer_callback_query(call.id, "👤 پروفایل شما")
    
    # --- کانفیگ من ---
    elif call.data == "my_config":
        # یک کانفیگ تصادفی شبیه‌سازی می‌کنیم
        config = f"""
🔐 **کانفیگ شما**

پروتکل: {random.choice(['vless', 'vmess', 'trojan'])}
آدرس: {random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}
پورت: {random.choice([443, 8443, 2053, 2087])}
UUID: {random.randint(100000, 999999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(100000, 999999)}
شبکه: ws
امنیت: tls
"""
        bot.edit_message_text(
            config,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "📱 کانفیگ شما")
    
    # --- Refresh ---
    elif call.data == "refresh":
        stats = db.get_stats()
        bot.answer_callback_query(call.id, "🔄 بروزرسانی شد")
        text = f"""
✅ **پنل بروزرسانی شد!**

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
📊 اینباندها: {stats['total_inbounds']}
👥 کاربران: {stats['total_users']}
📦 ترافیک: {stats['total_traffic']:.1f} GB
"""
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )
    
    # --- Help ---
    elif call.data == "help":
        text = """
🆘 **راهنمای کامل**

📌 **دستورات:**
/start - منوی اصلی
/add [نام] [ترافیک] [IP] [روز] - افزودن اینباند
/stats - آمار پنل
/list - لیست اینباندها
/help - این راهنما

📌 **دکمه‌ها:**
📊 داشبورد - مشاهده آمار کلی
📋 اینباندها - مدیریت اینباندها
➕ افزودن - ساخت اینباند جدید
📈 ترافیک - آمار مصرف
⚙️ تنظیمات - تنظیمات پنل
👤 پروفایل - اطلاعات کاربر
📱 کانفیگ من - دریافت کانفیگ

📌 **پشتیبانی:** @Admin
"""
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "🆘 راهنما")
    
    # --- عملیات اینباندها ---
    elif call.data.startswith("link_"):
        inbound_id = call.data.split("_")[1]
        link = db.get_inbound_link(inbound_id)
        if link:
            bot.answer_callback_query(call.id, "🔗 لینک کانفیگ کپی شد")
            bot.send_message(
                call.message.chat.id,
                f"🔗 **لینک کانفیگ:**\n`{link}`",
                parse_mode='Markdown'
            )
        else:
            bot.answer_callback_query(call.id, "❌ اینباند یافت نشد")
    
    elif call.data.startswith("delete_"):
        inbound_id = call.data.split("_")[1]
        if db.delete_inbound(inbound_id):
            bot.answer_callback_query(call.id, "🗑️ اینباند حذف شد")
            show_inbounds(call)
        else:
            bot.answer_callback_query(call.id, "❌ خطا در حذف")
    
    elif call.data.startswith("disable_"):
        inbound_id = call.data.split("_")[1]
        inbound = db.inbounds.get(inbound_id)
        if inbound:
            inbound["status"] = "غیرفعال" if inbound["status"] == "فعال" else "فعال"
            status = "غیرفعال" if inbound["status"] == "غیرفعال" else "فعال"
            bot.answer_callback_query(call.id, f"⏸️ اینباند {status} شد")
            show_inbounds(call)
        else:
            bot.answer_callback_query(call.id, "❌ اینباند یافت نشد")
    
    elif call.data.startswith("usage_"):
        inbound_id = call.data.split("_")[1]
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
"""
            bot.edit_message_text(
                text,
                call.message.chat.id,
                call.message.message_id,
                reply_markup=inbound_actions(inbound_id, inbound['name']),
                parse_mode='Markdown'
            )
        else:
            bot.answer_callback_query(call.id, "❌ اینباند یافت نشد")

def show_inbounds(call):
    inbounds = list(db.inbounds.values())
    
    if not inbounds:
        bot.edit_message_text(
            "📭 **هیچ اینباندی یافت نشد**\n\n"
            "برای افزودن، از دکمه ➕ استفاده کنید.",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu(),
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
        text += f"🆔 {item['id']}\n\n"
        
        if item['id']:
            keyboard.add(
                InlineKeyboardButton(f"🔗 {item['name']}", callback_data=f"link_{item['id']}"),
                InlineKeyboardButton(f"🗑️ حذف", callback_data=f"delete_{item['id']}"),
                InlineKeyboardButton(f"⏸️ {'فعال/غیرفعال'}", callback_data=f"disable_{item['id']}"),
                InlineKeyboardButton(f"📊 مصرف", callback_data=f"usage_{item['id']}")
            )
    
    keyboard.add(InlineKeyboardButton("➕ افزودن جدید", callback_data="add_inbound"))
    keyboard.add(InlineKeyboardButton("🔙 بازگشت", callback_data="dashboard"))
    
    bot.edit_message_text(
        text,
        call.message.chat.id,
        call.message.message_id,
        reply_markup=keyboard,
        parse_mode='Markdown'
    )
    bot.answer_callback_query(call.id, "📋 لیست اینباندها بروز شد")

# ========== دستور /add ==========
@bot.message_handler(commands=['add'])
def add_command(message):
    args = message.text.split()
    if len(args) != 5:
        bot.reply_to(
            message,
            "⚠️ **فرمت صحیح:**\n"
            "`/add [نام] [ترافیک_GB] [حداکثر_IP] [روز_اعتبار]`\n\n"
            "مثال:\n"
            "`/add ایران-تهران 150 5 30`",
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
        
        text = f"""
✅ **اینباند با موفقیت ساخته شد!**

📛 نام: {inbound['name']}
📊 ترافیک: {inbound['traffic_limit']} GB
👥 حداکثر IP: {inbound['max_ips']}
📅 انقضا: {inbound['expiry']}
🔌 پروتکل: {inbound['protocol']}
🌐 شبکه: {inbound['network']}
🆔 شناسه: {inbound['id']}
"""
        bot.reply_to(message, text, parse_mode='Markdown')
        
        # نمایش لیست بروز شده
        keyboard = InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            InlineKeyboardButton("📋 مشاهده اینباندها", callback_data="list_inbounds"),
            InlineKeyboardButton("🔗 دریافت کانفیگ", callback_data=f"link_{inbound['id']}")
        )
        bot.send_message(message.chat.id, "🔽 عملیات بعدی:", reply_markup=keyboard)
        
    except ValueError:
        bot.reply_to(message, "❌ مقادیر عددی را درست وارد کنید")
    except Exception as e:
        bot.reply_to(message, f"❌ خطا: {str(e)}")

# ========== دستور /stats ==========
@bot.message_handler(commands=['stats'])
def stats_command(message):
    stats = db.get_stats()
    text = f"""
📊 **آمار پنل X-Panel**

⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🖥️ **سیستم:**
• CPU: `{stats['cpu']}%`
• Memory: `{stats['memory']}%`
• Uptime: `{stats['uptime']}`

📊 **آمار:**
• 👥 کاربران: `{stats['total_users']}`
• ✅ فعال: `{stats['active_users']}`
• 📋 اینباندها: `{stats['total_inbounds']}`
• 📦 ترافیک کل: `{stats['total_traffic']:.1f} GB`

🌐 دامنه: `{stats['domain']}`
📌 نسخه: `{stats['version']}`
"""
    bot.reply_to(message, text, parse_mode='Markdown')

# ========== دستور /list ==========
@bot.message_handler(commands=['list'])
def list_command(message):
    inbounds = list(db.inbounds.values())
    if not inbounds:
        bot.reply_to(message, "📭 هیچ اینباندی یافت نشد")
        return
    
    text = "📋 **لیست اینباندها:**\n\n"
    for item in inbounds[:10]:
        status = "🟢" if item['status'] == "فعال" else "🔴"
        text += f"{status} {item['name']}: `{item['traffic_used']:.1f}/{item['traffic_limit']} GB` - {item['status']}\n"
    
    text += f"\n📌 {len(inbounds)} اینباند در سیستم وجود دارد."
    bot.reply_to(message, text, parse_mode='Markdown')
    # ========== دستور /help ==========
@bot.message_handler(commands=['help'])
def help_command(message):
    text = """
📚 **راهنمای کامل X-Panel**

**دستورات:**
/start - منوی اصلی
/add [نام] [ترافیک] [IP] [روز] - افزودن اینباند
/stats - آمار پنل
/list - لیست اینباندها
/help - این راهنما

**دکمه‌های اصلی:**
📊 داشبورد - مشاهده آمار کامل
📋 اینباندها - مدیریت اینباندها
➕ افزودن - ساخت اینباند جدید
📈 ترافیک - آمار مصرف
⚙️ تنظیمات - تنظیمات پنل
👤 پروفایل - اطلاعات کاربر
📱 کانفیگ من - دریافت کانفیگ

**ویژگی‌های پیشرفته:**
✅ شبیه‌سازی کامل پنل
✅ مدیریت اینباندها
✅ نمایش آمار لحظه‌ای
✅ دریافت لینک کانفیگ
✅ فعال/غیرفعال کردن اینباند
✅ نمایش مصرف دقیق

📌 **پشتیبانی:** @SupportBot
"""
    bot.reply_to(message, text, parse_mode='Markdown')

# ========== دستور /about ==========
@bot.message_handler(commands=['about'])
def about_command(message):
    text = """
🤖 **درباره X-Panel Bot**

📌 **نسخه:** 3.0.0
🔹 **ساخته شده با:** Python + Telebot
📅 **تاریخ ساخت:** 2026
👨‍💻 **توسعه‌دهنده:** X-Panel Team

✨ **ویژگی‌ها:**
• مدیریت کامل اینباندها
• نمایش آمار لحظه‌ای
• شبیه‌سازی پنل پیشرفته
• رابط کاربری زیبا
• دکمه‌های اینلاین
• پشتیبانی از چند کاربر

📌 **منبع:** Open Source
"""
    bot.reply_to(message, text, parse_mode='Markdown')

# ========== دستور /status ==========
@bot.message_handler(commands=['status'])
def status_command(message):
    stats = db.get_stats()
    text = f"""
🟢 **وضعیت بات**

✅ **در حال اجرا**
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📊 **آمار:**
• 👥 کاربران: `{stats['total_users']}`
• 📋 اینباندها: `{stats['total_inbounds']}`
• 📦 ترافیک: `{stats['total_traffic']:.1f} GB`
• ⏱ آپتایم: `{stats['uptime']}`

🖥️ **سیستم:**
• CPU: `{stats['cpu']}%`
• RAM: `{stats['memory']}%`

📌 **وضعیت:** 🟢 پایدار
"""
    bot.reply_to(message, text, parse_mode='Markdown')

# ========== دستور /ping ==========
@bot.message_handler(commands=['ping'])
def ping_command(message):
    start_time = time.time()
    bot.send_chat_action(message.chat.id, 'typing')
    end_time = time.time()
    ping = (end_time - start_time) * 1000
    bot.reply_to(message, f"🏓 **Pong!**\n⏱ زمان پاسخ: `{ping:.0f} ms`", parse_mode='Markdown')

# ========== دستور /users ==========
@bot.message_handler(commands=['users'])
def users_command(message):
    users = db.users
    if not users:
        bot.reply_to(message, "📭 هیچ کاربری یافت نشد")
        return
    
    text = "👥 **لیست کاربران:**\n\n"
    for user_id, user in list(users.items())[:10]:
        text += f"• {user['name']} (🆔 {user_id}) - {user['role']}\n"
    
    text += f"\n📌 مجموع: {len(users)} کاربر"
    bot.reply_to(message, text, parse_mode='Markdown')

# ========== دستور /traffic_reset ==========
@bot.message_handler(commands=['traffic_reset'])
def traffic_reset_command(message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ فقط ادمین می‌تواند این کار را انجام دهد!")
        return
    
    for inbound in db.inbounds.values():
        inbound['traffic_used'] = 0
    
    bot.reply_to(message, "✅ **ترافیک همه اینباندها ریست شد!**")

# ========== دستور /add_sample ==========
@bot.message_handler(commands=['add_sample'])
def add_sample_command(message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ فقط ادمین می‌تواند این کار را انجام دهد!")
        return
    
    sample_names = ["USA-Server", "Germany-Server", "Singapore-Server", "Japan-Server", "UK-Server"]
    for name in sample_names:
        traffic = random.randint(50, 200)
        days = random.randint(15, 60)
        db.create_inbound(name, traffic, 5, days)
    
    bot.reply_to(message, f"✅ **{len(sample_names)} اینباند نمونه با موفقیت اضافه شد!**")

# ========== دستور /backup ==========
@bot.message_handler(commands=['backup'])
def backup_command(message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ فقط ادمین می‌تواند این کار را انجام دهد!")
        return
    
    backup_data = {
        "users": db.users,
        "inbounds": db.inbounds,
        "settings": db.settings,
        "backup_time": datetime.now().isoformat()
    }
    
    backup_file = f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(backup_file, 'w') as f:
        json.dump(backup_data, f, indent=2)
    
    with open(backup_file, 'rb') as f:
        bot.send_document(message.chat.id, f, caption="📦 **بکاپ گرفته شد!**")
    
    os.remove(backup_file)

# ========== مدیریت پیام‌های معمولی ==========
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    text = message.text.lower()
    
    if text in ["سلام", "سلامی", "درود", "hi", "hello"]:
        bot.reply_to(message, f"👋 سلام {message.from_user.first_name} جان! به X-Panel خوش آمدی!")
    
    elif text in ["خوبی", "چطوری", "حالت چطوره", "how are you"]:
        bot.reply_to(message, "🤖 من خوبم! ممنون که پرسیدی! تو چطوری؟")
    
    elif text in ["ممنون", "مرسی", "متشکرم", "thanks"]:
        bot.reply_to(message, "🙏 خواهش می‌کنم! خوشحالم که می‌تونم کمک کنم!")
    
    elif text in ["کمک", "help", "راهنما"]:
        bot.reply_to(message, "🆘 برای راهنما، /help رو بزن!")
    
    elif text in ["وضعیت", "status", "اوضاع چطوره"]:
        stats = db.get_stats()
        bot.reply_to(message, f"🟢 همه چیز عالیه!\n📊 {stats['total_inbounds']} اینباند فعال\n👥 {stats['total_users']} کاربر")
    
    else:
        bot.reply_to(message, "🤔 متوجه نشدم! برای راهنما /help رو بزن.")

# ========== اجرا با مدیریت خطا ==========
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 X-Panel Bot نسخه 3.0.0")
    print("=" * 60)
    print(f"📊 تعداد اینباندها: {len(db.inbounds)}")
    print(f"👥 ادمین‌ها: {ADMIN_IDS}")
    print("✅ برای شروع، /start رو در تلگرام بزن")
    print("=" * 60)
    
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=60)
        except Exception as e:
            print(f"❌ خطا: {e}")
            print("🔄 راه‌اندازی مجدد در 5 ثانیه...")
            time.sleep(5)
            continue
