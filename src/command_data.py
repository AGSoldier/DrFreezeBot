import re
import validators

# Classe usata per contenere i dati del comando 'register'
class RegisterCommandData:
    
    ### Variabili
    amazon_url = ["amazon", "amzn"]
    url_regex = r"\/[A-Z0-9]{10}?"
    alias_regex = r"^[\w\d ]*$"
    
    telegram_id = None
    query = None
    step = None
    
    url = None
    alias = None
    price = None
    
    ### Costruttore
    def __init__(self, telegram_id, query):
        self.telegram_id = telegram_id
        self.query = query
        
    ### Metodi
    def set_url(self, url):
        if not validators.url(url):
            return False
        
        if not any(x in url for x in self.amazon_url):
            return False
            
        match = re.search(self.url_regex, url)
        if match == None:
            return False
            
        self.url = match.group(0)[1:]
        return True
        
    def set_alias(self, alias):
        if not re.match(self.alias_regex, alias):
            return False
            
        self.alias = alias
        return True
        
    def set_price(self, price):
        try:
            price = price.replace(",", ".")
            price = float(price)
            price = "{:2f}".format(price)
            
            self.price = price
            return True
        except:
            return False