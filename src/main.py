#!/usr/bin/env python3

import signal
import database
from telegram_bot import TelegramBotThred
from amazon_watch import AmazonWatch

tbot = TelegramBotThred()
watch = AmazonWatch(tbot)

def signal_handler(sig, frame):
    print("[INFO] Shutting down application...")
    watch.stop()
    watch.join()
    tbot.stop()
    tbot.join()
    while watch.is_alive() or tbot.is_alive():
        pass
    database.disconnect()
    
    exit()

def main():
    print("[INFO] Starting application...")
    database.connect()
    tbot.start()
    watch.start()
    
    while not tbot.running:
        pass
    
    signal.signal(signal.SIGINT, signal_handler)
    while True:
        pass

if __name__ == "__main__":
    main()
    