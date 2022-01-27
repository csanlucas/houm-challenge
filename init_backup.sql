--
-- PostgreSQL database dump
--

-- Dumped from database version 12.6
-- Dumped by pg_dump version 12.6

--
-- Data for Name: locator_houmer; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.locator_houmer (id, name, description) FROM stdin;
1	HM-NAME1	houmer code challenge
2	HM-NAME2	houmer code challenge
\.


--
-- Data for Name: locator_houmerlocation; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.locator_houmerlocation (id, latitude, longitude, "houmerId_id", "deviceId", created_at, velocity_kmh) FROM stdin;
1	-33.456329	-70.644175	1	DVID-TABLET1	2022-01-26 21:13:50.741938+00	0
2	-2.11488	-79.968221	1	DVID-TABLET1	2022-01-27 06:53:34.214644+00	0
3	-2.11488	-79.968221	1	DVID-TABLET1	2022-01-27 06:54:10.401376+00	20
4	-2.11488	-79.968221	1	DVID-TABLET1	2022-01-27 06:54:18.745715+00	75
5	-2.11488	-79.968221	1	DVID-TABLET1	2022-01-27 06:54:26.062454+00	110
6	-2.11488	-79.968221	1	DVID-TABLET1	2022-01-27 06:54:31.58597+00	115
7	-2.11488	-79.968221	1	DVID-TABLET1	2022-01-27 06:54:38.501648+00	140
\.


--
-- Data for Name: locator_property; Type: TABLE DATA; Schema: public; Owner: root
--

COPY public.locator_property (id, arrive_at, departure_at, latitude, longitude, visited_by_id) FROM stdin;
1	2022-01-27 03:24:12.864839+00	2022-01-27 06:30:28.618+00	-33.456329	-70.644175	1
\.


--
-- Name: locator_houmer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.locator_houmer_id_seq', 2, true);


--
-- Name: locator_houmerlocation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.locator_houmerlocation_id_seq', 7, true);


--
-- Name: locator_property_id_seq; Type: SEQUENCE SET; Schema: public; Owner: root
--

SELECT pg_catalog.setval('public.locator_property_id_seq', 1, true);


--
-- PostgreSQL database dump complete
--

