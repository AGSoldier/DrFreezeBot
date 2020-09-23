-- -----------------------------------------------------------------------------
-- CREATE TABLES
-- -----------------------------------------------------------------------------

-- LANGUAGES TABLE
DROP TABLE IF EXISTS languages CASCADE;
CREATE TABLE languages(

    -- Columns
    id SERIAL NOT NULL,
    code varchar(5) NOT NULL,
    name varchar NOT NULL, 
    
    -- Constraints
    PRIMARY KEY(id),
    UNIQUE(code)

);

-- USERS TABLE
DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users(

    -- Columns
    id SERIAL NOT NULL,
    telegram_id varchar,
    telegram_handle varchar,
    discord_id varchar,
    discord_handle varchar,
    pref_lang int NOT NULL DEFAULT(1),
    
    -- Constraints
    PRIMARY KEY(id),
    FOREIGN KEY(pref_lang) REFERENCES languages(id),
    UNIQUE(telegram_id),
    UNIQUE(discord_id)
    
);

-- LABELS TABLE
DROP TABLE IF EXISTS labels CASCADE;
CREATE TABLE labels(

    -- Columns
    id SERIAL NOT NULL,
    label varchar NOT NULL,
    
    -- Constraints
    PRIMARY KEY(id),
    UNIQUE(label)

);

-- PRODUCT WATCHES TABLE
DROP TABLE IF EXISTS product_watches CASCADE;
CREATE TABLE product_watches(

    -- Columns
    id SERIAL NOT NULL,
    user_id int NOT NULL,
    product_id varchar NOT NULL,
    product_alias varchar NOT NULL,
    price_threshold numeric(9, 2) NOT NULL,
    last_checked_price numeric(9, 2),
    
    -- Constrints
    PRIMARY KEY(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
    
);

-- INTERNATIONAL TEXT TABLE
DROP TABLE IF EXISTS intl_txt CASCADE;
CREATE TABLE intl_txt(

    -- Columns
    id SERIAL NOT NULL,
    lang_id int NOT NULL,
    label_id int NOT NULL,
    txt text,
    
    -- Constraints
    PRIMARY KEY(id),
    FOREIGN KEY(lang_id) REFERENCES languages(id),
    FOREIGN KEY(label_id) REFERENCES labels(id),
    UNIQUE(lang_id, label_id)

);

-- ----------------------------------------------------------------------------
-- INSERT VALUES
-- ----------------------------------------------------------------------------

-- INSERT INTO LANGUAGES
INSERT INTO languages(code, name)
VALUES('en_EN', 'English');