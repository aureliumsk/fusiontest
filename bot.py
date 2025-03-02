from telebot.types import Message, InputFile
import telebot
import config
import kadinsky
import io
import time
import random

DELAY = 5.0
TRIES = 10

cfg = config.load()
bot = telebot.TeleBot(cfg.telegram_api_key)
kd = kadinsky.Kadinsky(cfg)

messages = [
    "Обнимаем хороших людей...",
    "Взываем к древним богам...",
    "Колдуем...",
    "Рубим ввод на биты...",
    "Прогоняем вывод через base64...",
]

@bot.message_handler(commands=["start", "help"])
def help(message: Message):
    bot.reply_to(message, """Я - бот-генератор изображений!
Введи любой промпт, и получишь в ответ сгенерированное изображение!""")

@bot.message_handler(func=lambda message: True)
def generate_image(message: Message):
    prompt = message.text
    uuid = kd.generate(prompt)

    bot_message_id = bot.reply_to(message, "Начинаем генерацию изображения...").id

    tries = TRIES

    prev: str | None = None
    
    while tries > 0:
        image = kd.check_available(uuid)
        if image is not None:
            break
        tries -= 1
        time.sleep(DELAY)
        text = random.choice(messages)
        if text == prev:
            continue
        bot.edit_message_text(text, message.chat.id, bot_message_id)
        prev = text
    bot.delete_message(message.chat.id, bot_message_id) 
    img = InputFile(io.BytesIO(image), file_name=f"{prompt}.jpg")
    bot.send_photo(message.chat.id, img, caption="Генерация завершена! ;)") 

bot.infinity_polling()


