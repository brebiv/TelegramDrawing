from bot.utils.localization.lang.english import EnglishText
from bot.utils.localization.lang.russian import RussianText


class Text:

    def __init__(self, lang_code):
        self.language = lang_code

    def get_text(self):
        if self.language == 'en':
            return EnglishText
        elif self.language == 'ru':
            return RussianText
