import telebot
import os
from datetime import datetime
import random
import re

# Replace with your actual Bot Token
API_TOKEN = '7813890682:AAFfxPjkS8gaW_QO-l_gTceQwErmj2ONMvs'

# Replace with your group chat ID
GROUP_CHAT_ID = -1002376294175  # Example: replace with your actual group chat ID

bot = telebot.TeleBot(API_TOKEN)

# Directories to save GIFs and Stickers
SAVE_DIRECTORY = "saved_files"

# Ensure directory exists
if not os.path.exists(SAVE_DIRECTORY):
    os.makedirs(SAVE_DIRECTORY)

# Separate lists for saved GIFs and stickers by their type
saved_lfg_files = []  # Files saved with `/save.lfg`
saved_pump_files = []  # Files saved with `/save.pump`

# Function to handle replies with the "/save.lfg" command
@bot.message_handler(func=lambda message: message.reply_to_message and message.text.lower().startswith('/save'))
def save_file(message):
    global saved_lfg_files, saved_pump_files

    if message.reply_to_message and (message.reply_to_message.animation or message.reply_to_message.sticker):
        # Determine the type of save based on the command
        if 'pump' in message.text.lower():
            save_type = 'pump'
        elif 'lfg' in message.text.lower():
            save_type = 'lfg'
        else:
            bot.reply_to(message, "Please specify '/save lfg' or '/save pump'.")
            return

        file_id = None
        file_path = None

        if message.reply_to_message.animation:
            # Handle GIFs
            file_id = message.reply_to_message.animation.file_id
            file_info = bot.get_file(file_id)
            file_path = os.path.join(SAVE_DIRECTORY, f"{file_id}.gif")
        elif message.reply_to_message.sticker:
            # Handle Stickers
            file_id = message.reply_to_message.sticker.file_id
            file_info = bot.get_file(file_id)
            file_path = os.path.join(SAVE_DIRECTORY, f"{file_id}.webp")

        if file_info:
            downloaded_file = bot.download_file(file_info.file_path)
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            if save_type == 'pump':
                saved_pump_files.append(file_id)
                bot.reply_to(message, "File saved for Pump commands.")
            elif save_type == 'lfg':
                saved_lfg_files.append(file_id)
                bot.reply_to(message, "File saved for LFG commands.")
        else:
            bot.reply_to(message, "Could not download the file.")

# Handle sending random saved LFG GIFs or stickers when "/lfg" is typed
@bot.message_handler(func=lambda message: message.chat.id == GROUP_CHAT_ID and message.text.lower() == '/lfg')
def send_random_lfg_file(message):
    if saved_lfg_files:
        file_id = random.choice(saved_lfg_files)
        file_path = os.path.join(SAVE_DIRECTORY, f"{file_id}.gif") if file_id.endswith('.gif') else os.path.join(SAVE_DIRECTORY, f"{file_id}.webp")
        
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                if file_path.endswith(".gif"):
                    bot.send_animation(message.chat.id, file)
                else:
                    bot.send_sticker(message.chat.id, file)
        else:
            bot.reply_to(message, "Saved LFG file could not be found.")

# Handle sending random saved pump GIFs or stickers when "/pump" is typed
@bot.message_handler(func=lambda message: message.chat.id == GROUP_CHAT_ID and message.text.lower() == '/pump')
def send_random_pump_file(message):
    if saved_pump_files:
        file_id = random.choice(saved_pump_files)
        file_path = os.path.join(SAVE_DIRECTORY, f"{file_id}.gif") if file_id.endswith('.gif') else os.path.join(SAVE_DIRECTORY, f"{file_id}.webp")
        
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                if file_path.endswith(".gif"):
                    bot.send_animation(message.chat.id, file)
                else:
                    bot.send_sticker(message.chat.id, file)
        else:
            bot.reply_to(message, "Saved Pump file could not be found.")

# Start polling
bot.polling(none_stop=True)
