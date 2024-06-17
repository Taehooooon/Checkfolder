import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from telegram import Bot

# 텔레그램 봇 설정
TELEGRAM_BOT_TOKEN = "7128502921:AAGUdpae9NDqAhQcNTx--pbm9egzOJzhnkE"
CHAT_ID = "7471860459"

bot = Bot(token=TELEGRAM_BOT_TOKEN)

# 공유 폴더 경로
# folder_to_watch = r'\\172.20.100.213\fax'
folder_to_watch = r'/Users/th/Desktop/WORKSPACE/checkfolder_sk/1'

class Watcher:
    def __init__(self, directory_to_watch):
        self.observer = Observer()
        self.directory_to_watch = directory_to_watch

    def run(self):
        event_handler = Handler()
        self.observer.schedule(event_handler, self.directory_to_watch, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

class Handler(FileSystemEventHandler):
    @staticmethod
    def on_created(event):
        if not event.is_directory:
            message = f"새 파일이 생성되었습니다: {event.src_path}"
            logging.info(message)
            bot.send_message(chat_id=CHAT_ID, text=message)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    w = Watcher(folder_to_watch)
    w.run()
