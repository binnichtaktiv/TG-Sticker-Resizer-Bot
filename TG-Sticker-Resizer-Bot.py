import telebot
from PIL import Image
import os
import time

TOKEN = "6400495210:AAFmAqWPnbkfqI8e6AjrCUHTUE8lixqi0rs"
bot = telebot.TeleBot(TOKEN)

def retry_after(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except telebot.apihelper.ApiTelegramException as e:
            if e.error_code == 429:
                wait_time = e.result_json.get('parameters', {}).get('retry_after', 5)
                print(f"Too many requests. Waiting {wait_time} seconds.")
                time.sleep(wait_time)
                return wrapper(*args, **kwargs)
            raise e
    return wrapper

def resize_and_convert_image(input_path, output_path):
    with Image.open(input_path) as image:
        image.thumbnail((512, 512))
        
        if image.size != (512, 512):
            left_margin = (image.width - 512) / 2
            top_margin = (image.height - 512) / 2
            right_margin = (image.width + 512) / 2
            bottom_margin = (image.height + 512) / 2

            image = image.crop((left_margin, top_margin, right_margin, bottom_margin))
        image.save(output_path, "PNG")

@retry_after
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Hi! I can convert and resize pictures in the right size so that you can send them to the sticker bot. I can only convert one image at a time. If you want to convert multiple images quickly then use my other resizer on github (you can find my github on my website)\n\nMade by @binnichtaktiv\nhttps://binnichtaktiv.github.io")

@retry_after
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_id = message.photo[-1].file_id
    file_info = bot.get_file(file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    with open("temp.png", 'wb') as new_file:
        new_file.write(downloaded_file)
    
    resize_and_convert_image("temp.png", "temp_resized.png")
    
    with open("temp_resized.png", 'rb') as photo:
        bot.send_document(message.chat.id, photo)
    
    os.remove("temp.png")
    os.remove("temp_resized.png")

bot.polling(none_stop=True)
