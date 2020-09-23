#!/usr/bin/env python3

import database
from telegram_bot import TelegramBotThred
from amazon_watch import AmazonWatch

tbot = TelegramBotThred()
watch = AmazonWatch(tbot)

def terminal():
    while True:
        cmd = input("> ")
        
        if cmd == "exit":
            print("[INFO] Shutting down application...")
            watch.stop()
            tbot.stop()
            while watch.is_alive() or tbot.is_alive():
                pass
            database.disconnect()
            
            exit()
        else:
            print("[ERROR] Unknown command")

def main():
    print("[INFO] Starting application...")
    database.connect()
    tbot.start()
    watch.start()
    
    while not tbot.running:
        pass
    
    terminal()

if __name__ == "__main__":
    main()
    