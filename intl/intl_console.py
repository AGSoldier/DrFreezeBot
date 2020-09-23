#!/usr/bin/env python3

import os
import psycopg2
from psycopg2.errors import StringDataRightTruncation, UniqueViolation

# -----------------------------------------------------------------------------
#     DATABASE
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
#  VARIABLES
# -----------------------------------------------------------------------------

DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

conn = None
curr_lang = "en_EN"

# -----------------------------------------------------------------------------






# -----------------------------------------------------------------------------
#  DATABASE
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Opens the database connection
# -----------------------------------------------------------------------------
def open_connection():
    print("[INFO] Connecting to database...")
    global conn
    conn = psycopg2.connect(dbname = DB_NAME, user = DB_USER, password = DB_PASS, host = DB_HOST, port = DB_PORT)
    print("[OK] Successfully connected to database!")
    
# -----------------------------------------------------------------------------
# Closes the database connection
# -----------------------------------------------------------------------------
def close_connection():
    print("[INFO] Disconnecting from database...")
    conn.close()
    print("[OK] Successfully disconnected from database!")
    
# -----------------------------------------------------------------------------
    
    
    
    
    
    
# -----------------------------------------------------------------------------
#  LANGUAGES 
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Adds a language
#
# - code:
#       Code of the language
# - name:
#       Name of the language
# -----------------------------------------------------------------------------
def add_language(code, name):
    with conn.cursor() as cur:
        try:
            cur.execute("""
                INSERT INTO languages(code, name)
                VALUES(%s, %s);
            """, (code, name))
        except StringDataRightTruncation:
            print("[ERROR] Malformed language code: {}".format(code))
            conn.rollback()
        except UniqueViolation:
            print("[ERROR] The code '{}' is already present in the database".format(code))
            conn.rollback()
        else:
            conn.commit()
            
# -----------------------------------------------------------------------------
# Checks if a language exists
#
# - code:
#       Code of the language
#
# return:
#       True if the language exists
# -----------------------------------------------------------------------------
def exist_lang(code):
    result = None
    
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM languages
            WHERE label = %s;
        """, (code,))
        result = cur.fetchall()
        
    return len(result) > 0
    
# -----------------------------------------------------------------------------
# Returns the ID of the language with the specified code
#
# - code:
#       Code of the language
#
# return:
#       
# -----------------------------------------------------------------------------
def get_lang_id(code):
    result = None
    
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM languages
            WHERE code = %s;
        """, (code,))
        result = cur.fetchone()
        
    if result:
        return result[0]
    else:
        return -1

# -----------------------------------------------------------------------------
# Removes a language from the database
#
# - lang_id:
#       ID of the language
# -----------------------------------------------------------------------------
def remove_lang(lang_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM intl_txt
            WHERE lang_id = %s;
            
            DELETE FROM languages
            WHERE id = %s;
        """, (lang_id, lang_id))
        conn.commit()

# -----------------------------------------------------------------------------
# Lists all the languages in the database
# -----------------------------------------------------------------------------
def list_languages():
    result = None
    
    with conn.cursor() as cur:
        cur.execute("SELECT name, code FROM languages;")
        result = cur.fetchall()
        
    return result

# -----------------------------------------------------------------------------






# -----------------------------------------------------------------------------
# LABELS
# -----------------------------------------------------------------------------
            
def add_label(label):
    with conn.cursor() as cur:
        try:
            cur.execute("""
                INSERT INTO labels(label)
                VALUES(%s);
            """, (label,))
        except UniqueViolation:
            print("[ERROR] The label '{}' is already present in the database".format(label))
            conn.rollback()
        else:
            conn.commit()

def exist_label(label):
    result = None
    
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM labels
            WHERE label = %s;
        """, (label,))
        result = cur.fetchall()
        
    return len(result) > 0
    
def get_label_id(label):
    result = None
    
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM labels
            WHERE label = %s;
        """, (label,))
        result = cur.fetchone()
        
    if result:
        return result[0]
    else:
        return -1
        
        
def remove_label(label_id):
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM intl_txt
            WHERE label_id = %s;
            
            DELETE FROM labels
            WHERE id = %s;
        """, (label_id, label_id))
        conn.commit()
# -----------------------------------------------------------------------------






# -----------------------------------------------------------------------------
#  TEXTS
# -----------------------------------------------------------------------------

def add_text(label, text):
    lang_id = get_lang_id(curr_lang)
    label_id = get_label_id(label)
    
    with conn.cursor() as cur:
        try:
            cur.execute("""
                INSERT INTO intl_txt(lang_id, label_id, txt)
                VALUES(%s, %s, %s);
            """, (lang_id, label_id, text))
        except UniqueViolation:
            print("[ERROR] The selected language already has the text for the label {}".format(label))
            conn.rollback()
        else:
            conn.commit()
        
def get_text(label):
    lang_id = get_lang_id(curr_lang)
    label_id = get_label_id(label)
    
    result = None
    
    with conn.cursor() as cur:
        cur.execute("""
            SELECT txt FROM intl_txt
            WHERE lang_id = %s AND label_id = %s
        """, (lang_id, label_id))
        result = cur.fetchone()
        
    return result[0]
    
