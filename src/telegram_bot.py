import os
import re
import settings
import database
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ParseMode
from telegram.ext import Updater, MessageHandler, CommandHandler, Filters, CallbackQueryHandler
from command_data import RegisterCommandData, ApprovalRequestData 

# Classe del bot Telegram, estende la classe Thread
class TelegramBotThread(Thread):

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
        
        self.updater = Updater(token = settings.TELEGRAM_TOKEN, use_context = True)
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
        
    # Aggiorna l'username dell'utente da cui proviene il messaggio
    def update_handle(self, telegram_id, telegram_handle):
        user = database.get_user(telegram_id = telegram_id)
        
        if not telegram_handle == user['telegram_handle']:
            database.update_telegram_handle(telegram_id, telegram_handle)
        
    # Notifica un utente
    def notify_user(self, user_id, product_alias, product):
        user = database.get_user_by_id(user_id)
        url = product.detail_page_url
        price = product.bestOffer.price.amount
        msg = "Hey! Il prodotto che stavi controllando *{}* è sceso a {}!".format(product_alias, price)
        
        keyboard = [[InlineKeyboardButton(text = "Acquista subito!", url = url)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        self.updater.bot.send_message(
            chat_id = user['telegram_id'], 
            text = msg, 
            parse_mode = ParseMode.MARKDOWN, 
            reply_markup = reply_markup
        )
        
    # Notifica tutti gli utenti
    def notify_broadcast(self, user_id, product_alias, product):
        users = database.get_users()
        for user in users:
            if user['id'] != user_id:
                url = product.detail_page_url
                price = product.bestOffer.price.amount
                msg = "Un amministratore ha segnalato questa offerta: *{}* a soli {}!".format(product_alias, price)
                
                keyboard = [[InlineKeyboardButton(text = "Acquista subito!", url = url)]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                try:
                    self.updater.bot.send_message(
                        chat_id = user['telegram_id'], 
                        text = msg, 
                        parse_mode = ParseMode.MARKDOWN, 
                        reply_markup = reply_markup
                    )
                except:
                    print("[ERROR] Chat not found")
            else:
                self.notify_user(user_id, product_alias, product)
        
    # Notifica gli admin che un utente vuole diventare un debugger
    def debug_access_request(self, bot, request_id):
        request = self.approval_processes[request_id]
        admins = database.get_admins()
        
        msg = "L'utente *{}* ha richiesto di usare il bot di debug.\nApprovare?".format(request.request_name)
        keyboard = [
            [
                InlineKeyboardButton(text = "Rifiuta", callback_data = "debug reject {}".format(request_id)),
                InlineKeyboardButton(text = "Approva", callback_data = "debug approve {}".format(request_id))
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        for admin in admins:
            admin_id = int(admin["telegram_id"])
            msg_sent = bot.send_message(
                chat_id = admin_id, 
                text = msg, 
                parse_mode = ParseMode.MARKDOWN, 
                reply_markup = reply_markup
            )
            
            request.approval_msgs.append(msg_sent)
        
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
        msg = "Benvenuto su *Deal Alert!* Per iniziare a controllare un prodotto Amazon usa il comando /register."
        
        exist_user = database.exist_user(telegram_id = str(user_id))
        if not exist_user:
            database.register_user(telegram_id = str(update.effective_chat.id), telegram_handle = update.effective_chat.username)
        
        user = database.get_user(telegram_id = str(update.effective_chat.id))
        self.update_handle(str(user_id), update.effective_chat.username)
        
        if self.debug:
            if not user['debugger']:
                if not user_id in self.approval_processes:
                    context.bot.send_message(chat_id = user_id, text = "È stata inviata la richiesta per poter usare questo bot agli amministratori.")
                    request_name = update.message.from_user.first_name
                    if update.message.from_user.last_name != None:
                        request_name += " {}".format(update.message.from_user.last_name)
                    self.approval_processes[user_id] = ApprovalRequestData(update.callback_query, request_name)
                    self.debug_access_request(context.bot, user_id)
                    print("[INFO] The user {} has requested to join the debug bot.".format(request_name))
                else:
                    context.bot.send_message(chat_id = user_id, text = "La tua richiesta è stata inviata agli amministratori. Attendi la loro approvazione.")
                return
        
        context.bot.send_message(chat_id = update.effective_chat.id, text = msg, parse_mode = ParseMode.MARKDOWN)
        
    # Comportamento del comando 'register'
    def register_cmd(self, update, context):
        telegram_id = update.effective_chat.id
        user = database.get_user(telegram_id = str(telegram_id))
        self.update_handle(str(telegram_id), update.effective_chat.username)
        
        if self.debug and (not database.exist_user(telegram_id = user['telegram_id']) or (user != None and not database.is_user_debugger(user['id']))):
            context.bot.send_message(chat_id = telegram_id, text = "Non hai i permessi necessari per usare questo bot.")
            return
        
        if not database.exist_user(telegram_id = str(telegram_id)):
            context.bot.send_message(chat_id = telegram_id, text = "Ops! Sembra che tu non sia registrato. Usa il comando /start per registrarti.")
            return
        
        if telegram_id in self.registration_processes:
            context.bot.send_message(chat_id = telegram_id, text = "Stai già registrando un prodotto!")
            return
            
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
        if user['role'] == 2:
            msg += "\n(Aggiungi 'all' dopo il comando per registrare il prodotto globalmente)"
        
        context.bot.send_message(
                chat_id = telegram_id, 
                text = msg, 
                parse_mode = ParseMode.MARKDOWN, 
                reply_markup = reply_markup
            )
            
        self.registration_processes[telegram_id] = RegisterCommandData(
            telegram_id, 
            update.callback_query
        )
        self.registration_processes[telegram_id].broadcast = len(context.args) > 0 and context.args[0] == "all"
        
    # Comportamento del comando 'list'
    def list_cmd(self, update, context):
        telegram_id = update.effective_chat.id
        user = database.get_user(telegram_id = str(telegram_id))
        self.update_handle(str(telegram_id), update.effective_chat.username)
        
        if self.debug and (not database.exist_user(telegram_id = user['telegram_id']) or (user != None and not database.is_user_debugger(user['id']))):
            context.bot.send_message(chat_id = telegram_id, text = "Non hai i permessi necessari per usare questo bot.")
            return
        
        if not database.exist_user(telegram_id = user['telegram_id']):
            context.bot.send_message(chat_id = telegram_id, text = "Ops! Sembra che tu non sia registrato. Usa il comando /start per registrarti.")
            return
        
        telegram_id = update.effective_chat.id
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
                text = msg.format(watch['product_alias'], watch['price_threshold'], product.bestOffer.price.amount), 
                parse_mode = ParseMode.MARKDOWN, 
                reply_markup = reply_markup
            )
            
    # Comportamento del comando 'help'
    def help_cmd(self, update, context):
        user_id = update.effective_chat.id
        user = database.get_user(telegram_id = str(user_id))
        self.update_handle(str(user_id), update.effective_chat.username)
        
        msg = "*Deal Alert!*\n\nDeal Alert! ti consente di tenere sott'occhio i prodotti Amazon che ti interessano.\n\nTi basterà usare il comando /register e seguire le indicazioni.\nInvia qualsiasi link Amazon al bot, imposta un prezzo massimo a cui vorresti acquistarlo ed il bot ti avviserà appena il prodotto scenderà al prezzo da te indicato!\n\nCon il comando /list puoi controllare i prodotti da te registrati ed eventualmente eliminarli!\n\nBuono shopping!"
        if self.debug and (not database.exist_user(telegram_id = str(user_id)) or (user != None and not database.is_user_debugger(user['id']))):
            msg = "Non hai i permessi necessari per usare questo bot."
        
        context.bot.send_message(
                chat_id = update.effective_chat.id, 
                text = msg, 
                parse_mode = ParseMode.MARKDOWN
            )
            
    # Handler per i messaggi normali
    def messages_handler(self, update, context):
        user_id = update.message.chat.id
        self.update_handle(str(user_id), update.effective_chat.username)
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
        self.update_handle(str(user_id), update.effective_chat.username)
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
                database.add_watch(user['id'], product_id, product_name, curr_process.price, broadcast = curr_process.broadcast)
        
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
                text = "Non stai più controllando il prodotto *{}*.".format(watch['product_alias']),
                parse_mode = ParseMode.MARKDOWN
            )
        elif args[0] == "debug":
            request_id = int(args[2])
            
            if request_id in self.approval_processes:
                request_user = database.get_user(telegram_id = str(request_id))
                process = self.approval_processes[request_id]
            
                if args[1] == "approve":
                    context.bot.send_message(chat_id = request_id, text = "Complimenti! Ora hai accesso al bot di debug.")
                    
                    for msg in process.approval_msgs:
                        if user_id == msg.chat.id:
                            msg.edit_text("L'utente {} è stato accettato".format(process.request_name))
                        else:
                            msg.edit_text("L'utente {} ha accettato la richiesta di {}".format(query.from_user.first_name, process.request_name))
                        
                    database.set_debugger(request_user['id'])
                    print("[INFO] The user {} has been accepted by {}.".format(process.request_name, query.from_user.first_name))
                elif args[1] == "reject":
                    context.bot.send_message(chat_id = request_id, text = "Sei stato rifiutato per accedere al bot di debug.")
                    
                    for msg in process.approval_msgs:
                        if user_id == msg.chat.id:
                            msg.edit_text("L'utente {} è stato rifiutato".format(process.request_name))
                        else:
                            msg.edit_text("L'utente {} ha rifiutato la richiesta di {}".format(query.from_user.first_name, process.request_name))
                        
                    database.remove_user(request_user['id'])
                    print("[INFO] The user {} has been rejected by {}.".format(process.request_name, query.from_user.first_name))
                    
                del self.approval_processes[request_id]
                            
            else:
                context.bot.send_message(chat_id = user_id, text = "Questo utente è stato già gestito.")
    