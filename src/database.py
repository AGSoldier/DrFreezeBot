import psycopg2
import settings
from psycopg2.extras import DictCursor

# Connessione al database
conn = None

# Avvia la connessione al database
def connect():
    print("[INFO] Connecting to database...")
    global conn
    conn = psycopg2.connect(dbname = settings.DB_NAME, user = settings.DB_USER, password = settings.DB_PASS, host = settings.DB_HOST, port = settings.DB_PORT)
    print("[OK] Successfully connected to database!")
    
# Termina la connessione al database
def disconnect():
    print("[INFO] Disconnecting from database...")
    conn.close()
    print("[OK] Successfully disconnected from database!")
    
# Controlla se un utente esiste
def exist_user(telegram_id = "", discord_id = "__none__"):
    result = None
    
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM users 
            WHERE telegram_id = %s OR discord_id = %s
            """, (telegram_id, discord_id))
        result = cur.fetchone()
        conn.commit()
        
    return result != None

# Registra un utente
def register_user(telegram_id = None, telegram_handle = None, discord_id = None, discord_handle = None):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO users(telegram_id, telegram_handle, discord_id, discord_handle)
        VALUES(%s, %s, %s, %s);
        """, (telegram_id, telegram_handle, discord_id, discord_handle))
        conn.commit()

# Ritorna un utente
def get_user(telegram_id = "", discord_id = ""):
    with conn.cursor(cursor_factory = DictCursor) as cur:
        cur.execute("""
        SELECT * FROM users
        WHERE telegram_id = %s OR discord_id = %s;
        """, (telegram_id, discord_id))
        
        return cur.fetchone()
        
# Ritorna tutti gli utenti
def get_users():
    with conn.cursor(cursor_factory = DictCursor) as cur:
        cur.execute("""
        SELECT * FROM users;
        """)
        
        return cur.fetchall()
        
# Ritorna un utente specificato il suo ID
def get_user_by_id(id):
    with conn.cursor(cursor_factory = DictCursor) as cur:
        cur.execute("""
        SELECT * FROM users
        WHERE id = %s;
        """, (id,))
        
        return cur.fetchone()
        
# Controlla se l'utente ha i permessi di debug
def is_user_debugger(user_id):
    try:
        result = None
        
        with conn.cursor(cursor_factory = DictCursor) as cur:
            cur.execute("""
            SELECT debugger FROM users
            WHERE id = %s;
            """, (user_id,))
            
            result = cur.fetchone()
            
        return result["debugger"]
    except:
        return False
    
# Ritorna gli utenti con ruolo di admin    
def get_admins():
    with conn.cursor(cursor_factory = DictCursor) as cur:
        cur.execute("""
        SELECT * FROM users
        WHERE role = %s;
        """, (2,))
        
        return cur.fetchall()
        
# Rende un utente un debugger
def set_debugger(user_id):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE users
        SET debugger = true
        WHERE id = %s;
        """, (user_id,))
        
        conn.commit()
        
# Aggiorna l'username di Telegram
def update_telegram_handle(telegram_id, telegram_handle):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE users
        SET telegram_handle = %s
        WHERE telegram_id = %s;
        """, (telegram_handle, telegram_id))
        
        conn.commit()
        
# Rimuove un utente
def remove_user(user_id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM users
        WHERE id = %s;
        """, (user_id,))
        
        conn.commit()
    
        
# Aggiunge un watch per un utente
def add_watch(user_id, product_id, product_alias, price_threshold, broadcast = False):
    with conn.cursor() as cur:
        cur.execute("""
        INSERT INTO product_watches(user_id, product_id, product_alias, price_threshold, broadcast)
        VALUES(%s, %s, %s, %s, %s)
        RETURNING id;
        """, (user_id, product_id, product_alias, price_threshold, broadcast))
        conn.commit()
        
        return cur.fetchone()[0]

# Ritorna uno specifico watch
def get_watch(watch_id):
    with conn.cursor(cursor_factory = DictCursor) as cur:
        cur.execute("""
        SELECT * FROM product_watches
        WHERE id = %s;
        """, (watch_id,))
        
        return cur.fetchone()

# Ritorna la lista di watch
def get_watches():
    result = []
    
    with conn.cursor(cursor_factory = DictCursor) as cur:
        cur.execute("""
            SELECT * FROM product_watches;
        """)
        result = cur.fetchall()
        
    return result
    
# Ritorna la lista degli watch di un utente
def get_user_watches(user_id):
    with conn.cursor(cursor_factory = DictCursor) as cur:
        cur.execute("""
        SELECT * FROM product_watches
        WHERE user_id = %s;
        """, (user_id,))
        
        return cur.fetchall()

# Aggiorna l'ultimo prezzo controllato
def update_last_checked_price(watch_id, price):
    with conn.cursor() as cur:
        cur.execute("""
        UPDATE product_watches
        SET last_checked_price = %s
        WHERE id = %s;
        """, (price, watch_id))
        conn.commit()
        
# Cancella un watch
def delete_watch(watch_id):
    with conn.cursor() as cur:
        cur.execute("""
        DELETE FROM product_watches
        WHERE id = %s;
        """, (watch_id,))
        conn.commit()
