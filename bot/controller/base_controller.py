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
            lang_code = context.user_data['lang_code']
        except NoResultFound:   # if user doest exist in database
            user_database_entity = User(user_telegram_obj)   # Add user to database
            session.add(user_database_entity)
            session.commit()
            return self.base_view.send_choose_language_message(update.message.chat_id, context)
        except KeyError:        # if context doesnt have lang_code
            return self.base_view.send_choose_language_message(update.message.chat_id, context)
        else:
            self.base_view.send_main_menu_message(update.message.chat_id, context)

    def language_handler(self, update, context):
        return self.base_view.send_choose_language_message(update.message.chat_id, context)

    def callback_query_handler(self, update, context):
        callback = update.callback_query

        if callback.data.startswith("lang_"):
            lang_code = re.search('lang_([a-z]{2})', callback.data).group(1)    # return two chars after _
            user = session.query(User).filter(User.tid == callback.from_user.id).one()
            user.lang_code = lang_code
            session.commit()
            context.user_data['lang_code'] = lang_code
            context.bot.delete_message(callback.from_user.id, callback.message.message_id)
            return self.base_view.send_main_menu_message(callback.from_user.id, context)
        elif callback.data == "demo":
            try:
                if context.user_data['got_link'] is not True:
                    self.demo_drawing(callback.from_user.id, context)
                else:
                    self.base_view.send_you_already_have_drawing_link_message(callback.from_user.id, context)
            except KeyError:  # When there is no 'got_link' in context
                self.demo_drawing(callback.from_user.id, context)

    @run_async
    def demo_drawing(self, chat_id, context):
        context.user_data['hash'] = str(uuid.uuid4())
        self.base_view.send_drawing_link(chat_id, context)
        img = self.q.get()
        self.base_view.send_image(chat_id, context, img)
        context.user_data['got_link'] = False

    def start(self):
        # Create handlers
        start_handler = CommandHandler("start", self.start_handler)
        language_handler = CommandHandler("lang", self.language_handler)
        callback_query_handler = CallbackQueryHandler(self.callback_query_handler)
        # Add handlers
        self.dp.add_handler(start_handler)
        self.dp.add_handler(language_handler)
        self.dp.add_handler(callback_query_handler)
