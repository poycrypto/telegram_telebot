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
@bot.message_handler(func=lambda message: message.reply_to_message and message.text.lower() == '/save.lfg')
def save_lfg_file(message):
    global saved_lfg_files

    if message.reply_to_message and (message.reply_to_message.animation or message.reply_to_message.sticker):
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

            saved_lfg_files.append(file_id)
            bot.reply_to(message, "File saved to trigger with LFG command.")
        else:
            bot.reply_to(message, "Could not download the file.")

# Function to handle replies with the "/save.pump" command
@bot.message_handler(func=lambda message: message.reply_to_message and message.text.lower() == '/save.pump')
def save_pump_file(message):
    global saved_pump_files

    if message.reply_to_message and (message.reply_to_message.animation or message.reply_to_message.sticker):
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

            saved_pump_files.append(file_id)
            bot.reply_to(message, "File saved to trigger with Pump commands.")
        else:
            bot.reply_to(message, "Could not download the file.")

# Handle sending random saved LFG GIFs or stickers only if "save" isn't in the message
@bot.message_handler(func=lambda message: message.chat.id == GROUP_CHAT_ID and 'lfg' in message.text.lower() and 'save' not in message.text.lower())
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

# Handle sending random saved pump GIFs or stickers only if "save" is in the message
@bot.message_handler(func=lambda message: message.chat.id == GROUP_CHAT_ID and re.search(r'\bpump(b| it| it|m+p)\b', message.text.lower()) and 'save' in message.text.lower())
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
            bot.reply_to(message, "Saved pump file could not be found.")

# Start polling
bot.polling(none_stop=True)
