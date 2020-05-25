from io import BytesIO


class BaseView:

    def send_hello_message(self, update, context):
        return update.message.reply_text("Hey hi")

    def send_image(self, update, context, image):
        # Convert Pillow img obj into bytes
        img = BytesIO()
        img.name = "image.png"
        image.save(img, "PNG")
        img.seek(0)
        return context.bot.send_photo(update.message.chat_id, img)
