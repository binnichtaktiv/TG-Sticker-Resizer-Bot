import telebot
from PIL import Image
import os

TOKEN = "YOUR_BOT_TOKEN_HERE"
bot = telebot.TeleBot(TOKEN)

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

bot.polling()
