import telebot
import os
from datetime import datetime
import random

# Replace with your actual Bot Token
API_TOKEN = '7813890682:AAFfxPjkS8gaW_QO-l_gTceQwErmj2ONMvs'

# Replace with your group chat ID
GROUP_CHAT_ID = -1002383486624 # Example: replace with your actual group chat ID

bot = telebot.TeleBot(API_TOKEN)

# Define the directory to save the GIF
GIF_DIRECTORY = "saved_gifs"

# Make sure the GIF directory exists
if not os.path.exists(GIF_DIRECTORY):
    os.makedirs(GIF_DIRECTORY)

# List to store the file_id of the 3 saved GIFs
saved_gifs = []

# Function to handle incoming GIF messages

# Function to handle replies with the "/save" command
@bot.message_handler(func=lambda message: message.reply_to_message and message.text.lower() == '/save')
def save_gif(message):
    global saved_gifs

    # Check if the message is a reply to a GIF
    if message.reply_to_message and message.reply_to_message.animation:
        # Get the GIF file_id
        gif_id = message.reply_to_message.animation.file_id
        
        # Download the GIF
        file_info = bot.get_file(gif_id)
        downloaded_file = bot.download_file(file_info.file_path)

        # Save the GIF to the bot's local storage
        gif_path = os.path.join(GIF_DIRECTORY, f"{gif_id}.gif")
        with open(gif_path, 'wb') as new_file:
            new_file.write(downloaded_file)

        # Add to saved GIFs list
        saved_gifs.append(gif_id)
        bot.reply_to(message, "GIF saved! You can now request it with LFG.")

    else:
        bot.reply_to(message, "Please reply to a GIF with /save to save it.")

# Function to check if the message contains "lfg" or "LFG"
@bot.message_handler(func=lambda message: message.chat.id == GROUP_CHAT_ID and ('lfg' in message.text.lower()))
def send_random_gif(message):

    # Randomly choose one of the saved GIFs
    if len(saved_gifs) >= 1:
        gif_id = random.choice(saved_gifs)

        # Construct the path to the saved GIF
        gif_path = os.path.join(GIF_DIRECTORY, f"{gif_id}.gif")

        # Send the random GIF
        with open(gif_path, 'rb') as gif_file:
            bot.send_animation(message.chat.id, gif_file)

@bot.message_handler(func=lambda message: message.reply_to_message and message.text.lower() == '/delete')
def delete_gif(message):
    global saved_gifs

    # Check if the message is a reply to a GIF
    if message.reply_to_message and message.reply_to_message.animation:
        gif_id = message.reply_to_message.animation.file_id
        
        # Check if the GIF is in the saved GIFs list
        if gif_id in saved_gifs:
            # Remove the GIF from the saved_gifs list
            saved_gifs.remove(gif_id)
            
            # Construct the path to the GIF file
            gif_path = os.path.join(GIF_DIRECTORY, f"{gif_id}.gif")
            
            # Delete the GIF file from the local storage
            if os.path.exists(gif_path):
                os.remove(gif_path)
                bot.reply_to(message, "GIF deleted successfully.")
            else:
                bot.reply_to(message, "Error: GIF file not found.")
        else:
            bot.reply_to(message, "This GIF is not saved.")
    else:
        bot.reply_to(message, "Please reply to a saved GIF with /delete to delete it.")


# Start polling
bot.polling(none_stop=True)