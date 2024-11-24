import telebot
from pydub import AudioSegment
import os
from audio_processing import AudioSignalEntropy


# constants
TOKEN = "YOUR TOKEN"
AUDIOS_STORING_FOLDER = "audio_storage"
FIGURES_STORING_FOLDER = "figures_storage"


# utils
def entropy_of_signal(signal_entropy: AudioSignalEntropy = None, audio_file_path: str = None, option: int = None):
    if signal_entropy is None:
        signal_entropy = AudioSignalEntropy(figures_storage_path = FIGURES_STORING_FOLDER, audio_file_path = audio_file_path, option = option)
    signal_entropy.update_signal(audio_file_path, option)
    return (signal_entropy.signal_fig_path, 
            signal_entropy.fft_fig_path, 
            signal_entropy.distribution_fig_path, 
            signal_entropy.histogram_fig_path,
            signal_entropy.entropy)


def send_photos(bot, message_chat_id, photos):
    for photo_path in photos:
        with open(photo_path, 'rb') as photo_file:
            bot.send_document(message_chat_id, photo_file)


def clean_up_folder(folder_path):
    for filename in os.listdir(folder_path): 
        file_path = f"{folder_path}/{filename}" 
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)  
            elif os.path.isdir(file_path):  
                os.rmdir(file_path)  
        except Exception as e:  
            print(f"Error deleting {file_path}: {e}")
        

# bot session stuff
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start"])
def start(message):
    mess = f"Hello, <b>{message.from_user.first_name} <u>{'Send me a voice message'}</u></b>"
    bot.send_message(message.chat.id, mess, parse_mode="html")


@bot.message_handler(commands=["sample"])
def handle_sample(message):
    # option=1
    (signal_fig_path, 
     fft_fig_path, 
     distribution_fig_path, 
     histogram_fig_path, 
     entropy) = entropy_of_signal(option=1)
    send_photos(bot, message.chat.id, [signal_fig_path, fft_fig_path, distribution_fig_path, histogram_fig_path])
    bot.reply_to(message, f"Entropy of sine wave with frequency 440 Hz equals to {entropy}.")
    # option=2
    (signal_fig_path, 
     fft_fig_path, 
     distribution_fig_path, 
     histogram_fig_path, 
     entropy) = entropy_of_signal(option=2)
    send_photos(bot, message.chat.id, [signal_fig_path, fft_fig_path, distribution_fig_path, histogram_fig_path])
    bot.reply_to(message, f"Entropy of noisy sine wave with frequency 440 Hz equals to {entropy}.")
    # option=3
    (signal_fig_path, 
     fft_fig_path, 
     distribution_fig_path, 
     histogram_fig_path, 
     entropy) = entropy_of_signal(option=3)
    send_photos(bot, message.chat.id, [signal_fig_path, fft_fig_path, distribution_fig_path, histogram_fig_path])
    bot.reply_to(message, f"Entropy of gauss noise equals to {entropy}.")
    # option=4
    (signal_fig_path, 
     fft_fig_path, 
     distribution_fig_path, 
     histogram_fig_path, 
     entropy) = entropy_of_signal(option=4)
    send_photos(bot, message.chat.id, [signal_fig_path, fft_fig_path, distribution_fig_path, histogram_fig_path])
    bot.reply_to(message, f"Entropy of uniform noise equals to {entropy}.")


@bot.message_handler(content_types=["voice"])
def handle_audio_message(message):
    wav_file_name = ""
    try:
        # Get the file information
        file_info = bot.get_file(message.voice.file_id)
        file_path = file_info.file_path
        # Download the file
        downloaded_file = bot.download_file(file_path)
        ogg_file_name = f"{AUDIOS_STORING_FOLDER}/{message.voice.file_id}.ogg"
        with open(ogg_file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        # Convert OGG to WAV
        bot.reply_to(message, "Audio received! Converting to .wav...")
        wav_file_name = f"{AUDIOS_STORING_FOLDER}/{message.voice.file_id}.wav"
        audio = AudioSegment.from_file(ogg_file_name, format="ogg")
        audio.export(wav_file_name, format="wav")
        bot.reply_to(message, f"Saved as {wav_file_name}")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")
    try:
        # audio to entropy and figures
        (signal_fig_path, 
         fft_fig_path, 
         distribution_fig_path, 
         histogram_fig_path, 
         entropy) = entropy_of_signal(audio_file_path=wav_file_name)
        send_photos(bot, message.chat.id, [signal_fig_path, fft_fig_path, distribution_fig_path, histogram_fig_path])
        bot.reply_to(message, f"Entropy of this signal equals to {entropy}.")
    except Exception as e:
        bot.reply_to(message, f"An error occurred: {e}")
    finally:
        clean_up_folder(AUDIOS_STORING_FOLDER)
        clean_up_folder(FIGURES_STORING_FOLDER)
    

# main loop
def main():
    bot.polling() # none_stop=True

# if __name__ == '__main__':
#     main()


