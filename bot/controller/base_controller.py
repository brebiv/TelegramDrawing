from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler
from telegram.ext import run_async
from bot.view.base_view import BaseView
from queue import Queue
from threading import Thread


class BaseController:

    def __init__(self, dispatcher, queue: Queue):
        self.dp = dispatcher
        self.base_view = BaseView()
        self.q = queue

    @run_async
    def start_handler(self, update, context):
        # Here is an issue, when people can send /start very fast, it will create many threads, should fix it.
        self.base_view.send_hello_message(update, context)
        img = self.q.get()
        self.base_view.send_image(update, context, img)


    def start(self):
        # Create handlers
        start_handler = CommandHandler('start', self.start_handler)
        # Add handlers
        self.dp.add_handler(start_handler)
