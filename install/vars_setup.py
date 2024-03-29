#!/usr/bin/env python3

from getpass import getpass

# -----------------------------------------------------------------------------
# VARIABLES INPUT
# -----------------------------------------------------------------------------
print("ENVIRONMENT VARIABLES")

# Input database name
db_name = input("Database name: ")
if db_name == "":
    db_name = "none"
    
# Input database user
db_user = input("Database user: ")
if db_user == "":
    db_user = "none"
    
# Input database user password
db_pass = getpass("Database user password: ")
db_pass_confirm = getpass("Confirm password: ")

if db_pass == "":
    db_pass = "none"
    
if not db_pass == db_pass_confirm:
    print("Incorrect password, exiting")
    exit()
    
# Database host
db_host = input("Database host (default is localhost): ")
if db_host == "":
    db_host = "localhost"
    
# Database port
db_port = input("Database port (default is 5432): ")
if db_port == "":
    db_port = "5432"
    
# Telegram token
telegram_token = input("Telegram token: ")
if telegram_token == "":
    telegram_token = "none"
    
# Discord token
discord_token = input("Discord token: ")
if discord_token == "":
    discord_token = "none"
    
# Amazon access key
amazon_access_key = input("Amazon access key: ")
if amazon_access_key == "":
    amazon_access_key = "none"

# Amazon secret key
amazon_secret_key = input("Amazon secret key: ")
if amazon_secret_key == "":
    amazon_secret_key = "none"

# Amazon associate tag
amazon_assoc_tag = input("Amazon associate tag: ")
if amazon_assoc_tag == "":
    amazon_assoc_tag = "none"

env_vars = """
    export DB_NAME={}\n
    export DB_USER={}\n
    export DB_PASS={}\n
    export DB_HOST={}\n
    export DB_PORT={}\n
    export TELEGRAM_TOKEN={}\n
    export DISCORD_TOKEN={}\n
    export AMAZON_ACCESS_KEY={}\n
    export AMAZON_SECRET_KEY={}\n
    export AMAZON_ASSOC_TAG={}\n
    """.format(
        db_name, 
        db_user, 
        db_pass, 
        db_host, 
        db_port, 
        telegram_token, 
        discord_token,
        amazon_access_key,
        amazon_secret_key,
        amazon_assoc_tag)

print("\n")

# -----------------------------------------------------------------------------
# BOT FILE CREATION
# -----------------------------------------------------------------------------
print("[INFO] Creating variables file...")

vars_file_path = "/etc/profile.d/drfreeze_vars.sh"
with open(vars_file_path, "w+") as file:
    file.write("#!/bin/bash\n\n")
    file.write(env_vars)
        
print("[INFO] Variables file created successfully!")
