--
-- PostgreSQL database dump
--

-- Dumped from database version 10.14 (Ubuntu 10.14-0ubuntu0.18.04.1)
-- Dumped by pg_dump version 10.14 (Ubuntu 10.14-0ubuntu0.18.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: DATABASE postgres; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: intl_txt; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.intl_txt (
    id integer NOT NULL,
    lang_id integer NOT NULL,
    label_id integer NOT NULL,
    txt text
);


ALTER TABLE public.intl_txt OWNER TO postgres;

--
-- Name: intl_txt_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.intl_txt_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.intl_txt_id_seq OWNER TO postgres;

--
-- Name: intl_txt_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.intl_txt_id_seq OWNED BY public.intl_txt.id;


--
-- Name: labels; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.labels (
    id integer NOT NULL,
    label character varying NOT NULL
);


ALTER TABLE public.labels OWNER TO postgres;

--
-- Name: labels_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.labels_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.labels_id_seq OWNER TO postgres;

--
-- Name: labels_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.labels_id_seq OWNED BY public.labels.id;


--
-- Name: languages; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.languages (
    id integer NOT NULL,
    code character varying(5) NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.languages OWNER TO postgres;

--
-- Name: languages_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.languages_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.languages_id_seq OWNER TO postgres;

--
-- Name: languages_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.languages_id_seq OWNED BY public.languages.id;


--
-- Name: product_watches; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.product_watches (
    id integer NOT NULL,
    user_id integer NOT NULL,
    product_id character varying NOT NULL,
    product_alias character varying NOT NULL,
    price_threshold numeric(9,2) NOT NULL,
    last_checked_price numeric(9,2)
);


ALTER TABLE public.product_watches OWNER TO postgres;

--
-- Name: product_watches_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.product_watches_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.product_watches_id_seq OWNER TO postgres;

--
-- Name: product_watches_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.product_watches_id_seq OWNED BY public.product_watches.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    telegram_id character varying,
    telegram_handle character varying,
    discord_id character varying,
    discord_handle character varying,
    pref_lang integer DEFAULT 1 NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: intl_txt id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.intl_txt ALTER COLUMN id SET DEFAULT nextval('public.intl_txt_id_seq'::regclass);


--
-- Name: labels id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.labels ALTER COLUMN id SET DEFAULT nextval('public.labels_id_seq'::regclass);


--
-- Name: languages id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.languages ALTER COLUMN id SET DEFAULT nextval('public.languages_id_seq'::regclass);


--
-- Name: product_watches id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_watches ALTER COLUMN id SET DEFAULT nextval('public.product_watches_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: intl_txt; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.intl_txt (id, lang_id, label_id, txt) FROM stdin;
\.


--
-- Data for Name: labels; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.labels (id, label) FROM stdin;
\.


--
-- Data for Name: languages; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.languages (id, code, name) FROM stdin;
1	en_EN	English
\.


--
-- Data for Name: product_watches; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.product_watches (id, user_id, product_id, product_alias, price_threshold, last_checked_price) FROM stdin;
5	3	B087LT7NVB	POWERADD Batterie Alcaline AAA Confezione da 20 Pile Stilo AAA da 1.5V	8.00	7.99
8	4	B07K2J9DB9	POLIPO PELUCHE ＰＵＣＣＩＯＳＯ	14.50	\N
9	1	B07747FR44	Kindle	100.00	\N
10	2	B086PKYL63	Nuova versione 2020 - Frullatore ad Immersione Inox 5 in 1 - Piede Frullatore, Sbattitore Elettrico, Mixer - Multifunzione 1000 W, 9 Velocità - Accessori Gratuiti	30.00	\N
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, telegram_id, telegram_handle, discord_id, discord_handle, pref_lang) FROM stdin;
1	120725601	dr4ghs	\N	\N	1
2	258862683	None	\N	\N	1
3	129252760	Froz3nYoutube	\N	\N	1
4	864756488	Aakhet	\N	\N	1
5	919431472	philofobico	\N	\N	1
7	202539914	TullioSax	\N	\N	1
8	354874009	None	\N	\N	1
9	601550354	JeezyX	\N	\N	1
10	1239507432	FuckingHellBoi	\N	\N	1
\.


--
-- Name: intl_txt_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.intl_txt_id_seq', 1, false);


--
-- Name: labels_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.labels_id_seq', 1, false);


--
-- Name: languages_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.languages_id_seq', 1, true);


--
-- Name: product_watches_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.product_watches_id_seq', 11, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 10, true);


--
-- Name: intl_txt intl_txt_lang_id_label_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.intl_txt
    ADD CONSTRAINT intl_txt_lang_id_label_id_key UNIQUE (lang_id, label_id);


--
-- Name: intl_txt intl_txt_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.intl_txt
    ADD CONSTRAINT intl_txt_pkey PRIMARY KEY (id);


--
-- Name: labels labels_label_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.labels
    ADD CONSTRAINT labels_label_key UNIQUE (label);


--
-- Name: labels labels_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.labels
    ADD CONSTRAINT labels_pkey PRIMARY KEY (id);


--
-- Name: languages languages_code_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.languages
    ADD CONSTRAINT languages_code_key UNIQUE (code);


--
-- Name: languages languages_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.languages
    ADD CONSTRAINT languages_pkey PRIMARY KEY (id);


--
-- Name: product_watches product_watches_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_watches
    ADD CONSTRAINT product_watches_pkey PRIMARY KEY (id);


--
-- Name: users users_discord_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_discord_id_key UNIQUE (discord_id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: users users_telegram_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_telegram_id_key UNIQUE (telegram_id);


--
-- Name: intl_txt intl_txt_label_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.intl_txt
    ADD CONSTRAINT intl_txt_label_id_fkey FOREIGN KEY (label_id) REFERENCES public.labels(id);


--
-- Name: intl_txt intl_txt_lang_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.intl_txt
    ADD CONSTRAINT intl_txt_lang_id_fkey FOREIGN KEY (lang_id) REFERENCES public.languages(id);


--
-- Name: product_watches product_watches_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.product_watches
    ADD CONSTRAINT product_watches_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- Name: users users_pref_lang_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pref_lang_fkey FOREIGN KEY (pref_lang) REFERENCES public.languages(id);


--
-- PostgreSQL database dump complete
--

