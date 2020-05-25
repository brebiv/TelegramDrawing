from server.app import ServerWrapper
from bot.controller.base_controller import BaseController
from telegram.ext import Updater
from config import BotConfig
from telegram.ext import Defaults
from threading import Thread
from queue import Queue


# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

if __name__ == '__main__':
    # Main thread here
    # Queue to communicate with server and bot threads
    q = Queue()
    # Server here
    server_wrapper = ServerWrapper(q)
    sThread = Thread(target=server_wrapper.run, args=(), name="Server Thread")
    sThread.start()
    # Bot here
    defaults = Defaults(parse_mode="HTML")
    updater = Updater(BotConfig.API_TOKEN, use_context=True, defaults=defaults)
    dispatcher = updater.dispatcher
    base_controller = BaseController(dispatcher, q)
    base_controller.start()
    bThread = Thread(target=updater.start_polling, args=(), name="Bot Thread")
    bThread.start()
