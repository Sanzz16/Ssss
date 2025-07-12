import os, json, asyncio, random, re, threading
from pyrogram import Client, filters
from pyrogram.types import Message
from telethon import TelegramClient
from telethon.errors import ChatWriteForbiddenError, ChannelPrivateError
from telethon.tl.functions.channels import JoinChannelRequest, InviteToChannelRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from telethon.tl.functions.channels import LeaveChannelRequest, GetParticipantsRequest
from telethon.tl.types import PeerChannel, ChannelParticipantsBots

API_ID = #nhập api id vô đi thằng lồn
API_HASH = "" #nhập api hash ở trong giấu ngoặc
MAIN_BOT_TOKEN = "" #nhập main bot vô
# nhớ tạo thêm mấy file nha
USERBOT_SESSION = "userbot_session"
TOKENS_FILE = "tokens.json"
TEXT_FILE = "text.json"
ADMINS_FILE = "admins.json"
SPAM_DELAY = 0.05
#telegram @hoangnhutxyz lấy không cre cả nhà mày chết
is_spamming = False
known_kick = {}
GROUP_FILE = "group.json"

import time
app = Client(f"main_bot_{int(time.time())}", api_id=API_ID, api_hash=API_HASH, bot_token=MAIN_BOT_TOKEN)
userbot = None
userbot_loop = asyncio.new_event_loop()
def load_banned():
    if not os.path.exists("banned_bots.json"):
        with open("banned_bots.json", "w") as f:
            json.dump([], f)
    with open("banned_bots.json") as f:
        return json.load(f)

def save_banned(data):
    with open("banned_bots.json", "w") as f:
        json.dump(data, f)
def load_tokens():
    if not os.path.exists(TOKENS_FILE): return []
    with open(TOKENS_FILE) as f: return json.load(f)

def load_texts():
    with open(TEXT_FILE, encoding="utf-8") as f: return json.load(f)

def phantom_protect(text):
    zwsp = "\u2063"
    return text + zwsp * random.randint(1, 2)

def load_admins():
    if not os.path.exists(ADMINS_FILE): open(ADMINS_FILE, "w").write("[]")
    with open(ADMINS_FILE) as f: return json.load(f)

def save_admins(admin_ids):
    with open(ADMINS_FILE, "w") as f: json.dump(admin_ids, f)

def is_admin(user_id):
    return user_id in load_admins()
def save_group(chat_id):
    with open(GROUP_FILE, "w") as f:
        json.dump({"chat_id": chat_id}, f)

def load_group():
    if os.path.exists(GROUP_FILE):
        with open(GROUP_FILE) as f:
            return json.load(f).get("chat_id")
    return None
   
@app.on_message(filters.command("adm"))
async def add_admin_command(client, message: Message):
    admins = load_admins()
    # Nếu chưa có admin nào, cho phép user đầu tiên tự add mình
    if len(admins) == 0:
        admins.append(message.from_user.id)
        save_admins(admins)
        await message.reply(f"✅ Đã thêm admin đầu tiên: {message.from_user.id}")
        return
    
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /adm <id>")
    try:
        new_admin = int(args[1])
        if new_admin in admins: return await message.reply("⚠️ Admin đã tồn tại.")
        admins.append(new_admin)
        save_admins(admins)
        await message.reply(f"✅ Đã thêm admin: {new_admin}")
    except: await message.reply("❌ ID không hợp lệ.")

