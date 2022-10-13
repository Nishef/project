from asyncore import dispatcher
from lib2to3.pgen2 import token
from click import command
from telegram.ext.updater import Updater
from telegram.update import Update
from telegram.ext import *
from telegram import *
import telegram
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

GENDER, PHOTO, LOCATION, BIO = range(4)

TOKEN="5078266943:AAFilX0b3oV3MeIzciEm8EHx8_1x6MaZ4cI"
# ai_mallbot :5078266943:AAFilX0b3oV3MeIzciEm8EHx8_1x6MaZ4cI
# Nishef_bot :5047116093:AAHEh-MZaTTBRQCJV5xBr0QKUKph8A3zzKA
# pp = telegram.utils.request.Request(proxy_url='socks5://127.0.0.1:1080')
# bot=Updater(token="5047116093:AAHEh-MZaTTBRQCJV5xBr0QKUKph8A3zzKA")
# dispatcher = bot.dispatcher
# def startCommand(update, context):
#     pass

# bot.start_polling()


bot = telegram.Bot(token=TOKEN)
# updates = bot.get_updates()
# print(bot.get_me())
# print(updates[0])
# How to send a message to user?
# How to get an output from python and show it on bot to an specific user
# def error_callback(update, context):
#     logger.warning('Update "%s" caused error "%s"', update, context.error)
# bot.send_message(message.chat.id)

updater = Updater(TOKEN, use_context=True)

def log_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as exc:
            print(f'Error: {exc}')
            raise exc

    return wrapper

#!Maximum file size to download is 20 MB.
def downloader(update, context):
    context.bot.get_file(update.message.document).download()

    # writing to a custom file
    # with open("C:/Datas/Telegram Bot/file.doc", 'wb') as f:
    #     context.bot.get_file(update.message.document).download(out=f)
def image_handler(update,context):
    # file = context.bot.getFile(update.message.photo[-1].file_id)
    # print ("file_id: " + str(update.message.photo.file_id))
    # file.download('image.jpg')
    file = update.message.photo[-1].get_file()
    path = file.download("output.jpg")
def audio_handler(update,context):
    file = context.bot.getFile(update.message.audio).download()
    

def send_image(update, context):
    context.bot.send_photo(update.message.chat_id, photo=open('C:/Datas/Telegram Bot/output.jpg', 'rb'),timeout=1000)

#------------------------------------------

# def start(update: Update, context: CallbackContext) -> None:
#     """Sends a message with three inline buttons attached."""
#     keyboard = [
#         [
#             InlineKeyboardButton("Option 1", callback_data='1'),
#             InlineKeyboardButton("Option 2", callback_data='2'),
#         ],
#         [InlineKeyboardButton("Option 3", callback_data='3')],
#     ]

#     reply_markup = InlineKeyboardMarkup(keyboard)

#     update.message.reply_text('Please choose:', reply_markup=reply_markup)


# def button(update: Update, context: CallbackContext) -> None:
#     """Parses the CallbackQuery and updates the message text."""
#     query = update.callback_query

#     # CallbackQueries need to be answered, even if no notification to the user is needed
#     # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
#     query.answer()

#     query.edit_message_text(text=f"Selected option: {query.data}")

def start(update: Update, context: CallbackContext) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [['Boy', 'Girl', 'Other']]

    update.message.reply_text(
        'Hi! My name is Professor Bot. I will hold a conversation with you. '
        'Send /cancel to stop talking to me.\n\n'
        'Are you a boy or a girl?',
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder='Boy or Girl?'
        ),
    )

    return GENDER



def gender(update: Update, context: CallbackContext) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    logger.info("Gender of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'I see! Please send me a photo of yourself, '
        'so I know what you look like, or send /skip if you don\'t want to.',
        reply_markup=ReplyKeyboardRemove(),
    )

    return PHOTO


def photo(update: Update, context: CallbackContext) -> int:
    """Stores the photo and asks for a location."""
    user = update.message.from_user
    photo_file = update.message.photo[-1].get_file()
    photo_file.download('user_photo.jpg')
    logger.info("Photo of %s: %s", user.first_name, 'user_photo.jpg')
    update.message.reply_text(
        'Gorgeous! Now, send me your location please, or send /skip if you don\'t want to.'
    )

    return LOCATION


def skip_photo(update: Update, context: CallbackContext) -> int:
    """Skips the photo and asks for a location."""
    user = update.message.from_user
    logger.info("User %s did not send a photo.", user.first_name)
    update.message.reply_text(
        'I bet you look great! Now, send me your location please, or send /skip.'
    )

    return LOCATION


def location(update: Update, context: CallbackContext) -> int:
    """Stores the location and asks for some info about the user."""
    user = update.message.from_user
    user_location = update.message.location
    logger.info(
        "Location of %s: %f / %f", user.first_name, user_location.latitude, user_location.longitude
    )
    update.message.reply_text(
        'Maybe I can visit you sometime! At last, tell me something about yourself.'
    )

    return BIO


def skip_location(update: Update, context: CallbackContext) -> int:
    """Skips the location and asks for info about the user."""
    user = update.message.from_user
    logger.info("User %s did not send a location.", user.first_name)
    update.message.reply_text(
        'You seem a bit paranoid! At last, tell me something about yourself.'
    )

    return BIO


def bio(update: Update, context: CallbackContext) -> int:
    """Stores the info about the user and ends the conversation."""
    user = update.message.from_user
    logger.info("Bio of %s: %s", user.first_name, update.message.text)
    update.message.reply_text('Thank you! I hope we can talk again some day.')

    return ConversationHandler.END


def cancel(update: Update, context: CallbackContext) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        'Bye! I hope we can talk again some day.', reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END



# updater.dispatcher.add_handler(MessageHandler(Filters.document, downloader))
# updater.dispatcher.add_handler(MessageHandler(Filters.photo, image_handler))
# updater.dispatcher.add_handler(MessageHandler(Filters.audio, audio_handler))
# updater.dispatcher.add_handler(CommandHandler("send_image", send_image))
updater.dispatcher.add_handler(CommandHandler('start', start))
# updater.dispatcher.add_handler(CallbackQueryHandler(button))
# updater.dispatcher.add_handler(CommandHandler('help', help_command))
    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
conv_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        GENDER: [MessageHandler(Filters.regex('^(Boy|Girl|Other)$'), gender)],
        PHOTO: [MessageHandler(Filters.photo, photo), CommandHandler('skip', skip_photo)],
        LOCATION: [
            MessageHandler(Filters.location, location),
            CommandHandler('skip', skip_location),
        ],
        BIO: [MessageHandler(Filters.text & ~Filters.command, bio)],
    },
    fallbacks=[CommandHandler('cancel', cancel)],
)
updater.dispatcher.add_handler(conv_handler)

# Start the Bot
updater.start_polling()

# Run the bot until you press Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT. This should be used most of the time, since
# start_polling() is non-blocking and will stop the bot gracefully.
updater.idle()