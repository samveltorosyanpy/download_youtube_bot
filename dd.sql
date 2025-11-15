--
-- PostgreSQL database dump
--

-- Dumped from database version 15.5 (Ubuntu 15.5-1.pgdg22.04+1)
-- Dumped by pg_dump version 15.5 (Ubuntu 15.5-1.pgdg22.04+1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: links; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.links (
    source text NOT NULL,
    price integer DEFAULT 0 NOT NULL,
    users_count integer DEFAULT 0 NOT NULL,
    subscriptions_count integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.links OWNER TO postgres;

--
-- Name: payments; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payments (
    id integer NOT NULL,
    user_id bigint NOT NULL,
    sum integer NOT NULL,
    link text NOT NULL,
    created_by timestamp with time zone NOT NULL
);


ALTER TABLE public.payments OWNER TO postgres;

--
-- Name: payments_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.payments_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.payments_id_seq OWNER TO postgres;

--
-- Name: payments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.payments_id_seq OWNED BY public.payments.id;


--
-- Name: reflinks; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.reflinks (
    id integer NOT NULL,
    source text NOT NULL,
    price integer DEFAULT 0 NOT NULL,
    all_count integer DEFAULT 0 NOT NULL,
    unique_count integer DEFAULT 0 NOT NULL,
    subscriptions_count integer DEFAULT 0 NOT NULL,
    is_archive boolean DEFAULT false NOT NULL,
    created_at timestamp with time zone NOT NULL
);


ALTER TABLE public.reflinks OWNER TO postgres;

--
-- Name: reflinks_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.reflinks_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.reflinks_id_seq OWNER TO postgres;

--
-- Name: reflinks_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.reflinks_id_seq OWNED BY public.reflinks.id;


--
-- Name: requests; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.requests (
    id bigint NOT NULL,
    name text NOT NULL
);


ALTER TABLE public.requests OWNER TO postgres;

--
-- Name: requests_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.requests_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.requests_id_seq OWNER TO postgres;

--
-- Name: requests_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.requests_id_seq OWNED BY public.requests.id;


--
-- Name: subs; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.subs (
    id bigint NOT NULL,
    lang text NOT NULL,
    name text NOT NULL,
    link text NOT NULL,
    count integer DEFAULT 0 NOT NULL
);


ALTER TABLE public.subs OWNER TO postgres;

--
-- Name: subs_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.subs_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.subs_id_seq OWNER TO postgres;

--
-- Name: subs_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.subs_id_seq OWNED BY public.subs.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id bigint NOT NULL,
    verified boolean DEFAULT true NOT NULL,
    is_subscribe boolean DEFAULT false NOT NULL,
    is_dead boolean DEFAULT false NOT NULL,
    source text NOT NULL,
    state text NOT NULL,
    vip bigint DEFAULT 0 NOT NULL,
    lang text NOT NULL,
    subs text NOT NULL,
    last_activity double precision DEFAULT 0 NOT NULL,
    created_by timestamp with time zone NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
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
-- Name: views; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.views (
    id integer NOT NULL,
    type text NOT NULL,
    owner_id bigint NOT NULL,
    users text NOT NULL,
    progress integer DEFAULT 0 NOT NULL,
    "end" integer NOT NULL,
    text text NOT NULL,
    btn_text text NOT NULL,
    btn_url text NOT NULL,
    is_start boolean
);


ALTER TABLE public.views OWNER TO postgres;

--
-- Name: views_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.views_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.views_id_seq OWNER TO postgres;

--
-- Name: views_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.views_id_seq OWNED BY public.views.id;


--
-- Name: payments id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments ALTER COLUMN id SET DEFAULT nextval('public.payments_id_seq'::regclass);


--
-- Name: reflinks id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reflinks ALTER COLUMN id SET DEFAULT nextval('public.reflinks_id_seq'::regclass);


--
-- Name: requests id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests ALTER COLUMN id SET DEFAULT nextval('public.requests_id_seq'::regclass);


--
-- Name: subs id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.subs ALTER COLUMN id SET DEFAULT nextval('public.subs_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Name: views id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.views ALTER COLUMN id SET DEFAULT nextval('public.views_id_seq'::regclass);


--
-- Data for Name: links; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.links (source, price, users_count, subscriptions_count) FROM stdin;
\.


--
-- Data for Name: payments; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.payments (id, user_id, sum, link, created_by) FROM stdin;
\.


--
-- Data for Name: reflinks; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.reflinks (id, source, price, all_count, unique_count, subscriptions_count, is_archive, created_at) FROM stdin;
1	c03b411f8376	1	0	0	0	f	2024-03-09 00:42:59.158594+03
\.


--
-- Data for Name: requests; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.requests (id, name) FROM stdin;
\.


--
-- Data for Name: subs; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.subs (id, lang, name, link, count) FROM stdin;
\.



COPY public.views (id, type, owner_id, users, progress, "end", text, btn_text, btn_url, is_start) FROM stdin;
26002	type	1005792177	6046824712#703852832#703852832#1005792177#1391333607#6632425856#5852202723#5972043305#786024078#5588356366#1983824036#5619533114#5619533114#6285675964#961449096#6831962627#6752113979#1242833007#1613551208#5619533114#1400817444#1613551208#1613551208#1613551208#5619533114#1613551208#1613551208#1613551208#5619533114#6757793267#1334160480#1242833007#1242833007#657717080#5243112719#1005792177#5972043305#5879588140#6907816509#5106714712#937563611#6523449968#6957917668#1400817444#6648781058#5798671231#6857513473#1469498147#1455210510#6113386743#6113386743#1469498147#1983824036#5238956521#1469498147#1359178409#2121638145#6759631713#6193835021#6351308717#6351308717#6113386743#6351308717#6351308717#6351308717#6351308717#6351308717#1002432736#6351308717#2016970080#1369153680#6351308717#6351308717#6351308717#6351308717#6752113979#6752113979#6752113979#2016970080#6351308717#961449096#5443622473#6750303006#1650490235#6580933932#6040805783#6040805783#5831668176#6814809581#6814809581#5972043305#1818016257#6193835021#859403359#5066025076#1002432736#6193835021#6193835021#5798671231#1104507870#1104507870#1104507870#1104507870#6193835021#6762204240#6253235832#961449096#2119803325#6363874486#5759106380#6752113979#1198703872#1290646386#1290646386#6343874549#5443622473#5238956521#5852202723#5852202723#5852202723#5852202723#5830023580#6066672067#6066672067#6066672067#6697980669#6846382267#6193835021#6671695048#1616302156#1198703872#1621640030#1621640030#1621640030#1621640030#1621640030#5144438644#5852202723#5213855735#5213855735#6431577072#6431577072#7160780810#1005792177#6066672067#5122228938#1306768833#6490954268#6393638630#5122228938#5122228938#6389284390#5388066501#1469498147#	154	100000	Ուղարկիր ընկերներիդ բոտի հղումը 👇\n\nhttps://t.me/SkachatsYouTubebot \n\nՈրպեսզի նրանքել կարողանան իրենց սիրելի երգերը փոփոխեն տարբեր եղանակներով։			f
\.


--
-- Name: payments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.payments_id_seq', 1, false);


--
-- Name: reflinks_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.reflinks_id_seq', 1, true);


--
-- Name: requests_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.requests_id_seq', 1, false);


--
-- Name: subs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.subs_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- Name: views_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.views_id_seq', 1, false);


--
-- Name: links links_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.links
    ADD CONSTRAINT links_pkey PRIMARY KEY (source);


--
-- Name: payments payments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.payments
    ADD CONSTRAINT payments_pkey PRIMARY KEY (id);


--
-- Name: reflinks reflinks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.reflinks
    ADD CONSTRAINT reflinks_pkey PRIMARY KEY (id);


--
-- Name: requests requests_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.requests
    ADD CONSTRAINT requests_pkey PRIMARY KEY (id);


--
-- Name: subs subs_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

    ADD CONSTRAINT subs_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.subs


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: views views_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.views
    ADD CONSTRAINT views_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--

