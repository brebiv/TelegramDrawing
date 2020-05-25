from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler
from bot.view.base_view import BaseView


class BaseController:

    def __init__(self, dispatcher):
        self.dp = dispatcher
        self.base_view = BaseView()

    def start_handler(self, update, context):
        return self.base_view.send_hello_message(update, context)

    def start(self):
        # Create handlers
        start_handler = CommandHandler('start', self.start_handler)
        # Add handlers
        self.dp.add_handler(start_handler)
