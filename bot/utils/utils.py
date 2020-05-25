from emoji import EMOJI_UNICODE


def build_keyboard(buttons, cols, header_buttons=None, footer_buttons=None):
    """Return keyboard for InlineKeyboardMarkup"""
    menu = [buttons[i:i + cols] for i in range(0, len(buttons), cols)]

    if header_buttons:
        menu.insert(0, [header_buttons])
    if footer_buttons:
        menu.append([footer_buttons])

    return menu


def has_emoji(text: str) -> bool:
    """Check if text contains emoji"""
    for ch in text:
        if ch in EMOJI_UNICODE:
            return True
    return False


def is_emoji(text: str) -> bool:
    """Checks if string is emoji"""
    if text in EMOJI_UNICODE.values():
        return True
    else:
        return False
