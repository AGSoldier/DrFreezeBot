import time
import database
from threading import Thread
from settings import AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG, REFRESH_TIMEOUT
from amazon.paapi import AmazonAPI
from urllib.error import HTTPError

# Thread che si occupa di controllare i link Amazon salvati dagli utenti
class AmazonWatch(Thread):
    
    ### Costruttore
    def __init__(self, tbot):
        Thread.__init__(self)
        self.running = False
        self.timer = REFRESH_TIMEOUT
        
        self.amazon = AmazonAPI(AMAZON_ACCESS_KEY, AMAZON_SECRET_KEY, AMAZON_ASSOC_TAG, "IT")
        self.tbot = tbot
        self.tbot.product_data_service = self.get_product_info
        
    ### Metodi
    # Loop principale 
    def run(self):
        self.running = True
        while self.running:
            time.sleep(1)
            self.timer -= 1
            if self.timer == 0:
                self.check_products()
                self.timer = REFRESH_TIMEOUT
            
    # Ferma i controlli dei prezzi
    def stop(self):
        self.running = False
    
    # Controlla i watch ed eventualmente avvisa i client
    def check_products(self):
        watches = database.get_watches()
        for watch in watches:
            product_id = watch['product_id']
            search = self.amazon.get_items(item_ids = [product_id], async_req = True)
            product = search['data'][product_id]
            price = product.bestOffer.price.amount
            if (not watch['last_checked_price'] == None) and price >= float(watch['last_checked_price']):
                continue
            
            if price <= float(watch['price_threshold']):
                database.update_last_checked_price(watch['id'], price)
                self.tbot.notify_user(watch['user_id'], product)
                
    # Ottiene le informazioni di un prodotto
    def get_product_info(self, product_id):
        search = self.amazon.get_items(item_ids = [product_id], async_req = True)
        return search['data'][product_id]