import telebot
from telebot import types

# Initialize the bot with the token
BOT_TOKEN = '7882680466:AAFfYBHVhTgz8cQWJHCztU1AvGUWqXfWdLA'
bot = telebot.TeleBot(BOT_TOKEN)

# Function to handle the callback actions
def handle_question(call):
    questions = {
        'What_is_hackathon': "💻 Хакатон — это мероприятие, на котором команды решают задачи за ограниченное время (24-48 часов).",
        'How_to_participate': "👥 Для участия в хакатоне, зарегистрируйтесь на сайте мероприятия, соберите команду или присоединитесь к уже существующей.",
        'How_to_find_team': "🔗 Найдите команду через специальную площадку участников хакатона или через чаты мероприятия.",
        'About_app': "📲 Приложение HackOrg помогает отслеживать мероприятия, регистрироваться, общаться с участниками и следить за своим прогрессом."
    }
    bot.send_message(call.message.chat.id, questions.get(call.data, "Ошибка: неизвестный запрос."))


def send_qr_code(call):
    try:
        with open('C:/Users/liste/OneDrive/Рабочий стол/Test1/pframe.png', 'rb') as file:
            bot.send_photo(call.message.chat.id, file)
        bot.send_message(call.message.chat.id, "📲 Вот ваш QR-код для входа.")
    except FileNotFoundError:
        bot.send_message(call.message.chat.id, "Ошибка: QR-код не найден.")


def register_user(call):
    bot.send_message(call.message.chat.id, "🎉 Вы успешно зарегистрированы на Hackaton!")


def about_hackorg(call):
    bot.send_message(call.message.chat.id,
                     "🤖 HackOrg — это организация, которая проводит хакатоны и другие мероприятия для поддержки IT-сообщества.")


def upcoming_events(call):
    bot.send_message(call.message.chat.id,
                     "📅 Ближайшие события:\n1️⃣ Хакатон 'Зимний кодинг' — 12 января ❄️\n2️⃣ Летний хакатон 'CyberTech' — 15 июня ☀️.")


# Start command - Initial menu with options
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()

    # Add buttons to the menu, each button in a separate row
    markup.row(types.InlineKeyboardButton('🧐 Ответь на мой вопрос', callback_data='question'))
    markup.row(types.InlineKeyboardButton('ℹ️ Узнать о HackOrg', callback_data='about_hackorg'))
    markup.row(types.InlineKeyboardButton('📝 Зарегистрируй меня в Hackaton', callback_data='register_hackaton'))
    markup.row(types.InlineKeyboardButton('📲 Дай мне QR для входа', callback_data='qr_entry'))
    markup.row(types.InlineKeyboardButton('🎉 Расскажи о ближайших событиях', callback_data='upcoming_events'))

    bot.send_message(
        message.chat.id,
        f'Привет, {message.from_user.first_name}! 👋 Я бот Hack.Org, меня зовут Бэни 🤖. Как я могу вам помочь?',
        reply_markup=markup
    )


# Callback handler for button interactions
@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    bot.answer_callback_query(call.id)

    # Mapping callback data to specific functions
    actions = {
        'question': lambda call: show_questions(call),
        'register_hackaton': register_user,
        'qr_entry': send_qr_code,
        'about_hackorg': about_hackorg,
        'upcoming_events': upcoming_events
    }

    # Default to handling question-related callbacks
    if call.data in actions:
        actions[call.data](call)
    else:
        handle_question(call)


# Submenu to show questions
def show_questions(call):
    markup = types.InlineKeyboardMarkup()
    markup.row(types.InlineKeyboardButton('🤔 Что такое хакатон?', callback_data='What_is_hackathon'))
    markup.row(types.InlineKeyboardButton('🏃 Как принять участие в хакатоне?', callback_data='How_to_participate'))
    markup.row(types.InlineKeyboardButton('🔍 Как найти команду?', callback_data='How_to_find_team'))
    markup.row(types.InlineKeyboardButton('📱 Расскажи о приложении HackOrg', callback_data='About_app'))

    bot.send_message(call.message.chat.id, "На какой вопрос вы хотите получить ответ? 🤓", reply_markup=markup)


# Help command or specific info
@bot.message_handler(commands=['help', 'bushido_dzo', 'reset'])
def send_help(message):
    if message.text == '/help':
        bot.send_message(message.chat.id,
                         'Напишите /start для открытия меню. Это поможет вам узнать о хакатонах, зарегистрироваться или получить полезную информацию.')


# Handle other text messages
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    if message.text.lower() == "привет":
        bot.send_message(message.chat.id, "Привет! Как настроение?")
    else:
        bot.send_message(message.chat.id, f"Хмм... думаю над вашим запросом... 🤔")


# Start bot polling
bot.polling(none_stop=True)

