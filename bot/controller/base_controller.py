from telegram.ext import MessageHandler, CommandHandler, CallbackQueryHandler
from telegram.ext import run_async
from bot.view.base_view import BaseView
from queue import Queue
from threading import Thread
from models import User
from database_connect import session
from sqlalchemy.orm.exc import NoResultFound
import uuid
import re


class BaseController:

    def __init__(self, dispatcher, queue: Queue):
        self.dp = dispatcher
        self.base_view = BaseView()
        self.q = queue

    def start_handler(self, update, context):
        user_telegram_obj = update.message.from_user     # It's telegram user obj
        try:
            user = session.query(User).filter(User.tid == user_telegram_obj.id).one()
        except NoResultFound:
            user_database_entity = User(user_telegram_obj)   # Add user to database
            session.add(user_database_entity)
            session.commit()
        return self.base_view.send_choose_language_message(update, context)

    @run_async
    def demo_handler(self, update, context):
        try:
            if context.user_data['got_link'] is not True:
                self.demo_drawing(update, context)
            else:
                self.base_view.send_you_already_have_drawing_link_message(update, context)
        except KeyError:    # When there is no 'got_link' in context
            self.demo_drawing(update, context)

    def callback_query_handler(self, update, context):
        callback = update.callback_query

        if callback.data.startswith("lang_"):
            lang_code = re.search('lang_([a-z]{2})', callback.data).group(1)    # return two chars after _
            user = session.query(User).filter(User.tid == callback.from_user.id).one()
            user.lang_code = lang_code
            session.commit()
            context.user_data['lang_code'] = lang_code
            context.bot.delete_message(callback.from_user.id, callback.message.message_id)
            return self.base_view.send_greeting_message(callback.from_user.id, context)

    def demo_drawing(self, update, context):
        context.user_data['hash'] = str(uuid.uuid4())
        self.base_view.send_drawing_link(update, context)
        img = self.q.get()
        self.base_view.send_image(update, context, img)
        context.user_data['got_link'] = False

    def start(self):
        # Create handlers
        start_handler = CommandHandler("start", self.start_handler)
        demo_handler = CommandHandler("demo", self.demo_handler)
        callback_query_handler = CallbackQueryHandler(self.callback_query_handler)
        # Add handlers
        self.dp.add_handler(start_handler)
        self.dp.add_handler(demo_handler)
        self.dp.add_handler(callback_query_handler)
