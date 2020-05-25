

class BaseView:

    def send_hello_message(self, update, context):
        return update.message.reply_text("Hey hi")