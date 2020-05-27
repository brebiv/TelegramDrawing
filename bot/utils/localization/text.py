from bot.utils.localization.lang.english import EnglishText
from bot.utils.localization.lang.russian import RussianText


class Text:

    def __init__(self, lang_code):
        self.language = lang_code
        if self.language == 'en':
            self.replies = EnglishText
        elif self.language == 'ru':
            self.replies = RussianText

    def get_text(self):
        if self.language == 'en':
            return EnglishText
        elif self.language == 'ru':
            return RussianText

    def create_inline_url(self, url: str, text=None) -> str:
        if text is not None:
            return f'<a href="{url}">{text}</a>'
        else:
            return f'<a href="{url}">{self.replies.default_link_text}</a>'