# -----------------------------------------------------------------------------
# Edit an exsisting text
#
# - label:
#       Label of the text
# - text:
#       New text
# -----------------------------------------------------------------------------
def edit_text(label, text):
    lang_id = get_lang_id(curr_lang)
    label_id = get_label_id(label)
    
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE intl_txt
            SET txt = %s
            WHERE lang_id = %s AND label_id = %s;
        """, (text, lang_id, label_id))
        conn.commit()
        
# -----------------------------------------------------------------------------
# Removes a text from the database given its label
#
# - label:
#       Label of the text
# -----------------------------------------------------------------------------
def remove_text(label):
    lang_id = get_lang_id(curr_lang)
    label_id = get_label_id(label)
    
    with conn.cursor() as cur:
        cur.execute("""
            DELETE FROM intl_txt
            WHERE lang_id = %s AND label_id = %s;
        """, (lang_id, label_id))
        conn.commit()
# -----------------------------------------------------------------------------
    





# -----------------------------------------------------------------------------
#     PROGRAM
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
#  VARIABLES
# -----------------------------------------------------------------------------

running = True

# -----------------------------------------------------------------------------






# -----------------------------------------------------------------------------
# Sets current language command
#
# - lang:
#       Code of the language
# -----------------------------------------------------------------------------
def set_lang_cmd(lang):
    global curr_lang
    curr_lang = lang
    
# -----------------------------------------------------------------------------
# Add language command
#
# - params:
#       List of [id, name] of the language to add
# -----------------------------------------------------------------------------
def add_lang_cmd(params):
    add_language(params[0], params[1])
    
# -----------------------------------------------------------------------------
# Removes language command
#
# - code:
#       Code of the language to remove
# -----------------------------------------------------------------------------
def remove_lang_cmd(code):
    lang_id = get_lang_id(code)
    remove_lang(lang_id)
    
# -----------------------------------------------------------------------------
# Remove label command
#
# - label:
#       Label to remove
# -----------------------------------------------------------------------------
def remove_label_cmd(label):
    label_id = get_label_id(label)
    remove_label(label_id)
    
# -----------------------------------------------------------------------------
# Add text command
# -----------------------------------------------------------------------------
def add_text_cmd():
    label = input("Label: ")
    if label == "":
        print("[ERROR] Invalid label")
        return
    
    if not exist_label(label):
        add_label(label)
    
    text = input("Text: ")
    if text == "":
        print("[ERROR] Text cannot be null")
    
    add_text(label, text)
    
# -----------------------------------------------------------------------------
# Edit text command
#
# - label:
#       Label of the text
# -----------------------------------------------------------------------------
def edit_text_cmd(label):
    text = input("New text: ")
    
    edit_text(label, text)
    
# -----------------------------------------------------------------------------
# Remove text command
#
# - label:
#       Label of the text
# -----------------------------------------------------------------------------
def remove_text_cmd(label):
    remove_text(label)
    
# -----------------------------------------------------------------------------
# Print command
#
# - label
#       Text label
# -----------------------------------------------------------------------------
def print_cmd(label):
    text = None
    
    try:
        text = get_text(label)
    except:
        print("[ERROR] Label '{}' not found".format(label))
        return
        
    print("{}: {}".format(label, text))
    
# -----------------------------------------------------------------------------
# List languages command
# -----------------------------------------------------------------------------
def list_lang_cmd():
    langs = list_languages()
    
    print("=== LANGUAGES ===")
    if not langs:
        print("[ALERT] No languages defined in the database.")
    else:
        for lang in langs:
            print("- {} ({})".format(lang[0], lang[1]))
            
# -----------------------------------------------------------------------------
# Help command
# -----------------------------------------------------------------------------
def help_cmd():
    print("Command list:")
    print(" -  set [lang_code]\t\t\tSets the working language")
    print(" -  addlang [lang_code] [lang_name]\tAdd a language to the database")
    print(" -  addtext \t\t\t\tAdd the text to a specific label for the current language")
    print(" -  list\t\t\t\tList the registered languages")
    print(" -  info\t\t\t\tGets info about the current language")
    print(" -  exit\t\t\t\tStops the program")

# -----------------------------------------------------------------------------
# Dispatcher for the user commands
#
# - cmd
#       User command
# -----------------------------------------------------------------------------
def cmd_dispatcher(cmd):
    # Set 
    if cmd.startswith("setlang "):
        set_lang_cmd(cmd[8:])
        
    # Add language
    elif cmd.startswith("addlang "):
        add_lang_cmd(cmd[8:].split())
        
    # Remove language
    elif cmd.startswith("rmlang "):
        remove_lang_cmd(cmd[7:])
        
    # Remove label
    elif cmd.startswith("rmlabel "):
        remove_label_cmd(cmd[8:])
        
    # Add text
    elif cmd == "addtext":
        add_text_cmd()
        
    # Edit test
    elif cmd.startswith("edit "):
        edit_text_cmd(cmd[5:])
        
    # Remove text
    elif cmd.startswith("rmtext "):
        remove_text_cmd(cmd[7:])
        
    # Print label text
    elif cmd.startswith("print "):
        print_cmd(cmd[6:])
        
    # List languages
    elif cmd == "list":
        list_lang_cmd()
    
    # Get info
    elif cmd == "info":
        print("[INFO] Currenct language: {}".format(curr_lang))
        
    # Help
    elif cmd == "help":
        help_cmd()
        
    # Exit
    elif cmd == "exit":
        global running
        running = False
        
    # Unknown message
    else:
        print("[ERROR] Unknown command. Type 'help' for the command list")

# -----------------------------------------------------------------------------
# Main program
# -----------------------------------------------------------------------------
def terminal():
    print("\t\t===== DR. FREEZE BOT INTL MANAGER =====")
    print("Welcome to the Dr. Freeze Bot INTL manager. Type 'help' for the command list.")
    
    open_connection()
    
    while running:
        cmd_dispatcher(input("> "))
        
    close_connection()
    
# -----------------------------------------------------------------------------

terminal()
