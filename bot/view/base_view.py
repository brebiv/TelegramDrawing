from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from bot.utils.utils import build_keyboard
from bot.utils.my_emoji import Emoji
from bot.utils.localization.text import Text
from io import BytesIO
from config import WebServerConfig


class BaseView:

    def send_choose_language_message(self, chat_id, context):
        buttons = [
            InlineKeyboardButton(f"{Emoji.uk_flag} English", callback_data='lang_en'),
            InlineKeyboardButton(f"{Emoji.ru_flag} Русский", callback_data='lang_ru')
        ]
        kb = InlineKeyboardMarkup(build_keyboard(buttons, 2))
        return context.bot.send_message(chat_id, f"{Emoji.vulcan_salute} What is your language?", reply_markup=kb)

    def send_main_menu_message(self, chat_id, context):
        text = Text(context.user_data['lang_code'])
        buttons = [
            InlineKeyboardButton(f"Demo", callback_data="demo")
        ]
        kb = InlineKeyboardMarkup(build_keyboard(buttons, 1))
        return context.bot.send_message(chat_id, text.replies.main_menu_text, reply_markup=kb)

    def send_drawing_link(self, chat_id, context):
        text = Text(context.user_data['lang_code'])
        context.user_data['got_link'] = True
        url = WebServerConfig.ADDRESS + "/" + context.user_data['hash']
        context.user_data['url'] = url
        return context.bot.send_message(chat_id, text.replies.click_to_draw + text.create_inline_url(url))

    def send_you_already_have_drawing_link_message(self, chat_id, context):
        text = Text(context.user_data['lang_code'])
        url = context.user_data['url']
        return context.bot.send_message(chat_id,
                                        text.replies.you_already_have_drawing_link_text + text.create_inline_url(url))

    def send_image(self, chat_id, context, image):
        # Convert Pillow img obj into bytes
        img = BytesIO()
        img.name = "image.png"
        image.save(img, "PNG")
        img.seek(0)
        return context.bot.send_photo(chat_id, img)
