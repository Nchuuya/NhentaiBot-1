# ---------------- IMPORTS -------------
import logging
from nhentaiBot.helpers.functions import about
from nhentaiBot.helpers.conversation_query import s_conv, s_with_q, cancel, single_manga
from nhentaiBot import dp, updater
from telegram import InlineKeyboardMarkup
from telegram.ext import CommandHandler, InlineQueryHandler, MessageHandler, ConversationHandler, Filters, CallbackQueryHandler
from nhentaiBot.helpers.Inline_query import search_query
from nhentaiBot.helpers.Inline_keyboard import search_k
from nhentaiBot.helpers.constants import DEL_FAIL_LOG
from nhentaiBot.pyfunc.download_func import download_func
from nhentaiBot.helpers.callback_functions import download_manga_callback, s_search_callback, single_manga_callback

# ---------------- FUNCTIONS ------------


def start(update, context):
    text = """
Type `/help` to see all Commands.
To Start Inline select:
"""

    # Keyboard markup for Search here and Share
    reply_markup = InlineKeyboardMarkup(search_k)

    # Sending bot Message
    context.bot.sendMessage(chat_id=update.message.chat_id,
                            text=text, parse_mode="Markdown", reply_markup=reply_markup)
    try:
        # Deleting the User command message
        context.bot.deleteMessage(
            chat_id=update.message.chat_id, message_id=update.message.message_id)

    except Exception as e:
        # Loging the error if unable to delete message due to insufficient permission
        logging.error(DEL_FAIL_LOG)


def help(update, context):
    text = """\
`start` : `to start the bot`
`code`  : `read/download with code`
`search`: `Search nHentia`
`about` : `About BOT`
"""
    try:
        context.bot.deleteMessage(
            chat_id=update.message.chat_id, message_id=update.message.message_id)
    except Exception as e:
        logging.error(DEL_FAIL_LOG)
    context.bot.sendMessage(chat_id=update.message.chat_id,
                            text=text, parse_mode="Markdown")


def status(update, context):
    text = "`Status up`"
    context.bot.sendMessage(chat_id=update.message.chat_id,
                            text=text, parse_mode="Markdown")
    try:
        context.bot.deleteMessage(
            chat_id=update.message.chat_id, message_id=update.message.message_id)
    except Exception as e:
        logging.error(DEL_FAIL_LOG)


def main():

    # -------- COMMANDS ----------
    dp.add_handler(CommandHandler("nhstart", nhstart, run_async=True))
    dp.add_handler(CommandHandler("nhstatus", nhstatus, run_async=True))
    dp.add_handler(CommandHandler("nhhelp", nhhelp, run_async=True))
    dp.add_handler(CommandHandler("code", single_manga, run_async=True))
    dp.add_handler(InlineQueryHandler(search_query))
    dp.add_handler(ConversationHandler(entry_points=[CommandHandler('search', s_conv, run_async=True)],
                                       states={
                                           999: [MessageHandler(Filters.text & ~ Filters.command, s_with_q)]
    },
        fallbacks=[CommandHandler(
            'cancel', cancel, run_async=True)],
        conversation_timeout=10,
        allow_reentry=True))
    dp.add_handler(CallbackQueryHandler(
        s_search_callback, pattern="^search#"))
    dp.add_handler(CallbackQueryHandler(single_manga, pattern="^read#"))
    dp.add_handler(CallbackQueryHandler(
        single_manga_callback, pattern="^manga_p#"))
    dp.add_handler(CallbackQueryHandler(
        download_manga_callback, pattern="^download#"))
    dp.add_handler(CommandHandler("about", about, run_async=True))
    dp.add_handler(CallbackQueryHandler(about, pattern="^about_com$"))

    # --------- System Polling ------------
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