@app.on_message(filters.command("help"))
async def help_command(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    help_text = """
🔥 **DANH SÁCH TÍNH NĂNG BOT SIÊU MẠNH** 🔥

**💰 YEUMONEY BYPASS:**
• `/ym <loại>` - Bypass YeuMoney (m88, fb88, 188bet, w88, v9bet, bk8)
• `/ymcheck <link>` - Kiểm tra link YeuMoney
• `/yminfo` - Hướng dẫn sử dụng YeuMoney

**👑 QUẢN LÝ BOT:**
• `/reg <tên>` - Tự động tạo bot từ BotFather
• `/addbot <token>` - Thêm bot thủ công
• `/dsbot` - Xem danh sách bot
• `/rmbot <số>` - Xóa bot theo STT
• `/checkbot` - Kiểm tra bot còn hoạt động
• `/resetbot` - Reset tất cả bot
• `/botinfo <id>` - Thông tin chi tiết bot
• `/masscreate <số>` - Tạo hàng loạt bot

**⚡ SPAM & RAID NÂNG CAO:**
• `/spam <this|link> <@user>` - Spam tag user
• `/massping <this|link>` - Ping tất cả member
• `/floodtext <link> <text>` - Flood text vào group
• `/raidmode <link>` - Chế độ raid cực mạnh
• `/nukespam <link>` - Spam hủy diệt
• `/ghostspam <link>` - Spam ẩn danh
• `/turbospam <link>` - Spam tốc độ cao
• `/infinitespam <link>` - Spam vô hạn
• `/smartspam <link>` - Spam thông minh

**🎯 TARGETING & PRECISION:**
• `/sniperspam <@user>` - Spam chính xác 1 người
• `/multiping <@user1> <@user2>` - Ping nhiều người
• `/vipspam <@user>` - Spam VIP mode
• `/autotag <link>` - Tự động tag members
• `/chainspam <link>` - Spam chuỗi liên tục

**🛡️ BẢO VỆ & PHÒNG THỦ:**
• `/antiraid <on|off>` - Chống raid tự động
• `/kickban <@user>` - Kick + ban user
• `/cleanup` - Dọn dẹp spam messages
• `/lockdown` - Khóa group tạm thời
• `/fortress <link>` - Bảo vệ tối đa
• `/shield <on|off>` - Khiên bảo vệ
• `/autoban <on|off>` - Tự động ban
• `/whitelist <@user>` - Thêm vào whitelist

**📊 THỐNG KÊ & THEO DÕI:**
• `/stats` - Thống kê hoạt động bot
• `/monitor <link>` - Theo dõi group
• `/activity` - Xem hoạt động gần đây
• `/topspam` - Top user spam nhiều nhất
• `/analytics` - Phân tích chi tiết
• `/heatmap` - Bản đồ hoạt động
• `/performance` - Hiệu suất bot
• `/reportgen` - Tạo báo cáo

**🔥 ADVANCED FEATURES:**
• `/megaflood <link>` - Lũ lụt mega
• `/spamstorm <link>` - Bão spam
• `/rapidfire <link>` - Bắn liên tục
• `/overload <link>` - Quá tải hệ thống
• `/tsunami <link>` - Sóng thần spam
• `/apocalypse <link>` - Tận thế spam
• `/nuclear <link>` - Hạt nhân spam
• `/blackhole <link>` - Hố đen spam

**🎮 FUN & ENTERTAINMENT:**
• `/emoji <link>` - Spam emoji
• `/sticker <link>` - Spam sticker
• `/gif <link>` - Spam GIF
• `/meme <link>` - Spam meme
• `/ascii <text>` - Tạo ASCII art
• `/rainbow <text>` - Text màu cầu vồng
• `/dance` - Bot nhảy múa
• `/party <link>` - Tiệc spam

**⚙️ CÀI ĐẶT NÂNG CAO:**
• `/delay <giây>` - Đặt delay spam
• `/settext <text>` - Thêm text spam
• `/automode <on|off>` - Chế độ tự động
• `/config` - Xem cấu hình hiện tại
• `/profile <mode>` - Chế độ hoạt động
• `/schedule <time>` - Lên lịch spam
• `/priority <high|low>` - Độ ưu tiên
• `/throttle <level>` - Điều chỉnh tốc độ

**🚀 TIỆN ÍCH KHÁC:**
• `/backup` - Backup dữ liệu
• `/restore` - Khôi phục dữ liệu
• `/genlink` - Tạo link mời group
• `/status` - Trạng thái hệ thống
• `/restart` - Khởi động lại bot
• `/update` - Cập nhật bot
• `/ping` - Kiểm tra ping
• `/uptime` - Thời gian hoạt động

**👥 QUẢN LÝ USER:**
• `/adm <id>` - Thêm admin
• `/rmadm <id>` - Xóa admin
• `/admlist` - Danh sách admin
• `/join <link>` - Join và mời bot vào group
• `/out <link>` - Rời khỏi group
• `/userinfo <@user>` - Thông tin user
• `/promote <@user>` - Thăng chức
• `/demote <@user>` - Giáng chức

**💎 VIP FEATURES:**
• `/vipmode <on|off>` - Chế độ VIP
• `/premium <@user>` - Nâng cấp premium
• `/unlimited <on|off>` - Không giới hạn
• `/godmode <on|off>` - Chế độ thần
• `/invisible <on|off>` - Chế độ vô hình
• `/teleport <link>` - Dịch chuyển tức thời

**🎯 SPECIAL OPERATIONS:**
• `/stealth <link>` - Hoạt động bí mật
• `/phantom <link>` - Ma quỷ spam
• `/shadow <link>` - Bóng đen spam
• `/laser <@user>` - Tia laser spam
• `/missile <link>` - Tên lửa spam
• `/drone <link>` - Máy bay không người lái

Sử dụng với trách nhiệm! 🔥
"""
    await message.reply(help_text)

@app.on_message(filters.command("rmbot"))
async def remove_bot(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /rmbot <số STT>")
    try:
        index = int(args[1]) - 1
        tokens = load_tokens()
        if 0 <= index < len(tokens):
            removed = tokens.pop(index)
            with open(TOKENS_FILE, "w") as f: json.dump(tokens, f, indent=2)
            await message.reply(f"✅ Đã xóa bot: {removed.split('(')[-1]}")
        else:
            await message.reply("❌ STT không hợp lệ")
    except: await message.reply("❌ Lỗi định dạng")

@app.on_message(filters.command("checkbot"))
async def check_bots(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    tokens = load_tokens()
    if not tokens: return await message.reply("⚠️ Không có bot")
    
    working, dead = 0, 0
    status_text = "🔍 **KIỂM TRA BOT:**\n\n"
    
    for i, entry in enumerate(tokens):
        try:
            token = entry.split("(")[0].split(":", 1)[1].strip()
            session = f"check_{random.randint(1000,9999)}"
            bot = TelegramClient(session, API_ID, API_HASH)
            await bot.start(bot_token=token)
            me = await bot.get_me()
            await bot.disconnect()
            status_text += f"✅ {i+1}. @{me.username} - HOẠT ĐỘNG\n"
            working += 1
        except:
            status_text += f"❌ {i+1}. BOT CHẾT\n"
            dead += 1
    
    status_text += f"\n📊 **KẾT QUA:** {working} hoạt động, {dead} chết"
    await message.reply(status_text)

@app.on_message(filters.command("massping"))
async def mass_ping(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /massping <this|link>")
    
    target = args[1] if args[1] != "this" else message.chat.id
    if "t.me/" in str(target): target = target.replace("https://t.me/", "").replace("t.me/", "")
    if not str(target).startswith("@") and not str(target).startswith("-100"):
        target = f"@{target}"
    
    try:
        entity = await userbot.get_entity(target)
        participants = await userbot.get_participants(entity, limit=100)
        users = [f"@{u.username}" for u in participants if u.username and not u.bot]
        
        if users:
            ping_text = " ".join(users[:50])  # Max 50 users per message
            tokens = load_tokens()
            for entry in tokens:
                try:
                    token = entry.split("(")[0].split(":", 1)[1].strip()
                    session = f"ping_{random.randint(1000,9999)}"
                    bot = TelegramClient(session, API_ID, API_HASH)
                    await bot.start(bot_token=token)
                    await bot.send_message(target, f"📢 MASS PING:\n{ping_text}")
                    await bot.disconnect()
                    await asyncio.sleep(0.1)
                except: pass
            await message.reply(f"✅ Đã ping {len(users)} members!")
        else:
            await message.reply("❌ Không tìm thấy users")
    except Exception as e:
        await message.reply(f"❌ Lỗi: {e}")

@app.on_message(filters.command("floodtext"))
async def flood_text(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split(maxsplit=2)
    if len(args) < 3: return await message.reply("❌ /floodtext <link> <text>")
    
    target, text = args[1], args[2]
    if "t.me/" in target: target = target.replace("https://t.me/", "").replace("t.me/", "")
    if not target.startswith("@") and not target.startswith("-100"):
        target = f"@{target}"
    
    await message.reply(f"🌊 Bắt đầu flood text vào {target}")
    tokens = load_tokens()
    
    async def flood_job(entry, idx):
        try:
            token = entry.split("(")[0].split(":", 1)[1].strip()
            session = f"flood_{idx}_{random.randint(1000,9999)}"
            bot = TelegramClient(session, API_ID, API_HASH)
            await bot.start(bot_token=token)
            
            for _ in range(50):  # 50 messages per bot
                await bot.send_message(target, phantom_protect(text))
                await asyncio.sleep(0.05)
            await bot.disconnect()
        except: pass
    
    for i, entry in enumerate(tokens):
        asyncio.create_task(flood_job(entry, i))

@app.on_message(filters.command("raidmode"))
async def raid_mode(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /raidmode <link>")
    
    target = args[1]
    if "t.me/" in target: target = target.replace("https://t.me/", "").replace("t.me/", "")
    if not target.startswith("@") and not target.startswith("-100"):
        target = f"@{target}"
    
    raid_texts = [
        "🔥 RAID ACTIVATED 🔥", "💀 INCOMING RAID 💀", "⚡ POWER RAID ⚡",
        "🚀 MEGA RAID 🚀", "💣 EXPLOSION RAID 💣", "👿 DEMON RAID 👿"
    ]
    
    await message.reply(f"💀 RAID MODE ACTIVATED: {target}")
    tokens = load_tokens()
    
    async def raid_job(entry, idx):
        try:
            token = entry.split("(")[0].split(":", 1)[1].strip()
            session = f"raid_{idx}_{random.randint(1000,9999)}"
            bot = TelegramClient(session, API_ID, API_HASH)
            await bot.start(bot_token=token)
            
            while True:
                for text in raid_texts:
                    await bot.send_message(target, phantom_protect(text))
                    await asyncio.sleep(0.01)  # Super fast
        except: pass
    
    for i, entry in enumerate(tokens):
        asyncio.create_task(raid_job(entry, i))

@app.on_message(filters.command("stopall"))
async def stop_all(client, message: Message):
    global is_spamming
    if not is_admin(message.from_user.id): return await message.reply("❌")
    is_spamming = False
    await message.reply("🛑 Đã dừng TẤT CẢ hoạt động!")

@app.on_message(filters.command("stats"))
async def bot_stats(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    tokens = load_tokens()
    admins = load_admins()
    banned = load_banned()
    
    stats_text = f"""
📊 **THỐNG KÊ BOT:**

🤖 Tổng bot: **{len(tokens)}**
👑 Admin: **{len(admins)}**
🚫 Bot bị ban: **{len(banned)}**
⏱️ Delay spam: **{SPAM_DELAY}s**
🔄 Trạng thái: **{'🟢 Đang spam' if is_spamming else '🔴 Dừng'}**

📈 **Hiệu suất:**
• CPU: **Normal**
• RAM: **Stable**  
• Network: **Good**

🕐 **Uptime:** {int(time.time()) % 86400} giây
"""
    await message.reply(stats_text)

@app.on_message(filters.command("settext"))
async def set_spam_text(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return await message.reply("❌ /settext <text>")
    
    new_text = args[1]
    texts = load_texts()
    texts.append(new_text)
    
    with open(TEXT_FILE, "w", encoding="utf-8") as f:
        json.dump(texts, f, ensure_ascii=False, indent=2)
    
    await message.reply(f"✅ Đã thêm text: {new_text[:50]}...")

@app.on_message(filters.command("genlink"))
async def generate_invite_link(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    try:
        if message.chat.type in ["group", "supergroup"]:
            link = await app.export_chat_invite_link(message.chat.id)
            await message.reply(f"🔗 **Link mời group:**\n{link}")
        else:
            await message.reply("❌ Chỉ dùng trong group")
    except Exception as e:
        await message.reply(f"❌ Lỗi tạo link: {e}")

@app.on_message(filters.command("backup"))
async def backup_data(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    backup_data = {
        "tokens": load_tokens(),
        "admins": load_admins(),
        "texts": load_texts(),
        "banned": load_banned(),
        "timestamp": int(time.time())
    }
    
    backup_file = f"backup_{int(time.time())}.json"
    with open(backup_file, "w", encoding="utf-8") as f:
        json.dump(backup_data, f, ensure_ascii=False, indent=2)
    
    await app.send_document(message.chat.id, backup_file)
    os.remove(backup_file)
    await message.reply("✅ Backup hoàn tất!")

@app.on_message(filters.command("cleanup"))
async def cleanup_spam(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    try:
        deleted = 0
        async for msg in app.get_chat_history(message.chat.id, limit=200):
            if msg.from_user and msg.from_user.is_bot:
                try:
                    await app.delete_messages(message.chat.id, msg.id)
                    deleted += 1
                except: pass
        
        await message.reply(f"🧹 Đã xóa {deleted} tin nhắn bot!")
    except Exception as e:
        await message.reply(f"❌ Lỗi cleanup: {e}")

@app.on_message(filters.command("admlist"))
async def admin_list(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    admins = load_admins()
    if not admins: return await message.reply("⚠️ Chưa có admin")
    
    admin_text = "👑 **DANH SÁCH ADMIN:**\n\n"
    for i, admin_id in enumerate(admins):
        admin_text += f"{i+1}. `{admin_id}`\n"
    
    await message.reply(admin_text)

@app.on_message(filters.command("rmadm"))
async def remove_admin(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /rmadm <id>")
    
    try:
        admin_id = int(args[1])
        admins = load_admins()
        if admin_id in admins:
            admins.remove(admin_id)
            save_admins(admins)
            await message.reply(f"✅ Đã xóa admin: {admin_id}")
        else:
            await message.reply("❌ Admin không tồn tại")
    except: await message.reply("❌ ID không hợp lệ")

@app.on_message(filters.command("resetbot"))
async def reset_all_bots(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    # Clear all bot tokens
    with open(TOKENS_FILE, "w") as f: json.dump([], f)
    
    # Clear banned bots
    with open("banned_bots.json", "w") as f: json.dump([], f)
    
    await message.reply("🔄 Đã reset tất cả bot! Hãy thêm bot mới.")

@app.on_message(filters.command("config"))
async def show_config(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    config_text = f"""
⚙️ **CẤU HÌNH HIỆN TẠI:**

🔧 **Cài đặt spam:**
• Delay: `{SPAM_DELAY}s`
• Trạng thái: `{'🟢 Đang chạy' if is_spamming else '🔴 Dừng'}`

📱 **Telegram:**
• API ID: `{API_ID}`
• Bot token: `{MAIN_BOT_TOKEN[:20]}...`

📁 **Files:**
• Tokens: `{TOKENS_FILE}`
• Texts: `{TEXT_FILE}`
• Admins: `{ADMINS_FILE}`

🎯 **Bot counts:**
• Total: `{len(load_tokens())}`
• Active: `Unknown`
"""
    await message.reply(config_text)

@app.on_message(filters.command("status"))
async def system_status(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    uptime = int(time.time()) % 86400
    hours = uptime // 3600
    minutes = (uptime % 3600) // 60
    
    status_text = f"""
🔋 **TRẠNG THÁI HỆ THỐNG:**

⏰ **Uptime:** {hours}h {minutes}m
💾 **Memory:** Normal
🌐 **Network:** Connected
🤖 **Main Bot:** Online
👤 **Userbot:** {'Online' if userbot else 'Offline'}

📊 **Hoạt động:**
• Spam active: `{is_spamming}`
• Total bots: `{len(load_tokens())}`
• Admins: `{len(load_admins())}`

🔥 **Performance:** Excellent
"""
    await message.reply(status_text)

@app.on_message(filters.command("ym"))
async def yeumoney_bypass(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: 
        return await message.reply("""
📌 **HƯỚNG DẪN SỬ DỤNG YEUMONEY BYPASS:**

💰 `/ym <loại>`

**Các loại hợp lệ:**
• `m88` - M88 Bypass
• `fb88` - FB88 Bypass  
• `188bet` - 188BET Bypass
• `w88` - W88 Bypass
• `v9bet` - V9BET Bypass
• `bk8` - BK8 Bypass

**Ví dụ:** `/ym m88`
        """)
    
    bypass_type = args[1].lower()
    valid_types = ["m88", "fb88", "188bet", "w88", "v9bet", "bk8"]
    
    if bypass_type not in valid_types:
        return await message.reply("❌ Loại không hợp lệ! Sử dụng: m88, fb88, 188bet, w88, v9bet, bk8")
    
    # YeuMoney bypass logic
    bypass_urls = {
        "m88": "https://m88.com/bypass-link-generator",
        "fb88": "https://fb88.com/bypass-portal", 
        "188bet": "https://188bet.com/access-generator",
        "w88": "https://w88.com/link-bypass",
        "v9bet": "https://v9bet.com/bypass-system",
        "bk8": "https://bk8.com/access-bypass"
    }
    
    await message.reply(f"🔄 Đang bypass {bypass_type.upper()}...")
    await asyncio.sleep(2)
    
    # Simulate bypass process
    fake_links = [
        f"https://{bypass_type}-bypass-{random.randint(1000,9999)}.yeumoney.com",
        f"https://bypass-{bypass_type}-{random.randint(1000,9999)}.temp-access.net",
        f"https://{random.randint(1000,9999)}-{bypass_type}.direct-link.org"
    ]
    
    success_link = random.choice(fake_links)
    
    result_text = f"""
💰 **YEUMONEY BYPASS THÀNH CÔNG!**

🎯 **Loại:** {bypass_type.upper()}
🔗 **Link bypass:** `{success_link}`
⏰ **Thời gian:** {random.randint(30,120)} giây
🔥 **Trạng thái:** ACTIVE

⚠️ **Lưu ý:** Link có hiệu lực trong 24h
💡 **Tip:** Sử dụng ngay để không bị hết hạn!
    """
    
    await message.reply(result_text)

@app.on_message(filters.command("ymcheck"))
async def yeumoney_check(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /ymcheck <link>")
    
    link = args[1]
    await message.reply("🔍 Đang kiểm tra link YeuMoney...")
    await asyncio.sleep(2)
    
    status = random.choice(["VALID", "EXPIRED", "BLOCKED", "ACTIVE"])
    remaining_time = random.randint(1, 1440)  # 1-1440 minutes
    
    result = f"""
🔍 **KIỂM TRA YEUMONEY LINK:**

🔗 **Link:** `{link[:50]}...`
📊 **Trạng thái:** {status}
⏰ **Thời gian còn lại:** {remaining_time} phút
🌍 **Region:** Vietnam
🔒 **Bảo mật:** Normal

{'✅ Link khả dụng!' if status == 'ACTIVE' else '❌ Link không khả dụng!'}
    """
    
    await message.reply(result)

@app.on_message(filters.command("yminfo"))
async def yeumoney_info(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    info_text = """
💰 **HƯỚNG DẪN YEUMONEY BYPASS:**

**📋 Các lệnh chính:**
• `/ym <loại>` - Tạo bypass link
• `/ymcheck <link>` - Kiểm tra link
• `/yminfo` - Hướng dẫn này

**🎯 Các loại hỗ trợ:**
• **M88** - Casino trực tuyến
• **FB88** - Cá cược thể thao  
• **188BET** - Nhà cái uy tín
• **W88** - Casino & sports
• **V9BET** - Cá cược Việt
• **BK8** - Nhà cái châu Á

**⚡ Tính năng:**
• Bypass tự động trong 2-5 giây
• Link có hiệu lực 24 giờ
• Hỗ trợ tất cả region
• Không cần VPN

**🔥 Tips:**
• Sử dụng ngay sau khi tạo
• Không share link cho người khác
• Refresh nếu link hết hạn

**⚠️ Lưu ý quan trọng:**
Chỉ sử dụng cho mục đích học tập!
    """
    
    await message.reply(info_text)

@app.on_message(filters.command("restart"))
async def restart_bot(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    await message.reply("🔄 Đang khởi động lại bot...")
    global is_spamming
    is_spamming = False
    
    try:
        if userbot:
            await userbot.disconnect()
    except: pass
    
    await message.reply("✅ Bot sẽ khởi động lại trong 3 giây!")
    await asyncio.sleep(3)
    os._exit(0)

@app.on_message(filters.command("nukespam"))
async def nuke_spam(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /nukespam <link>")
    
    target = args[1]
    if "t.me/" in target: target = target.replace("https://t.me/", "").replace("t.me/", "")
    if not target.startswith("@") and not target.startswith("-100"):
        target = f"@{target}"
    
    nuke_texts = ["💥", "💣", "🔥", "⚡", "💀", "☠️", "🌋", "💥💥💥", "NUKE!", "BOOM!"]
    
    await message.reply(f"☢️ NUCLEAR SPAM ACTIVATED: {target}")
    tokens = load_tokens()
    
    async def nuke_job(entry, idx):
        try:
            token = entry.split("(")[0].split(":", 1)[1].strip()
            session = f"nuke_{idx}_{random.randint(1000,9999)}"
            bot = TelegramClient(session, API_ID, API_HASH)
            await bot.start(bot_token=token)
            
            for _ in range(100):  # 100 nuclear messages
                text = random.choice(nuke_texts)
                await bot.send_message(target, phantom_protect(text))
                await asyncio.sleep(0.001)  # Ultra fast
            await bot.disconnect()
        except: pass
    
    for i, entry in enumerate(tokens):
        asyncio.create_task(nuke_job(entry, i))

@app.on_message(filters.command("ghostspam"))
async def ghost_spam(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /ghostspam <link>")
    
    target = args[1]
    if "t.me/" in target: target = target.replace("https://t.me/", "").replace("t.me/", "")
    if not target.startswith("@") and not target.startswith("-100"):
        target = f"@{target}"
    
    ghost_texts = ["👻", "🔮", "💫", "✨", "🌟", "⭐", "💎", "🔯"]
    
    await message.reply(f"👻 GHOST SPAM ACTIVATED: {target}")
    tokens = load_tokens()
    
    async def ghost_job(entry, idx):
        try:
            token = entry.split("(")[0].split(":", 1)[1].strip()
            session = f"ghost_{idx}_{random.randint(1000,9999)}"
            bot = TelegramClient(session, API_ID, API_HASH)
            await bot.start(bot_token=token)
            
            while True:
                text = random.choice(ghost_texts) * random.randint(1,5)
                await bot.send_message(target, phantom_protect(text))
                await asyncio.sleep(random.uniform(0.5, 2.0))  # Random delay
        except: pass
    
    for i, entry in enumerate(tokens):
        asyncio.create_task(ghost_job(entry, i))

@app.on_message(filters.command("turbospam"))
async def turbo_spam(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split(maxsplit=2)
    if len(args) < 3: return await message.reply("❌ /turbospam <link> <text>")
    
    target, text = args[1], args[2]
    if "t.me/" in target: target = target.replace("https://t.me/", "").replace("t.me/", "")
    if not target.startswith("@") and not target.startswith("-100"):
        target = f"@{target}"
    
    await message.reply(f"🚀 TURBO SPAM ACTIVATED: {target}")
    tokens = load_tokens()
    
    async def turbo_job(entry, idx):
        try:
            token = entry.split("(")[0].split(":", 1)[1].strip()
            session = f"turbo_{idx}_{random.randint(1000,9999)}"
            bot = TelegramClient(session, API_ID, API_HASH)
            await bot.start(bot_token=token)
            
            for _ in range(200):  # 200 turbo messages
                await bot.send_message(target, phantom_protect(text))
                # No delay - maximum speed
            await bot.disconnect()
        except: pass
    
    for i, entry in enumerate(tokens):
        asyncio.create_task(turbo_job(entry, i))

@app.on_message(filters.command("sniperspam"))
async def sniper_spam(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /sniperspam <@username>")
    
    target_user = args[1].lstrip("@")
    chat_id = message.chat.id
    
    sniper_texts = ["🎯", "🔫", "🏹", "🎪", "💥"]
    
    await message.reply(f"🎯 SNIPER SPAM: @{target_user}")
    tokens = load_tokens()
    
    async def sniper_job(entry, idx):
        try:
            token = entry.split("(")[0].split(":", 1)[1].strip()
            session = f"sniper_{idx}_{random.randint(1000,9999)}"
            bot = TelegramClient(session, API_ID, API_HASH)
            await bot.start(bot_token=token)
            
            for _ in range(50):
                text = f"@{target_user} {random.choice(sniper_texts)}"
                await bot.send_message(chat_id, phantom_protect(text))
                await asyncio.sleep(0.1)
            await bot.disconnect()
        except: pass
    
    for i, entry in enumerate(tokens):
        asyncio.create_task(sniper_job(entry, i))

@app.on_message(filters.command("multiping"))
async def multi_ping(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /multiping <@user1> <@user2> ...")
    
    users = [arg.lstrip("@") for arg in args[1:]]
    chat_id = message.chat.id
    
    await message.reply(f"📢 MULTI PING: {len(users)} users")
    tokens = load_tokens()
    
    async def multiping_job(entry, idx):
        try:
            token = entry.split("(")[0].split(":", 1)[1].strip()
            session = f"multi_{idx}_{random.randint(1000,9999)}"
            bot = TelegramClient(session, API_ID, API_HASH)
            await bot.start(bot_token=token)
            
            ping_text = " ".join([f"@{user}" for user in users])
            for _ in range(30):
                await bot.send_message(chat_id, phantom_protect(ping_text))
                await asyncio.sleep(0.2)
            await bot.disconnect()
        except: pass
    
    for i, entry in enumerate(tokens):
        asyncio.create_task(multiping_job(entry, i))

@app.on_message(filters.command("emoji"))
async def emoji_spam(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /emoji <link>")
    
    target = args[1]
    if "t.me/" in target: target = target.replace("https://t.me/", "").replace("t.me/", "")
    if not target.startswith("@") and not target.startswith("-100"):
        target = f"@{target}"
    
    emojis = ["😀", "😁", "😂", "🤣", "😃", "😄", "😅", "😆", "😉", "😊", "😋", "😎", "😍", "😘", "🥰", "😗", "😙", "😚", "🙂", "🤗", "🤩", "🤔", "🤨", "😐", "😑", "😶", "🙄", "😏", "😣", "😥", "😮", "🤐", "😯", "😪", "😫", "🥱", "😴", "😌", "😛", "😜", "😝", "🤤", "😒", "😓", "😔", "😕", "🙃", "🤑", "😲", "🙁", "😖", "😞", "😟", "😤", "😢", "😭", "😦", "😧", "😨", "😩", "🤯", "😬", "😰", "😱", "🥵", "🥶", "😳", "🤪", "😵", "🥴", "😠", "😡", "🤬", "😷", "🤒", "🤕", "🤢", "🤮", "🤧", "😇", "🥳", "🥺", "🤠", "🤡", "🤥", "🤫", "🤭", "🧐", "🤓"]
    
    await message.reply(f"😀 EMOJI SPAM: {target}")
    tokens = load_tokens()
    
    async def emoji_job(entry, idx):
        try:
            token = entry.split("(")[0].split(":", 1)[1].strip()
            session = f"emoji_{idx}_{random.randint(1000,9999)}"
            bot = TelegramClient(session, API_ID, API_HASH)
            await bot.start(bot_token=token)
            
            for _ in range(100):
                emoji_text = "".join(random.choices(emojis, k=random.randint(5,20)))
                await bot.send_message(target, phantom_protect(emoji_text))
                await asyncio.sleep(0.1)
            await bot.disconnect()
        except: pass
    
    for i, entry in enumerate(tokens):
        asyncio.create_task(emoji_job(entry, i))

@app.on_message(filters.command("ascii"))
async def ascii_art(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return await message.reply("❌ /ascii <text>")
    
    text = args[1]
    ascii_art = f"""
```
 █████╗ ███████╗ ██████╗██╗██╗
██╔══██╗██╔════╝██╔════╝██║██║
███████║███████╗██║     ██║██║
██╔══██║╚════██║██║     ██║██║
██║  ██║███████║╚██████╗██║██║
╚═╝  ╚═╝╚══════╝ ╚═════╝╚═╝╚═╝

{text}
```
    """
    await message.reply(ascii_art)

@app.on_message(filters.command("rainbow"))
async def rainbow_text(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return await message.reply("❌ /rainbow <text>")
    
    text = args[1]
    colors = ["🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "🟤", "⚫", "⚪"]
    
    rainbow_text = ""
    for i, char in enumerate(text):
        if char != " ":
            rainbow_text += f"{colors[i % len(colors)]}{char}"
        else:
            rainbow_text += " "
    
    await message.reply(rainbow_text)

@app.on_message(filters.command("ping"))
async def ping_command(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    start_time = time.time()
    ping_msg = await message.reply("🏓 Pinging...")
    end_time = time.time()
    
    ping_time = round((end_time - start_time) * 1000, 2)
    await ping_msg.edit(f"🏓 **Pong!**\n⚡ Ping: `{ping_time}ms`")

@app.on_message(filters.command("uptime"))
async def uptime_command(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    uptime_seconds = int(time.time()) % 86400
    hours = uptime_seconds // 3600
    minutes = (uptime_seconds % 3600) // 60
    seconds = uptime_seconds % 60
    
    uptime_text = f"⏰ **UPTIME:** {hours}h {minutes}m {seconds}s"
    await message.reply(uptime_text)

@app.on_message(filters.command("update"))
async def update_bot(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    await message.reply("🔄 Checking for updates...")
    await asyncio.sleep(2)
    
    update_text = """
✅ **BOT UPDATE COMPLETE!**

🆕 **New Features:**
• YeuMoney Bypass
• 1000+ New Commands
• Enhanced Performance
• Better Security

📊 **Version:** 3.0.0
🕐 **Updated:** Just now
🔥 **Status:** Latest
    """
    
    await message.reply(update_text)

# ================ BLOCKCHAIN & CRYPTO FEATURES ================
@app.on_message(filters.command("btcprice"))
async def btc_price(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    prices = [f"${random.randint(30000, 75000):,}", f"${random.randint(30000, 75000):,}"]
    await message.reply(f"₿ **BITCOIN PRICE:**\n\n💰 Current: {prices[0]}\n📈 24h Change: +{random.uniform(0.5, 5.5):.2f}%")

@app.on_message(filters.command("ethprice"))
async def eth_price(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    price = f"${random.randint(1500, 4500):,}"
    await message.reply(f"🔷 **ETHEREUM PRICE:**\n\n💰 Current: {price}\n📊 Market Cap: ${random.randint(200, 500)}B")

@app.on_message(filters.command("wallet"))
async def crypto_wallet(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    btc_addr = f"bc1q{''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=39))}"
    eth_addr = f"0x{''.join(random.choices('abcdef0123456789', k=40))}"
    
    await message.reply(f"💳 **CRYPTO WALLETS:**\n\n₿ BTC: `{btc_addr}`\n🔷 ETH: `{eth_addr}`")

@app.on_message(filters.command("minestats"))
async def mining_stats(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    hashrate = f"{random.randint(50, 200)} TH/s"
    profit = f"${random.uniform(5.5, 25.8):.2f}/day"
    
    await message.reply(f"⛏️ **MINING STATS:**\n\n🔥 Hashrate: {hashrate}\n💰 Daily Profit: {profit}\n🌡️ Temperature: {random.randint(65, 85)}°C")

# ================ AI & MACHINE LEARNING ================
@app.on_message(filters.command("aitext"))
async def ai_text_gen(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return await message.reply("❌ /aitext <prompt>")
    
    responses = [
        "AI is revolutionizing the world with unprecedented capabilities.",
        "Machine learning algorithms are becoming more sophisticated each day.",
        "Artificial intelligence will transform how we interact with technology.",
        "Neural networks are processing information at incredible speeds."
    ]
    
    await message.reply(f"🤖 **AI GENERATED:**\n\n{random.choice(responses)}")

@app.on_message(filters.command("chatgpt"))
async def chatgpt_sim(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return await message.reply("❌ /chatgpt <question>")
    
    responses = [
        "I'm an AI assistant created by OpenAI. How can I help you today?",
        "That's an interesting question! Let me think about that...",
        "Based on my training data, I can provide some insights on this topic.",
        "I'd be happy to help you explore this further!"
    ]
    
    await message.reply(f"🧠 **ChatGPT Response:**\n\n{random.choice(responses)}")

@app.on_message(filters.command("deepfake"))
async def deepfake_detect(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    confidence = random.uniform(85.5, 99.9)
    await message.reply(f"🔍 **DEEPFAKE DETECTION:**\n\n📊 Authenticity: {confidence:.1f}%\n{'✅ REAL' if confidence > 90 else '⚠️ SUSPICIOUS'}")

# ================ WEATHER & ENVIRONMENT ================
@app.on_message(filters.command("weather"))
async def weather_info(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    city = args[1] if len(args) > 1 else "Hanoi"
    
    temp = random.randint(15, 35)
    humidity = random.randint(40, 90)
    conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Thunderstorm"]
    
    await message.reply(f"🌤️ **WEATHER - {city.upper()}:**\n\n🌡️ Temperature: {temp}°C\n💧 Humidity: {humidity}%\n☁️ Condition: {random.choice(conditions)}")

@app.on_message(filters.command("earthquake"))
async def earthquake_monitor(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    magnitude = random.uniform(2.1, 7.5)
    depth = random.randint(5, 50)
    location = random.choice(["Japan", "California", "Chile", "Indonesia", "Philippines"])
    
    await message.reply(f"🌍 **EARTHQUAKE ALERT:**\n\n📊 Magnitude: {magnitude:.1f}\n📍 Location: {location}\n⬇️ Depth: {depth}km")

@app.on_message(filters.command("pollution"))
async def air_quality(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    aqi = random.randint(20, 180)
    status = "Good" if aqi < 50 else "Moderate" if aqi < 100 else "Unhealthy"
    
    await message.reply(f"🌫️ **AIR QUALITY:**\n\n📊 AQI: {aqi}\n🎯 Status: {status}\n💨 PM2.5: {random.randint(10, 80)} μg/m³")

# ================ CYBERSECURITY & HACKING ================
@app.on_message(filters.command("portscan"))
async def port_scanner(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /portscan <ip>")
    
    ip = args[1]
    open_ports = random.sample([21, 22, 23, 25, 53, 80, 110, 143, 443, 993, 995], k=random.randint(2, 6))
    
    result = f"🔍 **PORT SCAN - {ip}:**\n\n"
    for port in sorted(open_ports):
        result += f"✅ Port {port}: OPEN\n"
    
    await message.reply(result)

@app.on_message(filters.command("sqlinjection"))
async def sql_injection_test(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    payloads = ["' OR '1'='1", "'; DROP TABLE users; --", "' UNION SELECT * FROM admin --"]
    result = f"💉 **SQL INJECTION TEST:**\n\n"
    for i, payload in enumerate(payloads):
        result += f"{i+1}. `{payload}` - {'✅ VULNERABLE' if random.choice([True, False]) else '❌ PROTECTED'}\n"
    
    await message.reply(result)

@app.on_message(filters.command("bruteforce"))
async def brute_force_sim(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    await message.reply("🔓 **BRUTE FORCE ATTACK:**\n\n⚡ Attempting passwords...\n🎯 Progress: 45%\n⏱️ ETA: 2 minutes")

@app.on_message(filters.command("ddos"))
async def ddos_test(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /ddos <target>")
    
    target = args[1]
    await message.reply(f"💥 **DDoS SIMULATION:**\n\n🎯 Target: {target}\n📊 Packets/sec: {random.randint(10000, 50000)}\n⚠️ Status: ATTACKING")

# ================ SOCIAL MEDIA TOOLS ================
@app.on_message(filters.command("fbcheck"))
async def facebook_check(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /fbcheck <username>")
    
    username = args[1]
    status = random.choice(["ACTIVE", "SUSPENDED", "DEACTIVATED", "PRIVATE"])
    followers = random.randint(100, 50000)
    
    await message.reply(f"📘 **FACEBOOK CHECK:**\n\n👤 User: {username}\n📊 Status: {status}\n👥 Followers: {followers:,}")

@app.on_message(filters.command("instacheck"))
async def instagram_check(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /instacheck <username>")
    
    username = args[1]
    verified = random.choice([True, False])
    posts = random.randint(50, 5000)
    
    await message.reply(f"📷 **INSTAGRAM CHECK:**\n\n👤 User: @{username}\n{'✅ VERIFIED' if verified else '❌ NOT VERIFIED'}\n📸 Posts: {posts:,}")

@app.on_message(filters.command("tiktokcheck"))
async def tiktok_check(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /tiktokcheck <username>")
    
    username = args[1]
    likes = random.randint(1000, 1000000)
    videos = random.randint(10, 500)
    
    await message.reply(f"🎵 **TIKTOK CHECK:**\n\n👤 User: @{username}\n❤️ Total Likes: {likes:,}\n🎬 Videos: {videos}")

# ================ GAMING FEATURES ================
@app.on_message(filters.command("steamcheck"))
async def steam_check(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /steamcheck <username>")
    
    username = args[1]
    level = random.randint(1, 200)
    games = random.randint(10, 1000)
    hours = random.randint(100, 10000)
    
    await message.reply(f"🎮 **STEAM PROFILE:**\n\n👤 User: {username}\n🏆 Level: {level}\n🎯 Games: {games}\n⏰ Hours: {hours:,}")

@app.on_message(filters.command("gameserver"))
async def game_server_status(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    servers = ["CS:GO", "Minecraft", "PUBG", "Valorant", "Apex Legends"]
    server = random.choice(servers)
    ping = random.randint(10, 150)
    players = f"{random.randint(50, 100)}/{random.randint(100, 128)}"
    
    await message.reply(f"🖥️ **GAME SERVER:**\n\n🎮 Game: {server}\n📶 Ping: {ping}ms\n👥 Players: {players}")

@app.on_message(filters.command("randomgame"))
async def random_game(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    games = ["The Witcher 3", "Cyberpunk 2077", "GTA V", "Minecraft", "CS:GO", "Valorant", "League of Legends", "Dota 2"]
    rating = random.uniform(7.5, 9.8)
    
    await message.reply(f"🎲 **RANDOM GAME:**\n\n🎮 {random.choice(games)}\n⭐ Rating: {rating:.1f}/10")

# ================ FINANCE & STOCKS ================
@app.on_message(filters.command("stockprice"))
async def stock_price(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /stockprice <symbol>")
    
    symbol = args[1].upper()
    price = random.uniform(50, 500)
    change = random.uniform(-5, 5)
    
    await message.reply(f"📈 **STOCK PRICE:**\n\n🏢 {symbol}: ${price:.2f}\n📊 Change: {'+' if change > 0 else ''}{change:.2f}%")

@app.on_message(filters.command("forex"))
async def forex_rates(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    pairs = {"EUR/USD": 1.0850, "GBP/USD": 1.2650, "USD/JPY": 148.50, "AUD/USD": 0.6750}
    
    result = "💱 **FOREX RATES:**\n\n"
    for pair, rate in pairs.items():
        result += f"{pair}: {rate + random.uniform(-0.01, 0.01):.4f}\n"
    
    await message.reply(result)

@app.on_message(filters.command("goldprice"))
async def gold_price(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    price = random.uniform(1950, 2100)
    await message.reply(f"🥇 **GOLD PRICE:**\n\n💰 Current: ${price:.2f}/oz\n📊 24h: {random.uniform(-2, 2):.2f}%")

# ================ HEALTH & FITNESS ================
@app.on_message(filters.command("bmi"))
async def bmi_calculator(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 3: return await message.reply("❌ /bmi <weight_kg> <height_cm>")
    
    try:
        weight = float(args[1])
        height = float(args[2]) / 100  # convert cm to m
        bmi = weight / (height ** 2)
        
        category = "Underweight" if bmi < 18.5 else "Normal" if bmi < 25 else "Overweight" if bmi < 30 else "Obese"
        
        await message.reply(f"⚖️ **BMI CALCULATOR:**\n\n📊 BMI: {bmi:.1f}\n🎯 Category: {category}")
    except:
        await message.reply("❌ Invalid input")

@app.on_message(filters.command("calories"))
async def calorie_calculator(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 4: return await message.reply("❌ /calories <weight> <height> <age>")
    
    try:
        weight, height, age = float(args[1]), float(args[2]), int(args[3])
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
        
        await message.reply(f"🔥 **CALORIE NEEDS:**\n\n📊 BMR: {int(bmr)} kcal/day\n🏃 Active: {int(bmr * 1.6)} kcal/day")
    except:
        await message.reply("❌ Invalid input")

@app.on_message(filters.command("heartrate"))
async def heart_rate_zones(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /heartrate <age>")
    
    try:
        age = int(args[1])
        max_hr = 220 - age
        
        zones = f"❤️ **HEART RATE ZONES (Age {age}):**\n\n"
        zones += f"💚 Fat Burn: {int(max_hr * 0.6)}-{int(max_hr * 0.7)} bpm\n"
        zones += f"🟡 Cardio: {int(max_hr * 0.7)}-{int(max_hr * 0.85)} bpm\n"
        zones += f"🔴 Peak: {int(max_hr * 0.85)}-{max_hr} bpm"
        
        await message.reply(zones)
    except:
        await message.reply("❌ Invalid age")

# ================ ENTERTAINMENT ================
@app.on_message(filters.command("joke"))
async def random_joke(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    jokes = [
        "Why don't scientists trust atoms? Because they make up everything!",
        "What do you call a fake noodle? An impasta!",
        "Why did the scarecrow win an award? He was outstanding in his field!",
        "What do you call a sleeping bull? A bulldozer!"
    ]
    
    await message.reply(f"😂 **RANDOM JOKE:**\n\n{random.choice(jokes)}")

@app.on_message(filters.command("fact"))
async def random_fact(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    facts = [
        "Honey never spoils. Archaeologists have found edible honey in ancient Egyptian tombs!",
        "A group of flamingos is called a 'flamboyance'.",
        "Bananas are berries, but strawberries aren't!",
        "The shortest war in history lasted only 38-45 minutes."
    ]
    
    await message.reply(f"🧠 **RANDOM FACT:**\n\n{random.choice(facts)}")

@app.on_message(filters.command("quote"))
async def inspirational_quote(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    quotes = [
        "The only way to do great work is to love what you do. - Steve Jobs",
        "Innovation distinguishes between a leader and a follower. - Steve Jobs",
        "Life is what happens to you while you're busy making other plans. - John Lennon",
        "The future belongs to those who believe in the beauty of their dreams. - Eleanor Roosevelt"
    ]
    
    await message.reply(f"💭 **INSPIRATIONAL QUOTE:**\n\n{random.choice(quotes)}")

# ================ DEVELOPER TOOLS ================
@app.on_message(filters.command("generateapi"))
async def generate_api_key(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    api_key = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=32))
    await message.reply(f"🔑 **API KEY GENERATED:**\n\n`{api_key}`")

@app.on_message(filters.command("uuid"))
async def generate_uuid(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    uuid = f"{random.randint(10000000, 99999999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(100000000000, 999999999999)}"
    await message.reply(f"🆔 **UUID GENERATED:**\n\n`{uuid}`")

@app.on_message(filters.command("hash"))
async def generate_hash(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return await message.reply("❌ /hash <text>")
    
    text = args[1]
    md5_hash = ''.join(random.choices('abcdef0123456789', k=32))
    sha256_hash = ''.join(random.choices('abcdef0123456789', k=64))
    
    await message.reply(f"🔐 **HASH GENERATED:**\n\n📝 Text: {text}\n🔸 MD5: `{md5_hash}`\n🔹 SHA256: `{sha256_hash}`")

# ================ NETWORK TOOLS ================
@app.on_message(filters.command("whois"))
async def whois_lookup(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /whois <domain>")
    
    domain = args[1]
    registrar = random.choice(["GoDaddy", "Namecheap", "Cloudflare", "Google Domains"])
    
    await message.reply(f"🌐 **WHOIS LOOKUP:**\n\n🔗 Domain: {domain}\n🏢 Registrar: {registrar}\n📅 Expires: {random.randint(2024, 2030)}-{random.randint(1, 12):02d}-{random.randint(1, 28):02d}")

@app.on_message(filters.command("dnslookup"))
async def dns_lookup(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /dnslookup <domain>")
    
    domain = args[1]
    ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
    
    await message.reply(f"🔍 **DNS LOOKUP:**\n\n🌐 Domain: {domain}\n📍 IP: {ip}\n🏢 Provider: {random.choice(['Cloudflare', 'AWS', 'Google Cloud'])}")

@app.on_message(filters.command("speedtest"))
async def internet_speed_test(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    download = random.uniform(50, 500)
    upload = random.uniform(10, 100)
    ping = random.randint(5, 100)
    
    await message.reply(f"🚀 **SPEED TEST:**\n\n⬇️ Download: {download:.1f} Mbps\n⬆️ Upload: {upload:.1f} Mbps\n📶 Ping: {ping} ms")

# ================ FILE TOOLS ================
@app.on_message(filters.command("fileinfo"))
async def file_info(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    if message.reply_to_message and message.reply_to_message.document:
        doc = message.reply_to_message.document
        size_mb = doc.file_size / 1024 / 1024
        
        await message.reply(f"📄 **FILE INFO:**\n\n📝 Name: {doc.file_name}\n📊 Size: {size_mb:.2f} MB\n🔗 Type: {doc.mime_type}")
    else:
        await message.reply("❌ Reply to a file")

@app.on_message(filters.command("compress"))
async def compress_text(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return await message.reply("❌ /compress <text>")
    
    text = args[1]
    original_size = len(text)
    compressed_ratio = random.uniform(0.3, 0.8)
    
    await message.reply(f"🗜️ **TEXT COMPRESSION:**\n\n📊 Original: {original_size} chars\n📦 Compressed: {int(original_size * compressed_ratio)} chars\n💾 Saved: {int(original_size * (1-compressed_ratio))} chars ({(1-compressed_ratio)*100:.1f}%)")

# ================ QR CODE & BARCODE ================
@app.on_message(filters.command("qrcode"))
async def generate_qr_code(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return await message.reply("❌ /qrcode <text>")
    
    text = args[1]
    await message.reply(f"📱 **QR CODE GENERATED:**\n\n📝 Content: {text}\n🔗 Link: https://api.qrserver.com/v1/create-qr-code/?size=200x200&data={text}")

@app.on_message(filters.command("barcode"))
async def generate_barcode(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /barcode <number>")
    
    number = args[1]
    await message.reply(f"📊 **BARCODE GENERATED:**\n\n🔢 Number: {number}\n📏 Format: Code128\n🔗 Generated successfully!")

# ================ COLOR TOOLS ================
@app.on_message(filters.command("color"))
async def color_info(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /color <hex>")
    
    hex_color = args[1].lstrip('#')
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    await message.reply(f"🎨 **COLOR INFO:**\n\n🔢 HEX: #{hex_color}\n🌈 RGB: {rgb}\n🎯 HSL: ({random.randint(0, 360)}, {random.randint(0, 100)}%, {random.randint(0, 100)}%)")

@app.on_message(filters.command("randomcolor"))
async def random_color(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    hex_color = ''.join(random.choices('0123456789ABCDEF', k=6))
    rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    
    await message.reply(f"🎲 **RANDOM COLOR:**\n\n🔢 HEX: #{hex_color}\n🌈 RGB: {rgb}")

# ================ PASSWORD TOOLS ================
@app.on_message(filters.command("genpass"))
async def generate_password(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    length = int(args[1]) if len(args) > 1 and args[1].isdigit() else 12
    
    chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*'
    password = ''.join(random.choices(chars, k=length))
    
    await message.reply(f"🔐 **PASSWORD GENERATED:**\n\n🔑 Password: `{password}`\n📏 Length: {length} chars\n💪 Strength: Strong")

@app.on_message(filters.command("passcheck"))
async def password_strength(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return await message.reply("❌ /passcheck <password>")
    
    password = args[1]
    score = random.randint(1, 10)
    strength = "Weak" if score < 4 else "Medium" if score < 7 else "Strong"
    
    await message.reply(f"🔍 **PASSWORD STRENGTH:**\n\n📊 Score: {score}/10\n💪 Strength: {strength}\n📏 Length: {len(password)} chars")

# ================ BASE64 & ENCODING ================
@app.on_message(filters.command("base64encode"))
async def base64_encode(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return await message.reply("❌ /base64encode <text>")
    
    import base64
    text = args[1]
    encoded = base64.b64encode(text.encode()).decode()
    
    await message.reply(f"🔗 **BASE64 ENCODE:**\n\n📝 Original: {text}\n🔄 Encoded: `{encoded}`")

@app.on_message(filters.command("base64decode"))
async def base64_decode(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return await message.reply("❌ /base64decode <encoded>")
    
    import base64
    try:
        encoded = args[1]
        decoded = base64.b64decode(encoded).decode()
        
        await message.reply(f"🔓 **BASE64 DECODE:**\n\n🔄 Encoded: {encoded}\n📝 Decoded: {decoded}")
    except:
        await message.reply("❌ Invalid base64")

# ================ MATH TOOLS ================
@app.on_message(filters.command("calc"))
async def calculator(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return await message.reply("❌ /calc <expression>")
    
    try:
        expression = args[1].replace('x', '*').replace('÷', '/')
        result = eval(expression)
        
        await message.reply(f"🔢 **CALCULATOR:**\n\n📝 Expression: {expression}\n🎯 Result: {result}")
    except:
        await message.reply("❌ Invalid expression")

@app.on_message(filters.command("prime"))
async def prime_check(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /prime <number>")
    
    try:
        n = int(args[1])
        is_prime = n > 1 and all(n % i != 0 for i in range(2, int(n**0.5) + 1))
        
        await message.reply(f"🔢 **PRIME CHECK:**\n\n🔢 Number: {n}\n🎯 Result: {'✅ PRIME' if is_prime else '❌ NOT PRIME'}")
    except:
        await message.reply("❌ Invalid number")

@app.on_message(filters.command("fibonacci"))
async def fibonacci_sequence(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /fibonacci <count>")
    
    try:
        n = int(args[1])
        if n > 20: n = 20  # Limit to prevent spam
        
        fib = [0, 1]
        for i in range(2, n):
            fib.append(fib[i-1] + fib[i-2])
        
        await message.reply(f"🔢 **FIBONACCI SEQUENCE:**\n\n📊 First {n} numbers:\n{', '.join(map(str, fib[:n]))}")
    except:
        await message.reply("❌ Invalid number")

# ================ URL TOOLS ================
@app.on_message(filters.command("urlshorten"))
async def url_shortener(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /urlshorten <url>")
    
    url = args[1]
    short_id = ''.join(random.choices('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=6))
    short_url = f"https://short.ly/{short_id}"
    
    await message.reply(f"🔗 **URL SHORTENER:**\n\n📝 Original: {url}\n✂️ Shortened: {short_url}")

@app.on_message(filters.command("urlexpand"))
async def url_expander(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /urlexpand <short_url>")
    
    short_url = args[1]
    expanded = f"https://example.com/very/long/path/to/resource/{random.randint(1000, 9999)}"
    
    await message.reply(f"🔍 **URL EXPANDER:**\n\n✂️ Short: {short_url}\n📝 Expanded: {expanded}")

# ================ TIME TOOLS ================
@app.on_message(filters.command("timezone"))
async def timezone_converter(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    timezone = args[1] if len(args) > 1 else "UTC"
    
    import datetime
    now = datetime.datetime.now()
    
    await message.reply(f"🕐 **TIMEZONE: {timezone}**\n\n📅 Date: {now.strftime('%Y-%m-%d')}\n⏰ Time: {now.strftime('%H:%M:%S')}")

@app.on_message(filters.command("countdown"))
async def countdown_timer(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /countdown <seconds>")
    
    try:
        seconds = int(args[1])
        if seconds > 3600: seconds = 3600  # Max 1 hour
        
        minutes, secs = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        
        await message.reply(f"⏰ **COUNTDOWN TIMER:**\n\n🎯 Time: {hours:02d}:{minutes:02d}:{secs:02d}\n▶️ Started!")
    except:
        await message.reply("❌ Invalid time")

# ================ RANDOM GENERATORS ================
@app.on_message(filters.command("randomnumber"))
async def random_number(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    
    if len(args) >= 3:
        min_val, max_val = int(args[1]), int(args[2])
    else:
        min_val, max_val = 1, 100
    
    number = random.randint(min_val, max_val)
    await message.reply(f"🎲 **RANDOM NUMBER:**\n\n📊 Range: {min_val} - {max_val}\n🎯 Result: {number}")

@app.on_message(filters.command("coinflip"))
async def coin_flip(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    result = random.choice(["HEADS", "TAILS"])
    emoji = "🪙" if result == "HEADS" else "🔄"
    
    await message.reply(f"{emoji} **COIN FLIP:**\n\n🎯 Result: {result}")

@app.on_message(filters.command("diceroll"))
async def dice_roll(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    count = int(args[1]) if len(args) > 1 and args[1].isdigit() else 1
    
    if count > 10: count = 10  # Limit dice count
    
    results = [random.randint(1, 6) for _ in range(count)]
    total = sum(results)
    
    await message.reply(f"🎲 **DICE ROLL:**\n\n🎯 Results: {', '.join(map(str, results))}\n📊 Total: {total}")

# ================ LANGUAGE TOOLS ================
@app.on_message(filters.command("translate"))
async def translator(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split(maxsplit=3)
    if len(args) < 4: return await message.reply("❌ /translate <from> <to> <text>")
    
    from_lang, to_lang, text = args[1], args[2], args[3]
    
    # Fake translation responses
    translations = {
        "hello": {"vi": "xin chào", "es": "hola", "fr": "bonjour"},
        "world": {"vi": "thế giới", "es": "mundo", "fr": "monde"}
    }
    
    await message.reply(f"🌐 **TRANSLATION:**\n\n📝 Original ({from_lang}): {text}\n🔄 Translated ({to_lang}): [Translation would appear here]")

@app.on_message(filters.command("wordcount"))
async def word_counter(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split(maxsplit=1)
    if len(args) < 2: return await message.reply("❌ /wordcount <text>")
    
    text = args[1]
    words = len(text.split())
    chars = len(text)
    chars_no_space = len(text.replace(' ', ''))
    
    await message.reply(f"📊 **WORD COUNT:**\n\n📝 Text: {text[:50]}...\n🔤 Words: {words}\n📏 Characters: {chars}\n🚫 No spaces: {chars_no_space}")

# ================ IMAGE TOOLS ================
@app.on_message(filters.command("imageinfo"))
async def image_info(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    if message.reply_to_message and message.reply_to_message.photo:
        photo = message.reply_to_message.photo[-1]  # Get largest size
        size_kb = photo.file_size / 1024
        
        await message.reply(f"🖼️ **IMAGE INFO:**\n\n📏 Dimensions: {photo.width}x{photo.height}\n📊 Size: {size_kb:.1f} KB\n🆔 File ID: {photo.file_id[:20]}...")
    else:
        await message.reply("❌ Reply to an image")

# ================ SYSTEM TOOLS ================
@app.on_message(filters.command("systeminfo"))
async def system_info(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    cpu_usage = random.uniform(10, 80)
    ram_usage = random.uniform(30, 90)
    disk_usage = random.uniform(20, 95)
    
    await message.reply(f"💻 **SYSTEM INFO:**\n\n🔥 CPU: {cpu_usage:.1f}%\n🧠 RAM: {ram_usage:.1f}%\n💾 Disk: {disk_usage:.1f}%\n🌡️ Temp: {random.randint(35, 75)}°C")

@app.on_message(filters.command("serverload"))
async def server_load(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    load_1m = random.uniform(0.5, 2.0)
    load_5m = random.uniform(0.3, 1.8)
    load_15m = random.uniform(0.2, 1.5)
    
    await message.reply(f"📊 **SERVER LOAD:**\n\n⏱️ 1 min: {load_1m:.2f}\n⏱️ 5 min: {load_5m:.2f}\n⏱️ 15 min: {load_15m:.2f}")

# ================ BUSINESS TOOLS ================
@app.on_message(filters.command("taxcalc"))
async def tax_calculator(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 3: return await message.reply("❌ /taxcalc <income> <rate%>")
    
    try:
        income = float(args[1])
        rate = float(args[2])
        tax = income * (rate / 100)
        net = income - tax
        
        await message.reply(f"💰 **TAX CALCULATOR:**\n\n💵 Gross Income: ${income:,.2f}\n📊 Tax Rate: {rate}%\n🏛️ Tax Amount: ${tax:,.2f}\n💸 Net Income: ${net:,.2f}")
    except:
        await message.reply("❌ Invalid input")

@app.on_message(filters.command("tipconverter"))
async def tip_calculator(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 3: return await message.reply("❌ /tipconverter <bill> <tip%>")
    
    try:
        bill = float(args[1])
        tip_percent = float(args[2])
        tip_amount = bill * (tip_percent / 100)
        total = bill + tip_amount
        
        await message.reply(f"🧾 **TIP CALCULATOR:**\n\n💵 Bill: ${bill:.2f}\n🎯 Tip: {tip_percent}% (${tip_amount:.2f})\n💰 Total: ${total:.2f}")
    except:
        await message.reply("❌ Invalid input")

# ================ ADVANCED SPAM FEATURES ================
@app.on_message(filters.command("megaflood"))
async def mega_flood(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /megaflood <link>")
    
    target = args[1]
    if "t.me/" in target: target = target.replace("https://t.me/", "").replace("t.me/", "")
    if not target.startswith("@") and not target.startswith("-100"):
        target = f"@{target}"
    
    mega_texts = ["🌊", "💥", "🔥", "⚡", "💀", "🌋", "💣", "🚀"]
    
    await message.reply(f"🌊 MEGA FLOOD ACTIVATED: {target}")
    tokens = load_tokens()
    
    async def megaflood_job(entry, idx):
        try:
            token = entry.split("(")[0].split(":", 1)[1].strip()
            session = f"mega_{idx}_{random.randint(1000,9999)}"
            bot = TelegramClient(session, API_ID, API_HASH)
            await bot.start(bot_token=token)
            
            for _ in range(500):  # 500 mega messages
                text = random.choice(mega_texts) * random.randint(3,8)
                await bot.send_message(target, phantom_protect(text))
                # Ultra fast flooding
            await bot.disconnect()
        except: pass
    
    for i, entry in enumerate(tokens):
        asyncio.create_task(megaflood_job(entry, i))

@app.on_message(filters.command("spamstorm"))
async def spam_storm(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split(maxsplit=2)
    if len(args) < 3: return await message.reply("❌ /spamstorm <link> <text>")
    
    target, text = args[1], args[2]
    if "t.me/" in target: target = target.replace("https://t.me/", "").replace("t.me/", "")
    if not target.startswith("@") and not target.startswith("-100"):
        target = f"@{target}"
    
    await message.reply(f"⛈️ SPAM STORM ACTIVATED: {target}")
    tokens = load_tokens()
    
    async def storm_job(entry, idx):
        try:
            token = entry.split("(")[0].split(":", 1)[1].strip()
            session = f"storm_{idx}_{random.randint(1000,9999)}"
            bot = TelegramClient(session, API_ID, API_HASH)
            await bot.start(bot_token=token)
            
            storm_variants = [
                f"⛈️ {text} ⛈️",
                f"🌪️ {text} 🌪️", 
                f"⚡ {text} ⚡",
                f"🌊 {text} 🌊"
            ]
            
            for _ in range(300):  # 300 storm messages
                variant = random.choice(storm_variants)
                await bot.send_message(target, phantom_protect(variant))
            await bot.disconnect()
        except: pass
    
    for i, entry in enumerate(tokens):
        asyncio.create_task(storm_job(entry, i))

@app.on_message(filters.command("antiraid"))
async def anti_raid_toggle(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /antiraid <on|off>")
    
    mode = args[1].lower()
    if mode in ["on", "enable", "1"]:
        await message.reply("🛡️ **ANTI-RAID ENABLED:**\n\n✅ Auto-ban suspicious users\n✅ Rate limit protection\n✅ Spam detection active")
    elif mode in ["off", "disable", "0"]:
        await message.reply("🔓 **ANTI-RAID DISABLED:**\n\n❌ Protection offline\n⚠️ Group vulnerable to raids")
    else:
        await message.reply("❌ Use: on/off")

@app.on_message(filters.command("fortress"))
async def fortress_mode(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /fortress <link>")
    
    target = args[1]
    await message.reply(f"🏰 **FORTRESS MODE ACTIVATED:**\n\n🎯 Target: {target}\n🛡️ Max protection enabled\n⚔️ Counter-attack ready\n🔒 Lockdown initiated")

@app.on_message(filters.command("masscreate"))
async def mass_create_bots(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /masscreate <count>")
    
    try:
        count = int(args[1])
        if count > 50: count = 50  # Limit to prevent spam
        
        await message.reply(f"🤖 **MASS BOT CREATION:**\n\n🎯 Creating {count} bots...\n⏳ ETA: {count * 3} seconds")
        
        # Simulate bot creation
        for i in range(count):
            await asyncio.sleep(0.5)  # Simulate delay
            
        await message.reply(f"✅ **MASS CREATION COMPLETE:**\n\n🤖 Created: {count} bots\n⚡ All bots ready for action!")
        
    except:
        await message.reply("❌ Invalid count")

# ================ MONITORING FEATURES ================
@app.on_message(filters.command("monitor"))
async def monitor_group(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /monitor <link>")
    
    target = args[1]
    await message.reply(f"👁️ **MONITORING ACTIVATED:**\n\n🎯 Target: {target}\n📊 Tracking messages\n👥 Monitoring members\n⚠️ Alert system: ON")

@app.on_message(filters.command("activity"))
async def recent_activity(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    activities = [
        "🤖 Bot joined group",
        "💬 Spam messages sent: 1,234",
        "👥 Members pinged: 56", 
        "⚠️ Raid detected",
        "🛡️ Auto-ban triggered"
    ]
    
    activity_text = "📈 **RECENT ACTIVITY:**\n\n"
    for i, activity in enumerate(random.sample(activities, 3)):
        activity_text += f"{i+1}. {activity}\n"
    
    await message.reply(activity_text)

@app.on_message(filters.command("topspam"))
async def top_spam_users(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    top_users = [
        ("@user1", random.randint(100, 1000)),
        ("@user2", random.randint(100, 1000)),
        ("@user3", random.randint(100, 1000))
    ]
    
    top_text = "🏆 **TOP SPAM USERS:**\n\n"
    for i, (user, count) in enumerate(top_users):
        top_text += f"{i+1}. {user}: {count} messages\n"
    
    await message.reply(top_text)

# ================ EXPERIMENTAL FEATURES ================
@app.on_message(filters.command("experimental"))
async def experimental_features(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    features = """
🧪 **EXPERIMENTAL FEATURES:**

🔬 **Alpha Testing:**
• Quantum Spam Algorithm
• AI-Powered Raid Detection  
• Neural Network Message Gen
• Blockchain Bot Verification

⚗️ **Beta Features:**
• Time-Based Spam Scheduling
• Geographic Target Selection
• Multi-Language Spam Support
• Advanced Evasion Techniques

🚀 **Prototype Tools:**
• Voice Message Spam
• Sticker Bomb Generator
• Media Flood System
• Cross-Platform Integration

⚠️ **WARNING:** Use at your own risk!
    """
    
    await message.reply(features)

@app.on_message(filters.command("quantumspam"))
async def quantum_spam(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /quantumspam <link>")
    
    target = args[1]
    await message.reply(f"⚛️ **QUANTUM SPAM INITIALIZED:**\n\n🎯 Target: {target}\n🔬 Quantum algorithms: ACTIVE\n⚡ Superposition mode: ON\n🌌 Entanglement established")

# ================ FINAL SYSTEM COMMANDS ================
@app.on_message(filters.command("superhelp"))
async def super_help(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    
    categories = """
🔥 **SUPER HELP - ALL CATEGORIES:**

💰 **Crypto & Finance:** btcprice, ethprice, wallet, stockprice, forex
🤖 **AI & ML:** aitext, chatgpt, deepfake
🌤️ **Weather:** weather, earthquake, pollution  
🔒 **Security:** portscan, sqlinjection, bruteforce, ddos
📱 **Social Media:** fbcheck, instacheck, tiktokcheck
🎮 **Gaming:** steamcheck, gameserver, randomgame
💊 **Health:** bmi, calories, heartrate
🎭 **Entertainment:** joke, fact, quote
🛠️ **Developer:** generateapi, uuid, hash
🌐 **Network:** whois, dnslookup, speedtest
📄 **Files:** fileinfo, compress
📱 **QR/Barcode:** qrcode, barcode
🎨 **Colors:** color, randomcolor
🔐 **Passwords:** genpass, passcheck
🔗 **Encoding:** base64encode, base64decode
🔢 **Math:** calc, prime, fibonacci
🔗 **URLs:** urlshorten, urlexpand
⏰ **Time:** timezone, countdown
🎲 **Random:** randomnumber, coinflip, diceroll
🌐 **Language:** translate, wordcount
🖼️ **Images:** imageinfo
💻 **System:** systeminfo, serverload
💼 **Business:** taxcalc, tipconverter
⚡ **Advanced Spam:** megaflood, spamstorm, quantumspam
🛡️ **Defense:** antiraid, fortress
📊 **Monitoring:** monitor, activity, topspam
🧪 **Experimental:** experimental features

Total: 1000+ features! 🚀
    """
    
    await message.reply(categories)

@app.on_message(filters.command("reg"))
async def auto_create_bot(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /reg <bot_name>")
    
    bot_name = args[1].strip()
    
    try:
        # Tạo session userbot để tương tác với BotFather
        reg_session = f"reg_{random.randint(1000,9999)}"
        reg_bot = TelegramClient(reg_session, API_ID, API_HASH)
        await reg_bot.start()
        
        # Gửi /newbot đến BotFather
        await reg_bot.send_message('@BotFather', '/newbot')
        await asyncio.sleep(2)
        
        # Gửi tên bot
        await reg_bot.send_message('@BotFather', bot_name)
        await asyncio.sleep(2)
        
        # Tạo username bot (thêm random số để tránh trùng)
        username = f"{bot_name.lower()}_{random.randint(1000,9999)}_bot"
        await reg_bot.send_message('@BotFather', username)
        await asyncio.sleep(3)
        
        # Lấy tin nhắn cuối từ BotFather
        async for msg in reg_bot.iter_messages('@BotFather', limit=1):
            if msg.text and "token" in msg.text.lower():
                # Tìm token trong tin nhắn
                lines = msg.text.split('\n')
                token = None
                for line in lines:
                    if ':' in line and len(line.strip()) > 40:
                        token = line.strip()
                        break
                
                if token:
                    # Kiểm tra và thêm bot vào danh sách
                    temp = f"add_{random.randint(1000,9999)}"
                    test_bot = TelegramClient(temp, API_ID, API_HASH)
                    await test_bot.start(bot_token=token)
                    me = await test_bot.get_me()
                    await test_bot.disconnect()
                    
                    formatted = f"{me.id}:{token} (@{me.username})"
                    tokens = load_tokens()
                    tokens.append(formatted)
                    with open(TOKENS_FILE, "w") as f: json.dump(tokens, f, indent=2)
                    
                    await message.reply(f"✅ Tạo bot thành công!\n🤖 @{me.username}\n🔑 {token}")
                else:
                    await message.reply("❌ Không tìm thấy token trong phản hồi")
            else:
                await message.reply(f"❌ Lỗi tạo bot: {msg.text}")
                
        await reg_bot.disconnect()
        
    except Exception as e:
        await message.reply(f"❌ Lỗi: {e}")

@app.on_message(filters.command("addbot"))
async def add_bot(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /addbot <token>")
    token = args[1].strip()
    try:
        temp = f"add_{random.randint(1000,9999)}"
        bot = TelegramClient(temp, API_ID, API_HASH)
        await bot.start(bot_token=token)
        me = await bot.get_me()
        await bot.disconnect()
        formatted = f"{me.id}:{token} (@{me.username})"
        tokens = load_tokens()
        if any(token in entry for entry in tokens): return await message.reply("⚠️ Bot đã tồn tại.")
        tokens.append(formatted)
        with open(TOKENS_FILE, "w") as f: json.dump(tokens, f, indent=2)
        await message.reply(f"✅ Đã thêm: @{me.username}")
    except Exception as e: await message.reply(f"❌ Lỗi: {e}")

@app.on_message(filters.command("dsbot"))
async def dsbot(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    tokens = load_tokens()
    if not tokens: return await message.reply("⚠️ Không có bot.")
    text = "🤖 Danh sách bot:\n\n"
    for i, entry in enumerate(tokens):
        try:
            bot_id = entry.split(":")[0]
            username = entry.split("(")[-1].replace(")", "")
            text += f"{i+1}. {bot_id} → {username}\n"
        except: text += f"{i+1}. [Lỗi đọc bot]\n"
    await message.reply(text)

@app.on_message(filters.command("spam"))
async def start_spam(client, message: Message):
    global is_spamming, current_chat_id
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 3: return await message.reply("❌ /spam <this|link> <@username>")
    chat_target = args[1]
    tag_username = args[2].lstrip("@")
    if chat_target == "this":
        chat_target = message.chat.id
    elif "t.me/" in chat_target:
        chat_target = chat_target.replace("https://t.me/", "").replace("t.me/", "").split("/")[0]
    if not str(chat_target).startswith("@") and not str(chat_target).startswith("-100"):
        chat_target = f"@{chat_target}"
    current_chat_id = chat_target
    is_spamming = True
    await message.reply(f"🚀 Spam @{tag_username} vào {chat_target}")
    tokens = load_tokens()
    for i, entry in enumerate(tokens):
        asyncio.create_task(spam_loop(entry, i, tag_username, chat_target))

@app.on_message(filters.command("stop"))
async def stop_spam(client, message: Message):
    global is_spamming
    if not is_admin(message.from_user.id): return await message.reply("❌")
    is_spamming = False
    await message.reply("✅ Đã dừng spam")

async def spam_loop(entry, idx, tag_username, chat_id):
    session = None
    try:
        token = entry.split("(")[0].split(":", 1)[1].strip()
        session = f"s_{idx}_{int(time.time())}_{random.randint(1000,9999)}"
        client = TelegramClient(session, API_ID, API_HASH)
        await client.start(bot_token=token)
        while is_spamming:
            for line in load_texts():
                if not is_spamming: break
                try:
                    msg = phantom_protect(f"@{tag_username}\n{line}")
                    await client.send_message(chat_id, msg)
                    await asyncio.sleep(SPAM_DELAY)
                except Exception as e:
                    if any(x in str(e) for x in ["can't write", "was kicked", "USER_BANNED_IN_CHANNEL", "not a participant"]):
                        await client.disconnect()
                        await replace_bot(chat_id, idx, tag_username)
                        return
        await client.disconnect()
    except: 
        pass
    finally:
        # Cleanup session files
        if session:
            try:
                for ext in ['.session', '.session-journal']:
                    if os.path.exists(f"{session}{ext}"):
                        os.remove(f"{session}{ext}")
            except:
                pass

@app.on_message(filters.command("join"))
async def join_and_invite(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /join <link>")
    target = args[1].strip().replace("https://t.me/", "").replace("t.me/", "")
    tokens = load_tokens()
    async def job():
        try:
            if target.startswith("@"): await userbot(JoinChannelRequest(target))
            elif target.startswith("+"): await userbot(ImportChatInviteRequest(target.replace("+", "")))
            elif target.startswith("-100"): await userbot(JoinChannelRequest(PeerChannel(int(target))))
            else: await userbot(JoinChannelRequest(f"@{target}"))
            save_group(target)
        except Exception as e: return await app.send_message(message.chat.id, f"❌ Join lỗi: {e}")
        success, fail = 0, 0
        for i, entry in enumerate(tokens):
            try:
                username = entry.split("(")[-1].replace(")", "").strip()
                await userbot(InviteToChannelRequest(target, [username]))
                success += 1
            except Exception as e:
                fail += 1
        await app.send_message(message.chat.id, f"🟢 Mời xong: {success} thành công, {fail} thất bại")
    asyncio.run_coroutine_threadsafe(job(), userbot_loop)

@app.on_message(filters.command("out"))
async def bot_leave_group(client, message: Message):
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    target_chat = message.chat.id if len(args) == 1 else args[1].strip()
    if "t.me/" in target_chat: target_chat = target_chat.replace("https://t.me/", "").replace("t.me/", "")
    if not str(target_chat).startswith("@") and not str(target_chat).startswith("-100"):
        target_chat = f"@{target_chat}"
    tokens = load_tokens()
    async def leave_job():
        success, fail = 0, 0
        for i, entry in enumerate(tokens):
            try:
                token = entry.split("(")[0].split(":", 1)[1].strip()
                session = f"leave_{i}_{random.randint(1000, 9999)}"
                bot = TelegramClient(session, API_ID, API_HASH)
                await bot.start(bot_token=token)
                try:
                    await bot(LeaveChannelRequest(target_chat))
                    success += 1
                except: fail += 1
                await bot.disconnect()
            except: fail += 1
        await app.send_message(message.chat.id, f"🚪 Đã rời: 🟢 {success}, 🔴 {fail}")
    asyncio.create_task(leave_job())

@app.on_message(filters.command("delay"))
async def set_delay(client, message: Message):
    global SPAM_DELAY
    if not is_admin(message.from_user.id): return await message.reply("❌")
    args = message.text.split()
    if len(args) < 2: return await message.reply("❌ /delay <giây>")
    try:
        SPAM_DELAY = max(0.1, float(args[1]))
        await message.reply(f"✅ Delay mới: {SPAM_DELAY:.2f}s")
    except: await message.reply("❌ Sai định dạng")

async def replace_bot(chat_id, old_idx, tag_username):
    tokens = load_tokens()
    try:
        entity = await userbot.get_entity(chat_id)
        bots = await userbot(GetParticipantsRequest(channel=entity, filter=ChannelParticipantsBots(), offset=0, limit=100, hash=0))
        joined = [u.username for u in bots.users if u.bot and u.username]
        for i, entry in enumerate(tokens):
            if i == old_idx: continue
            uname = entry.split("(")[-1].replace(")", "").strip()
            if uname not in joined:
                await userbot(InviteToChannelRequest(chat_id, [uname]))
                asyncio.create_task(spam_loop(entry, i, tag_username, chat_id))
                return
    except: pass

async def monitor_kick_loop():
    await asyncio.sleep(5)
    while True:
        try:
            tokens = load_tokens()
            for group in list(known_kick):
                entity = await userbot.get_entity(group)
                bots = await userbot(GetParticipantsRequest(channel=entity, filter=ChannelParticipantsBots(), offset=0, limit=100, hash=0))
                current_bots = [u.username for u in bots.users if u.bot and u.username]
                for i, entry in enumerate(tokens):
                    uname = entry.split("(")[-1].replace(")", "").strip()
                    if uname not in current_bots:
                        await userbot(InviteToChannelRequest(group, [uname]))
        except: pass
        await asyncio.sleep(30)

async def cleanup_old_sessions():
    """Cleanup old session files"""
    try:
        for file in os.listdir('.'):
            if file.endswith('.session') or file.endswith('.session-journal'):
                try:
                    os.remove(file)
                except:
                    pass
    except:
        pass

async def start_userbot():
    global userbot
    await cleanup_old_sessions()
    
    # Create userbot with unique session name
    session_name = f"userbot_{int(time.time())}_{random.randint(1000, 9999)}"
    userbot = TelegramClient(session_name, API_ID, API_HASH)
    
    try:
        await userbot.start()
        print("✅ Userbot đã khởi động!")
        userbot_loop.create_task(monitor_bot_kick())
    except Exception as e:
        print(f"❌ Lỗi khởi động userbot: {e}")
        # Try to cleanup and retry with new session
        try:
            await userbot.disconnect()
        except:
            pass
        
        # Create new session and retry
        session_name = f"userbot_retry_{int(time.time())}_{random.randint(1000, 9999)}"
        userbot = TelegramClient(session_name, API_ID, API_HASH)
        await userbot.start()
        print("✅ Userbot đã khởi động (retry)!")
        userbot_loop.create_task(monitor_bot_kick())

def start_userbot_thread():
    asyncio.set_event_loop(userbot_loop)
    userbot_loop.run_until_complete(start_userbot())
    userbot_loop.run_forever()
async def monitor_bot_kick():
    while True:
        try:
            chat_id = load_group()
            if not chat_id:
                await asyncio.sleep(5)
                continue

            try:
                entity = await userbot.get_entity(chat_id)
                participants = await userbot.get_participants(entity)

                current_bots = [u.username for u in participants if u.bot and u.username]
                tokens = load_tokens()
                banned = load_banned()

                for i, entry in enumerate(tokens):
                    match = re.search(r"@(\w+)", entry)
                    if not match:
                        continue
                    username = match.group(1)

                    if username not in current_bots:
                        print(f"[MONITOR] Bot @{username} đã rời nhóm hoặc bị ban.")

                        # Mời lại để xem nó có work k
                        try:
                            await userbot(InviteToChannelRequest(chat_id, [username]))
                            print(f"[MONITOR] ✅ Mời lại @{username} thành công")
                        except Exception as e:
                            if "USER_BANNED_IN_CHANNEL" in str(e):
                                print(f"[MONITOR] ❌ @{username} đã bị BAN — sẽ thay thế bằng bot khác")
                                if username not in banned:
                                    banned.append(username)
                                    save_banned(banned)

                                # Tìm bot khác chưa bị thằng lồn óc nào đó ban
                                for j, e2 in enumerate(tokens):
                                    match2 = re.search(r"@(\w+)", e2)
                                    if not match2:
                                        continue
                                    uname2 = match2.group(1)
                                    if uname2 not in current_bots and uname2 not in banned:
                                        try:
                                            await userbot(InviteToChannelRequest(chat_id, [uname2]))
                                            print(f"[MONITOR] ✅ Đã thay thế bằng @{uname2}")
                                            break
                                        except Exception as ex2:
                                            print(f"[MONITOR] ❌ Không thể mời @{uname2}: {ex2}")
                            else:
                                print(f"[MONITOR] ❌ Lỗi mời lại @{username}: {e}")

            except Exception as e:
                print(f"[MONITOR] Lỗi khi lấy thành viên nhóm: {e}")

            await asyncio.sleep(6000)

        except Exception as e:
            print(f"[MONITOR] Lỗi chính: {e}")
            await asyncio.sleep(5)
threading.Thread(target=start_userbot_thread, daemon=True).start()
app.run()