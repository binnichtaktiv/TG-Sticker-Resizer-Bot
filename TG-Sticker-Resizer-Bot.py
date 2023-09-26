import telebot
from PIL import Image
import os
import tempfile
import time

bot = telebot.TeleBot("YOUR_BOT_TOKEN")

def resize_and_fill_image(input_path, output_path):
    with Image.open(input_path) as image:
        target_size = (512, 512)
        
        width_ratio = target_size[0] / image.width
        height_ratio = target_size[1] / image.height
        scale_ratio = min(width_ratio, height_ratio)
        
        new_width = int(image.width * scale_ratio)
        new_height = int(image.height * scale_ratio)
        
        new_image = Image.new("RGB", target_size, "black")
        
        x_offset = (target_size[0] - new_width) // 2
        y_offset = (target_size[1] - new_height) // 2
        
        new_image.paste(image.resize((new_width, new_height), Image.LANCZOS), (x_offset, y_offset))
        
        new_image.save(output_path, "PNG")

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hi! I can convert and resize pictures in the right size so that you can send them to the sticker bot. I can only convert one image at a time. If you want to convert multiple images quickly then use my other resizer on github (you can find my github on my website)\n\nMade by @binnichtaktiv\nhttps://binnichtaktiv.github.io")

@bot.message_handler(content_types=['photo'])
def handle_image(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    
    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = os.path.join(temp_dir, 'input.png')
        output_path = os.path.join(temp_dir, 'output.png')
        
        with open(input_path, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        resize_and_fill_image(input_path, output_path)
        
        with open(output_path, 'rb') as img:
            bot.send_document(message.chat.id, img)

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, "Fehler: Bitte senden Sie ein Bild.")

while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        print("Bot crashed. Restarting...")
        time.sleep(10)
