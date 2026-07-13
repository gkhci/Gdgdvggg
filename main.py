import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json
import time
import random
from datetime import datetime, timedelta
import os

# ========== تنظیمات ==========
BOT_TOKEN = "8793482183:AAEGUa7ZEURP26N34DzKvrudnndC3q7apBk"
ADMIN_IDS [8680457924]  # آیدی عددی خودت رو بذار

bot = telebot.TeleBot(BOT_TOKEN)

# ========== دیتابیس ==========
class Database:
    def __init__(self):
        self.users = {}
        self.inbounds = {}
        self.settings = {
            "panel_name": "Luffy Panel",
            "version": "3.0.0",
            "domain": "web-production-1ca13.up.railway.app",
            "uptime": time.time()
        }
        self._init_sample_data()
    
    def _init_sample_data(self):
        sample_inbounds = [
            {"id": "1", "name": "Luffy-1", "traffic_limit": 100, "traffic_used": 23.5, "status": "فعال", "expiry": "2026-12-31"},
            {"id": "2", "name": "Luffy-2", "traffic_limit": 200, "traffic_used": 45.2, "status": "فعال", "expiry": "2026-11-15"},
            {"id": "3", "name": "Luffy-3", "traffic_limit": 150, "traffic_used": 12.8, "status": "فعال", "expiry": "2027-01-20"},
            {"id": "4", "name": "Luffy-4", "traffic_limit": 80, "traffic_used": 5.3, "status": "غیرفعال", "expiry": "2026-09-10"},
            {"id": "5", "name": "Luffy-5", "traffic_limit": 120, "traffic_used": 67.1, "status": "فعال", "expiry": "2026-10-05"},
        ]
        for inbound in sample_inbounds:
            self.inbounds[inbound["id"]] = inbound
    
    def add_user(self, user_id, name):
        if user_id not in self.users:
            self.users[user_id] = {
                "name": name,
                "role": "admin" if user_id in ADMIN_IDS else "user",
                "joined": datetime.now().isoformat()
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
            "name": name,
            "traffic_limit": traffic_limit,
            "traffic_used": 0,
            "max_ips": max_ips,
            "status": "فعال",
            "expiry": expiry,
            "created": datetime.now().isoformat()
        }
        self.inbounds[inbound_id] = inbound
        return inbound
    
    def delete_inbound(self, inbound_id):
        if inbound_id in self.inbounds:
            del self.inbounds[inbound_id]
            return True
        return False

db = Database()

# ========== شبیه‌سازی کانفیگ Luffy ==========
def generate_luffy_config(inbound_name, inbound_id):
    """تولید کانفیگ با فرمت دقیق پنل Luffy"""
    domain = "web-production-1ca13.up.railway.app"
    port = 443
    path = f"/ws/{inbound_id}"
    
    protocol = random.choice(["vless", "vmess", "trojan"])
    uuid = f"{random.randint(10000000, 99999999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(10000000, 99999999)}"
    
    if protocol == "vless":
        config = f"vless://{uuid}@{domain}:{port}?encryption=none&security=tls&type=ws&host={domain}&path={path}&sni={domain}&fp=chrome&alpn=http/1.1#{inbound_name}"
    elif protocol == "vmess":
        config = f"vmess://{uuid}@{domain}:{port}?security=tls&type=ws&host={domain}&path={path}&sni={domain}&fp=chrome&alpn=http/1.1#{inbound_name}"
    else:
        config = f"trojan://{uuid}@{domain}:{port}?security=tls&type=ws&host={domain}&path={path}&sni={domain}&fp=chrome&alpn=http/1.1#{inbound_name}"
    
    return config

