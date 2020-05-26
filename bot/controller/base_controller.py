from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler
from telegram.ext import run_async
from bot.view.base_view import BaseView
from queue import Queue
from threading import Thread
import uuid
from models import User
from database_connect import session
from sqlalchemy.exc import IntegrityError


class BaseController:

    def __init__(self, dispatcher, queue: Queue):
        self.dp = dispatcher
        self.base_view = BaseView()
        self.q = queue

    def start_handler(self, update, context):
        user_telegram_obj = update.message.from_user     # It's telegram user obj
        try:
            user_database_entity = User(user_telegram_obj)   # It's sqlalchemy user obj
            session.add(user_database_entity)
            session.commit()
        except IntegrityError:      # it's when user already in database
            pass
        return self.base_view.send_greeting_message(update, context)

    @run_async
    def demo_handler(self, update, context):
        # Here is an issue, when people can send /start very fast, it will create many threads, should fix it.
        context.user_data['hash'] = str(uuid.uuid4())
        self.base_view.send_drawing_link(update, context)
        img = self.q.get()
        self.base_view.send_image(update, context, img)

    def start(self):
        # Create handlers
        start_handler = CommandHandler("start", self.start_handler)
        demo_handler = CommandHandler("demo", self.demo_handler)
        # Add handlers
        self.dp.add_handler(start_handler)
        self.dp.add_handler(demo_handler)
