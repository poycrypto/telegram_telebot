import telebot
import os
from datetime import datetime
import random

# Replace with your actual Bot Token
API_TOKEN = '7813890682:AAFfxPjkS8gaW_QO-l_gTceQwErmj2ONMvs'

# Replace with your group chat ID
GROUP_CHAT_ID = -1002376294175  # Example: replace with your actual group chat ID

bot = telebot.TeleBot(API_TOKEN)

# Define the directories to save the GIFs and stickers
SAVE_DIRECTORY = "saved_files"

# Make sure the save directory exists
if not os.path.exists(SAVE_DIRECTORY):
    os.makedirs(SAVE_DIRECTORY)

# List to store the file_ids of the saved files
saved_files = []

# Function to handle replies with the "/save" command
@bot.message_handler(func=lambda message: message.reply_to_message and message.text.lower() == '/save')
def save_file(message):
    global saved_files

    # Check if the message is a reply to a GIF or sticker
    if message.reply_to_message and (message.reply_to_message.animation or message.reply_to_message.sticker):
        # Determine the file type (GIF or sticker)
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

        # Download the file
        if file_info:
            downloaded_file = bot.download_file(file_info.file_path)
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            # Add to saved files list
            saved_files.append(file_id)
            bot.reply_to(message, "File saved! You can now request it with LFG.")
        else:
            bot.reply_to(message, "Could not download the file.")

    else:
        bot.reply_to(message, "Please reply to a GIF or sticker with /save to save it.")


# Function to check if the message contains "lfg" or "LFG"
@bot.message_handler(func=lambda message: message.chat.id == GROUP_CHAT_ID and ('lfg' in message.text.lower()))
def send_random_file(message):
    if len(saved_files) >= 1:
        # Randomly choose one of the saved files
        file_id = random.choice(saved_files)
        file_path = os.path.join(SAVE_DIRECTORY, f"{file_id}.gif") if file_id.endswith(".gif") else os.path.join(SAVE_DIRECTORY, f"{file_id}.webp")

        # Send the file
        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                if file_path.endswith('.gif'):
                    bot.send_animation(message.chat.id, file)
                else:
                    bot.send_sticker(message.chat.id, file)
        else:
            bot.reply_to(message, "File does not exist, try again.")

# Handle deleting files via "/delete"
@bot.message_handler(func=lambda message: message.reply_to_message and message.text.lower() == '/delete')
def delete_file(message):
    global saved_files

    # Check if the message is a reply to a GIF or sticker
    if message.reply_to_message and (message.reply_to_message.animation or message.reply_to_message.sticker):
        file_id = None
        file_path = None

        if message.reply_to_message.animation:
            file_id = message.reply_to_message.animation.file_id
            file_path = os.path.join(SAVE_DIRECTORY, f"{file_id}.gif")
        elif message.reply_to_message.sticker:
            file_id = message.reply_to_message.sticker.file_id
            file_path = os.path.join(SAVE_DIRECTORY, f"{file_id}.webp")

        # Remove the file from the saved files list and delete it
        if file_id and file_id in saved_files:
            saved_files.remove(file_id)
            if os.path.exists(file_path):
                os.remove(file_path)
                bot.reply_to(message, "File deleted successfully.")
            else:
                bot.reply_to(message, "Error: File not found.")
        else:
            bot.reply_to(message, "This file is not saved.")
    else:
        bot.reply_to(message, "Please reply to a saved GIF or sticker with /delete to delete it.")


# Start polling
bot.polling(none_stop=True)