def generate_all_links(inbound_name, inbound_id):
    """تولید همه لینک‌ها"""
    domain = "web-production-1ca13.up.railway.app"
    port = 443
    path = f"/ws/{inbound_id}"
    uuid = f"{random.randint(10000000, 99999999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(10000000, 99999999)}"
    
    return {
        "vless": f"vless://{uuid}@{domain}:{port}?encryption=none&security=tls&type=ws&host={domain}&path={path}&sni={domain}&fp=chrome&alpn=http/1.1#{inbound_name}",
        "vmess": f"vmess://{uuid}@{domain}:{port}?security=tls&type=ws&host={domain}&path={path}&sni={domain}&fp=chrome&alpn=http/1.1#{inbound_name}",
        "trojan": f"trojan://{uuid}@{domain}:{port}?security=tls&type=ws&host={domain}&path={path}&sni={domain}&fp=chrome&alpn=http/1.1#{inbound_name}"
    }

# ========== کیبوردها ==========
def main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("📊 داشبورد", callback_data="dashboard"),
        InlineKeyboardButton("📋 اینباندها", callback_data="list_inbounds"),
        InlineKeyboardButton("➕ افزودن اینباند", callback_data="add_inbound"),
        InlineKeyboardButton("🔗 کانفیگ من", callback_data="my_config"),
        InlineKeyboardButton("📈 ترافیک", callback_data="traffic"),
        InlineKeyboardButton("👤 پروفایل", callback_data="profile"),
        InlineKeyboardButton("🔄 بروزرسانی", callback_data="refresh"),
        InlineKeyboardButton("🆘 راهنما", callback_data="help")
    )
    return keyboard

