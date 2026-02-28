import telebot
from telebot import types
import datetime

TOKEN = "8379282751:AAFKF1HCubu8XzGGREqBJUjJaBTKGpVKzhc"
ADMIN_ID = 5773143142

bot = telebot.TeleBot(TOKEN)

# Хранение данных заказа
orders = {}

def get_main_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.KeyboardButton("🛒 Заказать GOBOX"))
    keyboard.add(types.KeyboardButton("📦 Состав набора"))
    keyboard.add(types.KeyboardButton("❓ Вопрос"))
    return keyboard

# /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        f"👋 Привет! Это бот заказа *GOBOX* — спасательный набор для леса, рыбалки и дороги.\n\n"
        f"🔥 Акция: ~~12 900 ₽~~ → *9 900 ₽*\n"
        f"📦 40+ предметов · 950г · доставка по России\n\n"
        f"Выбери действие ниже 👇",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

# Состав
@bot.message_handler(func=lambda m: m.text == "📦 Состав набора")
def composition(message):
    bot.send_message(
        message.chat.id,
        "📦 *Состав GOBOX (40+ предметов):*\n\n"
        "🔥 *Огонь и свет:* фонарик COB, батарейки, зажигалка ×2, свеча, сухое горючее\n"
        "🧭 *Навигация:* свисток, компас, термометр, браслет светоотражающий\n"
        "🪢 *Крепёж:* паракорд 10м (250кг), карабин (1200кг), булавки\n"
        "🔧 *Инструменты:* мультитул, пила-струна, экстрактор клещей ×3, скотч, суперклей\n"
        "🩹 *Аптечка:* салфетки, хлоргексидин, пластырь, таблетки для воды, перчатки, пробирки\n"
        "💧 *Вода:* фляга тритан 1л BPA FREE, кружка нержавейка, соль, энергетики\n"
        "📦 *Прочее:* термоодеяло, фольга, силикагель, блокнот, карандаш, инструкция\n\n"
        "💰 Цена: *9 900 ₽* (акция, обычно 12 900 ₽)\n\n"
        "Готов заказать? 👇",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )

# Вопрос
@bot.message_handler(func=lambda m: m.text == "❓ Вопрос")
def question(message):
    bot.send_message(
        message.chat.id,
        "Напиши свой вопрос — Александр ответит лично в ближайшее время 👇",
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(message, forward_question)

def forward_question(message):
    bot.send_message(
        ADMIN_ID,
        f"❓ *Вопрос от покупателя*\n\n"
        f"👤 {message.from_user.first_name} {message.from_user.last_name or ''}\n"
        f"🆔 @{message.from_user.username or 'нет юзернейма'}\n"
        f"💬 {message.text}",
        parse_mode="Markdown"
    )
    bot.send_message(
        message.chat.id,
        "✅ Вопрос отправлен! Александр ответит вам лично.",
        reply_markup=get_main_keyboard()
    )

# Заказ — шаг 1: имя
@bot.message_handler(func=lambda m: m.text == "🛒 Заказать GOBOX")
def order_start(message):
    orders[message.chat.id] = {}
    bot.send_message(
        message.chat.id,
        "Отлично! Оформляем заказ 🛒\n\n*Шаг 1 из 4*\nКак вас зовут? (Имя и фамилия)",
        parse_mode="Markdown",
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(message, get_name)

def get_name(message):
    orders[message.chat.id]['name'] = message.text
    bot.send_message(
        message.chat.id,
        f"*Шаг 2 из 4*\nВаш номер телефона для связи:",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, get_phone)

def get_phone(message):
    orders[message.chat.id]['phone'] = message.text
    bot.send_message(
        message.chat.id,
        f"*Шаг 3 из 4*\nГород и адрес доставки:\n_(например: Краснодар, ул. Ленина 5, кв. 12)_",
        parse_mode="Markdown"
    )
    bot.register_next_step_handler(message, get_address)

def get_address(message):
    orders[message.chat.id]['address'] = message.text
    
    # Кнопки количества
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.row(
        types.KeyboardButton("1 набор — 9 900 ₽"),
        types.KeyboardButton("2 набора — 19 800 ₽")
    )
    keyboard.add(types.KeyboardButton("3 набора — 29 700 ₽"))
    
    bot.send_message(
        message.chat.id,
        f"*Шаг 4 из 4*\nСколько наборов?",
        parse_mode="Markdown",
        reply_markup=keyboard
    )
    bot.register_next_step_handler(message, get_quantity)

def get_quantity(message):
    orders[message.chat.id]['quantity'] = message.text
    order = orders[message.chat.id]
    
    # Подтверждение покупателю
    bot.send_message(
        message.chat.id,
        f"✅ *Заказ принят!*\n\n"
        f"👤 Имя: {order['name']}\n"
        f"📱 Телефон: {order['phone']}\n"
        f"📍 Адрес: {order['address']}\n"
        f"📦 Количество: {order['quantity']}\n\n"
        f"Александр свяжется с вами в течение 2 часов для подтверждения и оплаты.\n\n"
        f"Спасибо за заказ! 🙏",
        parse_mode="Markdown",
        reply_markup=get_main_keyboard()
    )
    
    # Уведомление администратору
    now = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    bot.send_message(
        ADMIN_ID,
        f"🔥 *НОВЫЙ ЗАКАЗ GOBOX!*\n"
        f"⏰ {now}\n\n"
        f"👤 *Имя:* {order['name']}\n"
        f"📱 *Телефон:* {order['phone']}\n"
        f"📍 *Адрес:* {order['address']}\n"
        f"📦 *Количество:* {order['quantity']}\n"
        f"💬 *Telegram:* @{message.from_user.username or 'нет'}\n"
        f"🆔 *ID:* {message.chat.id}",
        parse_mode="Markdown"
    )

# Любое другое сообщение
@bot.message_handler(func=lambda m: True)
def unknown(message):
    bot.send_message(
        message.chat.id,
        "Выбери действие 👇",
        reply_markup=get_main_keyboard()
    )

print("🤖 GOBOX бот запущен...")
bot.infinity_polling()
