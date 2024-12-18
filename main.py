import telebot
import os
import random

# Replace with your actual Bot Token
API_TOKEN = '7813890682:AAFfxPjkS8gaW_QO-l_gTceQwErmj2ONMvs'

# Replace with your group chat ID
GROUP_CHAT_ID = -1002376294175  # Example: replace with your actual group chat ID

bot = telebot.TeleBot(API_TOKEN)

# Directory to save the GIFs and stickers
GIF_DIRECTORY = "saved_gifs"

# Ensure save directory exists
if not os.path.exists(GIF_DIRECTORY):
    os.makedirs(GIF_DIRECTORY)

# Lists to store saved file paths
saved_lfg_files = []
saved_pump_files = []


# Function to check if the file should already exist
def file_already_saved(file_path, saved_list):
    """
    Check if the file is already saved in the list.
    """
    return file_path in saved_list


# Function to handle replies with the "/add" command
@bot.message_handler(func=lambda message: message.reply_to_message and message.text.lower().startswith('/add'))
def save_file(message):
    global saved_lfg_files, saved_pump_files

    print("Received command:", message.text)  # Log the full command
    if message.reply_to_message:
        # Detect if it’s an animation or sticker
        if message.reply_to_message.animation:
            print("Found GIF in reply.")
            file_id = message.reply_to_message.animation.file_id
            save_path = os.path.join(GIF_DIRECTORY, f"{file_id}.gif")
        elif message.reply_to_message.sticker:
            print("Found sticker in reply.")
            file_id = message.reply_to_message.sticker.file_id
            save_path = os.path.join(GIF_DIRECTORY, f"{file_id}.webp")
        else:
            bot.reply_to(message, "No animation or sticker found in the reply.")
            return

        # Determine if user wants to save to LFG or Pump and only check that specific list
        if 'pump' in message.text.lower():
            # Only check the Pump collection
            if save_path in saved_pump_files:
                bot.reply_to(message, "This file is already saved to the Pump collection.")
                print("Skipping save for Pump files.")
                return
        elif 'lfg' in message.text.lower():
            # Only check the LFG collection
            if save_path in saved_lfg_files:
                bot.reply_to(message, "This file is already saved to the LFG collection.")
                print("Skipping save for LFG files.")
                return

        # Proceed to download and save only if checks pass
        try:
            file_info = bot.get_file(file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            with open(save_path, 'wb') as f:
                f.write(downloaded_file)

            # Log the saved path for debugging
            print("Saved file at:", save_path)

            # Determine save type
            if 'pump' in message.text.lower():
                saved_pump_files.append(save_path)
                bot.reply_to(message, "Saved to Pump collection.")
                print("Pump files saved:", saved_pump_files)
            elif 'lfg' in message.text.lower():
                saved_lfg_files.append(save_path)
                bot.reply_to(message, "Saved to LFG collection.")
                print("LFG files saved:", saved_lfg_files)

        except Exception as e:
            bot.reply_to(message, f"Failed to save file: {str(e)}")
            print("Error during download/save:", e)

# Handle sending random saved LFG GIFs or stickers when "/lfg" is typed
@bot.message_handler(func=lambda message: message.text.lower() == '/lfg')
def send_random_lfg_file(message):
    print("Triggered /lfg command.")

    if saved_lfg_files:
        file_path = random.choice(saved_lfg_files)
        try:
            print("Sending LFG file:", file_path)
            with open(file_path, 'rb') as file:
                bot.send_animation(message.chat.id, file)
            print("LFG file sent successfully.")
        except Exception as e:
            bot.reply_to(message, f"Failed to send LFG file: {str(e)}")
            print("Error:", e)
    else:
        bot.reply_to(message, "No LFG files are saved.")


# Handle sending random saved Pump GIFs or stickers when "/pump" is typed
@bot.message_handler(func=lambda message: message.text.lower() == '/pump')
def send_random_pump_file(message):
    print("Triggered /pump command.")

    if saved_pump_files:
        file_path = random.choice(saved_pump_files)
        try:
            print("Sending Pump file:", file_path)
            with open(file_path, 'rb') as file:
                bot.send_animation(message.chat.id, file)
            print("Pump file sent successfully.")
        except Exception as e:
            bot.reply_to(message, f"Failed to send Pump file: {str(e)}")
            print("Error:", e)
    else:
        bot.reply_to(message, "No Pump files are saved.")

# Function to handle replies with the "/delete" command
@bot.message_handler(func=lambda message: message.reply_to_message and message.text.lower() == '/delete')
def delete_file(message):
    global saved_lfg_files, saved_pump_files

    print("Triggered /delete command.")
    if message.reply_to_message:
        # Check if it's an animation or sticker
        if message.reply_to_message.animation:
            file_id = message.reply_to_message.animation.file_id
            file_path = os.path.join(GIF_DIRECTORY, f"{file_id}.gif")
        elif message.reply_to_message.sticker:
            file_id = message.reply_to_message.sticker.file_id
            file_path = os.path.join(GIF_DIRECTORY, f"{file_id}.webp")
        else:
            bot.reply_to(message, "No animation or sticker found in the reply.")
            return

        # Log the computed path for debugging
        print("Attempting to delete file:", file_path)

        # Attempt to delete the file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)  # Remove the actual file from the system
                # Remove from saved lists
                if file_path in saved_lfg_files:
                    saved_lfg_files.remove(file_path)
                    bot.reply_to(message, "LFG file deleted successfully.")
                    print("Deleted from LFG files:", saved_lfg_files)
                if file_path in saved_pump_files:
                    saved_pump_files.remove(file_path)
                    bot.reply_to(message, "Pump file deleted successfully.")
                    print("Deleted from Pump files:", saved_pump_files)
            except Exception as e:
                bot.reply_to(message, f"Failed to delete file: {str(e)}")
                print("Error during delete:", e)
        else:
            # Handle cases where the file doesn't exist but is still in the list
            if file_path in saved_lfg_files:
                saved_lfg_files.remove(file_path)
                bot.reply_to(message, "LFG file reference removed.")
                print("Removed reference from LFG files.")
            if file_path in saved_pump_files:
                saved_pump_files.remove(file_path)
                bot.reply_to(message, "Pump file reference removed.")
                print("Removed reference from Pump files.")


# Start polling
bot.infinity_polling()