# ========== دستورات ==========
@bot.message_handler(commands=['start'])
def start_command(message):
    user_id = message.from_user.id
    name = message.from_user.first_name
    db.add_user(user_id, name)
    
    welcome = f"""
🌟 **به پنل Luffy خوش آمدید!**

👤 کاربر: {name}
🆔 آیدی: {user_id}
👑 نقش: {'ادمین' if user_id in ADMIN_IDS else 'کاربر'}

📌 از دکمه‌های زیر استفاده کنید:
"""
    bot.send_message(
        message.chat.id,
        welcome,
        reply_markup=main_menu(),
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    user_id = call.from_user.id
    
    # --- داشبورد ---
    if call.data == "dashboard":
        stats = db.get_stats()
        text = f"""
📊 **داشبورد Luffy Panel**

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
            "`/add Luffy-6 150 5 30`",
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )
    
    # --- کانفیگ من ---
    elif call.data == "my_config":
        inbounds = list(db.inbounds.values())
        if not inbounds:
            bot.answer_callback_query(call.id, "❌ هیچ اینباندی یافت نشد")
            return
        
        # انتخاب یک اینباند تصادفی
        inbound = random.choice(inbounds)
        config = generate_luffy_config(inbound['name'], inbound['id'])
        
        text = f"""
🔐 **کانفیگ شما**

📛 نام: {inbound['name']}
🆔 شناسه: {inbound['id']}

📌 **لینک کانفیگ:**
`{config}`

📥 روی لینک کلیک کن تا کپی بشه!
"""
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "🔗 کانفیگ شما")
    
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
        
        bot.edit_message_text(
            text,
            call.message.chat.id,
            call.message.message_id,
            reply_markup=main_menu(),
            parse_mode='Markdown'
        )
        bot.answer_callback_query(call.id, "📊 آمار ترافیک")
    
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
🔗 کانفیگ من - دریافت کانفیگ
📈 ترافیک - آمار مصرف
👤 پروفایل - اطلاعات کاربر

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
        inbound = db.inbounds.get(inbound_id)
        if inbound:
            config = generate_luffy_config(inbound['name'], inbound_id)
            bot.answer_callback_query(call.id, "🔗 کانفیگ کپی شد")
            bot.send_message(
                call.message.chat.id,
                f"🔗 **کانفیگ {inbound['name']}:**\n`{config}`",
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
            bot.answer_callback_query(call.id, f"⏸️ اینباند {inbound['status']} شد")
            show_inbounds(call)
        else:
            bot.answer_callback_query(call.id, "❌ اینباند یافت نشد")
    
    elif call.data.startswith("links_"):
        inbound_id = call.data.split("_")[1]
        inbound = db.inbounds.get(inbound_id)
        if inbound:
            links = generate_all_links(inbound['name'], inbound_id)
            text = f"""
🔗 **لینک‌های {inbound['name']}**

**VLESS:**
`{links['vless']}`

**VMESS:**
`{links['vmess']}`

**Trojan:**
`{links['trojan']}`

📌 هر کدوم رو که می‌خوای کپی کن!
"""
            bot.answer_callback_query(call.id, "🔗 لینک‌ها")
            bot.send_message(
                call.message.chat.id,
                text,
                parse_mode='Markdown'
            )
        else:
            bot.answer_callback_query(call.id, "❌ اینباند یافت نشد")

def show_inbounds(call):
    inbounds = list(db.inbounds.values())
    
    if not inbounds:
        bot.edit_message_text(
            "📭 **هیچ اینباندی یافت نشد**",
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
        text += f"📅 انقضا: `{item['expiry']}`\n"
        text += f"🆔 {item['id']}\n\n"
        
        if item['id']:
            keyboard.add(
                InlineKeyboardButton(f"🔗 کانفیگ", callback_data=f"link_{item['id']}"),
                InlineKeyboardButton(f"🔗 همه لینک‌ها", callback_data=f"links_{item['id']}"),
                InlineKeyboardButton(f"🗑️ حذف", callback_data=f"delete_{item['id']}"),
                InlineKeyboardButton(f"⏸️ {item['status']}", callback_data=f"disable_{item['id']}")
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
    bot.answer_callback_query(call.id, "📋 لیست اینباندها")

# ========== دستورات متنی ==========
@bot.message_handler(commands=['add'])
def add_command(message):
    args = message.text.split()
    if len(args) != 5:
        bot.reply_to(
            message,
            "⚠️ **فرمت صحیح:**\n"
            "`/add [نام] [ترافیک_GB] [حداکثر_IP] [روز_اعتبار]`\n\n"
            "مثال:\n"
            "`/add Luffy-6 150 5 30`",
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
        
        inbound = db.create_inbound(name, traffic, max_ips, days)
        
        text = f"""
✅ **اینباند ساخته شد!**

📛 نام: {inbound['name']}
📊 ترافیک: {inbound['traffic_limit']} GB
👥 حداکثر IP: {inbound['max_ips']}
📅 انقضا: {inbound['expiry']}
🆔 شناسه: {inbound['id']}
"""
        bot.reply_to(message, text, parse_mode='Markdown')
        
        # نمایش کانفیگ
        config = generate_luffy_config(inbound['name'], inbound['id'])
        bot.send_message(
            message.chat.id,
            f"🔗 **کانفیگ:**\n`{config}`",
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
📊 **آمار پنل Luffy**

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
        text += f"{status} {item['name']}: `{item['traffic_used']:.1f}/{item['traffic_limit']} GB` - {item['status']}\n"
    
    text += f"\n📌 {len(inbounds)} اینباند در سیستم وجود دارد."
    bot.reply_to(message, text, parse_mode='Markdown')

@bot.message_handler(commands=['help'])
def help_command(message):
    text = """
📚 **راهنمای کامل Luffy Panel**

**دستورات:**
/start - منوی اصلی
/add [نام] [ترافیک] [IP] [روز] - افزودن اینباند
/stats - آمار پنل
/list - لیست اینباندها
/help - این راهنما

**دکمه‌ها:**
📊 داشبورد - مشاهده آمار کلی
📋 اینباندها - مدیریت اینباندها
➕ افزودن - ساخت اینباند جدید
🔗 کانفیگ من - دریافت کانفیگ
📈 ترافیک - آمار مصرف
👤 پروفایل - اطلاعات کاربر

**ویژگی‌ها:**
✅ شبیه‌سازی دقیق کانفیگ Luffy
✅ پشتیبانی از VLESS/VMESS/Trojan
✅ لینک‌های با فرمت اصلی
✅ مدیریت کامل اینباندها
"""
    bot.reply_to(message, text, parse_mode='Markdown')

# ========== اجرا ==========
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Luffy Panel Bot")
    print("=" * 60)
    print(f"📊 تعداد اینباندها: {len(db.inbounds)}")
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
            # ========== ادامه دستورات متنی ==========

# ========== دستور /ping ==========
@bot.message_handler(commands=['ping'])
def ping_command(message):
    start_time = time.time()
    bot.send_chat_action(message.chat.id, 'typing')
    end_time = time.time()
    ping = (end_time - start_time) * 1000
    bot.reply_to(message, f"🏓 **Pong!**\n⏱ زمان پاسخ: `{ping:.0f} ms`", parse_mode='Markdown')

# ========== دستور /status ==========
@bot.message_handler(commands=['status'])
def status_command(message):
    stats = db.get_stats()
    text = f"""
🟢 **وضعیت بات Luffy Panel**

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

# ========== دستور /users ==========
@bot.message_handler(commands=['users'])
def users_command(message):
    user_id = message.from_user.id
    if user_id not in ADMIN_IDS:
        bot.reply_to(message, "⛔ فقط ادمین می‌تواند این کار را انجام دهد!")
        return
    
    users = db.users
    if not users:
        bot.reply_to(message, "📭 هیچ کاربری یافت نشد")
        return
    
    text = "👥 **لیست کاربران:**\n\n"
    for user_id, user in list(users.items())[:10]:
        text += f"• {user['name']} (🆔 {user_id}) - {user['role']}\n"
    
    text += f"\n📌 مجموع: {len(users)} کاربر"
    bot.reply_to(message, text, parse_mode='Markdown')

# ========== دستور /reset_traffic ==========
@bot.message_handler(commands=['reset_traffic'])
def reset_traffic_command(message):
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
    
    sample_names = ["Luffy-US", "Luffy-DE", "Luffy-SG", "Luffy-JP", "Luffy-UK"]
    for name in sample_names:
        traffic = random.randint(50, 200)
        days = random.randint(15, 60)
        db.create_inbound(name, traffic, 5, days)
    
    bot.reply_to(message, f"✅ **{len(sample_names)} اینباند نمونه اضافه شد!**")

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
    
    if text in ["سلام", "سلامی", "درود", "hi", "hello", "سلام عليكم"]:
        bot.reply_to(message, f"👋 سلام {message.from_user.first_name} جان! به Luffy Panel خوش آمدی!")
    
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
            config = generate_luffy_config(inbound['name'], inbound['id'])
            bot.reply_to(message, f"🔗 **کانفیگ {inbound['name']}:**\n`{config}`", parse_mode='Markdown')
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
        # پاسخ هوشمندانه به پیام‌های ناشناخته
        responses = [
            "🤔 متوجه نشدم! برای راهنما /help رو بزن.",
            "😅 منظورت رو کامل متوجه نشدم! لطفاً واضح‌تر بگو.",
            "🧐 اینو نمی‌دونم! از منوی دکمه‌ها استفاده کن.",
            "📌 برای دیدن راهنما، /help رو بزن.",
            "🤖 من یه بات ساده هستم! دستورات رو ببین."
        ]
        bot.reply_to(message, random.choice(responses))

# ========== اجرا با مدیریت خطا ==========
if __name__ == "__main__":
    print("=" * 60)
    print("🚀 Luffy Panel Bot نسخه 3.0.0")
    print("=" * 60)
    print(f"📊 تعداد اینباندها: {len(db.inbounds)}")
    print(f"👥 ادمین‌ها: {ADMIN_IDS}")
    print(f"🌐 دامنه: {db.settings['domain']}")
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
