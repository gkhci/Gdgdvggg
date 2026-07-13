import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import requests
import json
import time
from datetime import datetime

# ========== تنظیمات ==========
BOT_TOKEN = "8793482183:AAEGUa7ZEURP26N34DzKvrudnndC3q7apBk"
PANEL_URL = "https://web-production-1ca13.up.railway.app"  # آدرس پنل
PANEL_PASSWORD = "admin"

bot = telebot.TeleBot(BOT_TOKEN)
session = requests.Session()

# ========== توابع پنل ==========
def login_panel():
    try:
        url = f"{PANEL_URL}/api/login"
        response = session.post(url, json={"password": PANEL_PASSWORD}, timeout=5)
        return response.status_code == 200
    except:
        return False

def get_stats():
    try:
        if not login_panel():
            return None
        response = session.get(f"{PANEL_URL}/api/stats", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def get_inbounds():
    try:
        if not login_panel():
            return None
        response = session.get(f"{PANEL_URL}/api/inbounds", timeout=5)
        if response.status_code == 200:
            data = response.json()
            return data.get('inbounds', [])
        return None
    except:
        return None

def create_inbound(remark, traffic_limit_gb, max_ips, expiry_days):
    try:
        if not login_panel():
            return False, "ورود به پنل ناموفق"
        payload = {
            "remark": remark,
            "traffic_limit": int(traffic_limit_gb * 1073741824),
            "max_ips": int(max_ips),
            "expiry_days": int(expiry_days)
        }
        response = session.post(f"{PANEL_URL}/api/inbounds", json=payload, timeout=5)
        if response.status_code in [200, 201]:
            return True, "✅ اینباند با موفقیت ساخته شد"
        return False, f"❌ خطا: {response.text}"
    except Exception as e:
        return False, f"❌ خطا: {str(e)}"

def delete_inbound(inbound_id):
    try:
        if not login_panel():
            return False, "ورود به پنل ناموفق"
        response = session.delete(f"{PANEL_URL}/api/inbounds/{inbound_id}", timeout=5)
        if response.status_code in [200, 204]:
            return True, "✅ اینباند حذف شد"
        return False, f"❌ خطا: {response.text}"
    except Exception as e:
        return False, f"❌ خطا: {str(e)}"

def format_bytes(bytes_val):
    if bytes_val < 1024:
        return f"{bytes_val} B"
    elif bytes_val < 1024 * 1024:
        return f"{bytes_val/1024:.1f} KB"
    elif bytes_val < 1024 * 1024 * 1024:
        return f"{bytes_val/(1024*1024):.1f} MB"
    else:
        return f"{bytes_val/(1024*1024*1024):.2f} GB"

# ========== دستورات بات ==========
@bot.message_handler(commands=['start'])
def start_command(message):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("📊 آمار", callback_data="stats"),
        InlineKeyboardButton("📋 اینباندها", callback_data="list"),
        InlineKeyboardButton("➕ افزودن", callback_data="add_menu"),
        InlineKeyboardButton("🔄 بروزرسانی", callback_data="refresh")
    )
    
    bot.send_message(
        message.chat.id,
        "🤖 **مدیریت پنل Luffy**\n\n"
        "سلام! به بات مدیریت پنل خوش آمدید.\n"
        "از دکمه‌های زیر استفاده کنید:",
        reply_markup=keyboard,
        parse_mode='Markdown'
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    if call.data == "stats":
        show_stats(call.message)
    elif call.data == "list":
        show_inbounds(call.message)
    elif call.data == "add_menu":
        bot.send_message(
            call.message.chat.id,
            "📝 **افزودن اینباند جدید**\n\n"
            "فرمت:\n"
            "`/add [نام] [ترافیک_GB] [حداکثر_IP] [روز_اعتبار]`\n\n"
            "مثال:\n"
            "`/add کاربر1 100 5 30`",
            parse_mode='Markdown'
        )
    elif call.data.startswith("delete_"):
        inbound_id = call.data.split("_")[1]
        success, msg = delete_inbound(inbound_id)
        bot.answer_callback_query(call.id, msg)
        if success:
            show_inbounds(call.message)
    elif call.data == "refresh":
        bot.answer_callback_query(call.id, "🔄 بروزرسانی شد")

def show_stats(message):
    stats = get_stats()
    if not stats:
        bot.send_message(message.chat.id, "❌ دریافت آمار ناموفق")
        return
    
    text = f"📊 **آمار پنل**\n"
    text += f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    text += f"🖥️ CPU: `{stats.get('cpu', '0')}%`\n"
    text += f"🧠 Memory: `{stats.get('memory', '0')}%`\n"
    text += f"🌐 Domain: `{stats.get('domain', 'نامشخص')}`\n"
    text += f"📦 ترافیک: `{format_bytes(stats.get('total_traffic', 0))}`\n"
    text += f"📋 اینباندها: `{stats.get('inbounds_count', 0)}`\n"
    text += f"⏱️ Uptime: `{stats.get('uptime', 'نامشخص')}`"
    
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

def show_inbounds(message):
    inbounds = get_inbounds()
    if inbounds is None:
        bot.send_message(message.chat.id, "❌ دریافت لیست اینباندها ناموفق")
        return
    
    if not inbounds:
        bot.send_message(message.chat.id, "📭 هیچ اینباندی یافت نشد")
        return
    
    text = "📋 **لیست اینباندها:**\n\n"
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    for item in inbounds[:15]:
        name = item.get('remark', 'بدون نام')
        usage = item.get('usage', 0)
        status = "✅" if item.get('status', False) else "❌"
        expiry = item.get('expiry', 'نامحدود')
        inbound_id = item.get('id')
        
        text += f"**{name}** {status}\n"
        text += f"📊 مصرف: `{format_bytes(usage)}`\n"
        text += f"📅 انقضا: `{expiry}`\n\n"
        
        if inbound_id:
            keyboard.add(
                InlineKeyboardButton(f"🗑️ {name}", callback_data=f"delete_{inbound_id}")
            )
    
    keyboard.add(InlineKeyboardButton("➕ افزودن جدید", callback_data="add_menu"))
    
    bot.send_message(message.chat.id, text, reply_markup=keyboard, parse_mode='Markdown')

@bot.message_handler(commands=['add'])
def add_command(message):
    args = message.text.split()
    if len(args) != 5:
        bot.reply_to(
            message,
            "⚠️ **فرمت صحیح:**\n"
            "`/add [نام] [ترافیک_GB] [حداکثر_IP] [روز_اعتبار]`\n\n"
            "مثال:\n"
            "`/add کاربر1 100 5 30`",
            parse_mode='Markdown'
        )
        return
    
    try:
        _, remark, traffic, max_ips, days = args
        traffic = float(traffic)
        max_ips = int(max_ips)
        days = int(days)
        
        if traffic <= 0 or max_ips <= 0 or days <= 0:
            bot.reply_to(message, "❌ همه مقادیر باید مثبت باشند")
            return
        
        bot.reply_to(message, "⏳ در حال ساخت اینباند...")
        success, msg = create_inbound(remark, traffic, max_ips, days)
        bot.reply_to(message, msg)
        if success:
            show_inbounds(message)
            
    except ValueError:
        bot.reply_to(message, "❌ مقادیر عددی را درست وارد کنید")
    except Exception as e:
        bot.reply_to(message, f"❌ خطا: {str(e)}")

@bot.message_handler(commands=['help'])
def help_command(message):
    text = """
📚 **راهنمای بات**

**دستورات:**
`/start` - منوی اصلی
`/stats` - آمار پنل
`/list` - لیست اینباندها
`/add [نام] [ترافیک_GB] [IP] [روز]` - افزودن اینباند
`/help` - این راهنما

**دکمه‌ها:**
• 🗑️ - حذف اینباند
• ➕ - افزودن اینباند جدید

**نکته:** برای استفاده از دکمه‌ها، پیام‌ها را بروزرسانی کنید.
"""
    bot.send_message(message.chat.id, text, parse_mode='Markdown')

# ========== اجرا ==========
if __name__ == "__main__":
    print("🤖 بات در حال اجراست...")
    print("✅ برای شروع، /start رو در تلگرام بزن")
    
    try:
        bot.polling(none_stop=True, interval=0)
    except Exception as e:
        print(f"❌ خطا: {e}")
        print("🔄 راه‌اندازی مجدد...")
        time.sleep(3)
        bot.polling(none_stop=True, interval=0)
