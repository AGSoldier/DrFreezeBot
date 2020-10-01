import os
import re
import settings
import database
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackQueryHandler
from command_data import RegisterCommandData, ApprovalRequestData

# Classe del bot Telegram, estende la classe Thread
class TelegramBotThred(Thread):

    ### Variabili
    registration_processes = {}
    approval_processes = {}

    ### Callbacks
    product_data_service = None

    ### Costruttore
    def __init__(self, debug):
        Thread.__init__(self)
        self.running = False
        self.debug = debug
        
        token = self.debug if setting.TELEGRAM_DBG_TOKEN else settings.TELEGRAM_TOKEN
        self.updater = Updater(token = token, use_context = True)
        self.dispatcher = self.updater.dispatcher
        
        self.cmds_setup()
    
    ### Metodi
    # Loop principale del bot
    def run(self):
        self.updater.start_polling()
        while not self.updater.running:
            pass
        print("[OK] Telegram bot started")
        
        self.running = True
        while self.running:
            pass
        
        self.updater.stop()
        print("[OK] Telegram bot closed")
        
    # Ferma l'esecuzione del bot
    def stop(self):
        self.running = False
        
    # Notifica un utente
    def notify_user(self, user_id, product):
        user = database.get_user_by_id(user_id)
        product_name = product.item_info.title.display_value
        url = product.detail_page_url
        price = product.bestOffer.price.amount
        msg = "Hey! Il prodotto che stavi controllando *{}* è sceso a {}!".format(product_name, price)
        
        keyboard = [[InlineKeyboardButton(text = "Acquista subito!", url = url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        self.updater.bot.send_message(
            chat_id = user['telegram_id'], 
            text = msg, 
            parse_mode = ParseMode.MARKDOWN, 
            reply_markup = reply_markup
        )
        
    # Setup per i vari comandi del bot
    def cmds_setup(self):
        # /start
        start_handler = CommandHandler("start", self.start_cmd)
        self.dispatcher.add_handler(start_handler)
        
        # /register
        register_handler = CommandHandler("register", self.register_cmd)
        self.dispatcher.add_handler(register_handler)
        
        # /list
        list_handler = CommandHandler("list", self.list_cmd)
        self.dispatcher.add_handler(list_handler)
        
        # /help
        help_handler = CommandHandler("help", self.help_cmd)
        self.dispatcher.add_handler(help_handler)
        
        # Messaggi normali
        messages_handler = MessageHandler(Filters.text & (~Filters.command), self.messages_handler)
        self.dispatcher.add_handler(messages_handler)
        
        # Bottoni
        button_handler = CallbackQueryHandler(self.button_handler)
        self.dispatcher.add_handler(button_handler)
    
    # Comportamento del comando 'start'
    def start_cmd(self, update, context):
        user_id = update.effective_chat.id
        exist_user = database.exist_user(telegram_id = str(user_id))
        
        if self.debug and exist_user:
            user = database.get_user(telegram_id = str(update.effective_chat.id))
            if not user['debugger']:
                if not user_id in self.approval_processes:
                    context.bot.send_message(chat_id = update.effective_chat.id, text = "È stata inviata la richiesta per poter usare questo bot agli amministratori.")
                    self.approval_processes[user_id] = ApprovalRequestData(update.callback_query, user_id, "{} {}".format(update.from_user.first_name, update.from_user.last_name)
                    return
                
                return
        
        msg = "Benvenuto su *Deal Alert!* Per iniziare a controllare un prodotto Amazon usa il comando /register."
        if not exist_user:
            database.register_user(telegram_id = str(update.effective_chat.id), telegram_handle = str(update.effective_chat.username))
            
        context.bot.send_message(chat_id = update.effective_chat.id, text = msg, parse_mode = ParseMode.MARKDOWN)
        
    # Comportamento del comando 'register'
    def register_cmd(self, update, context):
        telegram_id = update.effective_chat.id
        if not database.exist_user(telegram_id = str(telegram_id)):
            context.bot.send_message(chat_id = telegram_id, text = "Ops! Sembra che tu non sia registrato. Usa il comando /start per registrarti.")
            return
        
        if telegram_id in self.registration_processes:
            context.bot.send_message(chat_id = telegram_id, text = "Stai già registrando un prodotto!")
            return
            
        self.registration_processes[telegram_id] = RegisterCommandData(
            telegram_id, 
            update.callback_query
        )
        
        keyboard = [
            [
                InlineKeyboardButton(text = "Prodotto", callback_data = "register url"),
                InlineKeyboardButton(text = "Nome (opzionale)", callback_data = "register alias"),
                InlineKeyboardButton(text = "Prezzo", callback_data = "register price")
            ],
            [
                InlineKeyboardButton(text = "Annulla", callback_data = "register cancel"),
                InlineKeyboardButton(text = "Registra", callback_data = "register ok")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        msg = "*Registra prodotto*\n\nIniziamo! Dimmi quale prodotto vuoi controllare ed a che prezzo."
        context.bot.send_message(
                chat_id = telegram_id, 
                text = msg, 
                parse_mode = ParseMode.MARKDOWN, 
                reply_markup = reply_markup
            )
        
    # Comportamento del comando 'list'
    def list_cmd(self, update, context):
        telegram_id = update.effective_chat.id
        if not database.exist_user(telegram_id = str(telegram_id)):
            context.bot.send_message(chat_id = telegram_id, text = "Ops! Sembra che tu non sia registrato. Usa il comando /start per registrarti.")
            return
        
        telegram_id = update.effective_chat.id
        user = database.get_user(telegram_id = str(telegram_id))
        watches = database.get_user_watches(user['id'])
        if len(watches) == 0:
            context.bot.send_message(chat_id = telegram_id, text = "Non hai prodotti registrati.\nUsa il comando /register per registrarne uno.")
            return
        
        msg = "Prodotto: *{}*\nSoglia: {}\nPrezzo: {}"
        for watch in watches:
            product = self.product_data_service(watch['product_id'])
            keyboard = [[InlineKeyboardButton(text = "Elimina", callback_data = "delete {}".format(watch['id']))]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            context.bot.send_message(
                chat_id = telegram_id, 
                text = msg.format(product.item_info.title.display_value, watch['price_threshold'], product.bestOffer.price.amount), 
                parse_mode = ParseMode.MARKDOWN, 
                reply_markup = reply_markup
            )
            
    # Comportamento del comando 'help'
    def help_cmd(self, update, context):
        msg = "*Deal Alert!*\n\nDeal Alert! ti consente di tenere sott'occhio i prodotti Amazon che ti interessano.\n\nTi basterà usare il comando /register e seguire le indicazioni.\nInvia qualsiasi link Amazon al bot, imposta un prezzo massimo a cui vorresti acquistarlo ed il bot ti avviserà appena il prodotto scenderà al prezzo da te indicato!\n\nCon il comando /list puoi controllare i prodotti da te registrati ed eventualmente eliminarli!\n\nBuono shopping!"
        
        context.bot.send_message(
                chat_id = update.effective_chat.id, 
                text = msg, 
                parse_mode = ParseMode.MARKDOWN
            )
            
    # Handler per i messaggi normali
    def messages_handler(self, update, context):
        user_id = update.message.chat.id
        user_msg = update.message.text
        
        if user_id in self.registration_processes:
            process = self.registration_processes[user_id]
            success = False
            msg = None
            
            if process.step == "url":
                success = process.set_url(user_msg)
                msg = "Il link che hai inviato non è corretto."
            elif process.step == "alias":
                success = process.set_alias(user_msg)
                msg = "Nome non valido: usa solo lettere e numeri."
            elif process.step == "price":
                success = process.set_price(user_msg)
                msg = "Il formato del prezzo inviato non è corretto."
                
            if not success:
                context.bot.send_message(chat_id = user_id, text = msg)
            else:
                options = []
                if process.url == None:
                    options.append(InlineKeyboardButton(text = "Prodotto", callback_data = "register url"))
                    
                if process.alias == None:
                    options.append(InlineKeyboardButton(text = "Nome (opzionale)", callback_data = "register alias"))
                    
                if process.price == None:
                    options.append(InlineKeyboardButton(text = "Prezzo", callback_data = "register price"))
                
                keyboard = [
                    options,
                    [
                        InlineKeyboardButton(text = "Annulla", callback_data = "register cancel"),
                        InlineKeyboardButton(text = "Registra", callback_data = "register ok")
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                process.query.edit_message_reply_markup(reply_markup)
            
    # Handler per i bottoni
    def button_handler(self, update, context):
        query = update.callback_query
        user_id = query.from_user.id
        args = query.data.split()

        if args[0] == "register":
            msg = query.message
            if not user_id in self.registration_processes:
                return
            curr_process = self.registration_processes[user_id]
            curr_process.query = query
            curr_process.step = args[1]
                
            options = []
            if curr_process.url == None:
                options.append(InlineKeyboardButton(text = "Prodotto", callback_data = "register url"))
                
            if curr_process.alias == None:
                options.append(InlineKeyboardButton(text = "Nome (opzionale)", callback_data = "register alias"))
                
            if curr_process.price == None:
                options.append(InlineKeyboardButton(text = "Prezzo", callback_data = "register price"))
            
            keyboard = [
                options,
                [
                    InlineKeyboardButton(text = "Annulla", callback_data = "register cancel"),
                    InlineKeyboardButton(text = "Registra", callback_data = "register ok")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            if args[1] == "url":
                context.bot.send_message(chat_id = user_id, text = "Invia il link del prodotto.")
                pass
            elif args[1] == "alias":
                context.bot.send_message(chat_id = user_id, text = "Scegli un nome per il prodotto.")
                pass
            elif args[1] == "price":
                context.bot.send_message(chat_id = user_id, text = "A quale prezzo lo vorresti acquistare?")
                pass
            elif args[1] == "ok":
                msg = "*ATTENZIONE!*\nMancano dei valori:\n"
                error = False
                if curr_process.url == None:
                    msg += "- Prodotto\n"
                    error = True
                    
                if curr_process.price == None:
                    msg += "- Prezzo"
                    error = True
                    
                if error:
                    context.bot.send_message(chat_id = user_id, text = msg, parse_mode = ParseMode.MARKDOWN)
                    return
                
                product_id = curr_process.url
                product = self.product_data_service(product_id)
                
                product_name = product.item_info.title.display_value
                if curr_process.alias != None:
                    product_name = curr_process.alias
                
                user = database.get_user(telegram_id = str(user_id))
                database.add_watch(user['id'], product_id, product_name, curr_process.price)
        
                msg = "Hai registrato il prodotto *{}*!\nTi avviseremo quando raggiungerà il prezzo da te indicato.".format(product_name)
                context.bot.send_message(chat_id = user_id, text = msg, parse_mode = ParseMode.MARKDOWN)
                del self.registration_processes[user_id]
            elif args[1] == "cancel":
                del self.registration_processes[user_id]
                context.bot.send_message(chat_id = user_id, text = "Registrazione prodotto annullata.")
        elif args[0] == "delete":
            watch = database.get_watch(int(args[1]))
            database.delete_watch(watch['id'])
            product = self.product_data_service(watch['product_id'])
            
            database.delete_watch(watch['id'])
            context.bot.send_message(
                chat_id = user_id, 
                text = "Non stai più controllando il prodotto *{}*.".format(product.item_info.title.display_value),
                parse_mode = ParseMode.MARKDOWN
            )
        