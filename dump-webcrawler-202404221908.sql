PGDMP                         |        
   webcrawler    15.5 (Debian 15.5-0+deb12u1)    15.3     �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    30226 
   webcrawler    DATABASE     v   CREATE DATABASE webcrawler WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'en_US.UTF-8';
    DROP DATABASE webcrawler;
             
   webcrawler    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
                pg_database_owner    false            �           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                   pg_database_owner    false    4            �            1259    30228    band    TABLE     X   CREATE TABLE public.band (
    band_id integer NOT NULL,
    band_name text NOT NULL
);
    DROP TABLE public.band;
       public         heap 
   webcrawler    false    4            �            1259    30227    band_band_id_seq    SEQUENCE     �   CREATE SEQUENCE public.band_band_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.band_band_id_seq;
       public       
   webcrawler    false    4    215            �           0    0    band_band_id_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.band_band_id_seq OWNED BY public.band.band_id;
          public       
   webcrawler    false    214            �            1259    30237    band_url    TABLE     K  CREATE TABLE public.band_url (
    url_id integer NOT NULL,
    band_id integer NOT NULL,
    url text NOT NULL,
    hash_value text,
    date_added timestamp without time zone DEFAULT CURRENT_TIMESTAMP,
    last_updated timestamp without time zone,
    class_name character varying,
    last_failed timestamp without time zone
);
    DROP TABLE public.band_url;
       public         heap 
   webcrawler    false    4            �            1259    30236    url_hash_url_id_seq    SEQUENCE     �   CREATE SEQUENCE public.url_hash_url_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 *   DROP SEQUENCE public.url_hash_url_id_seq;
       public       
   webcrawler    false    217    4            �           0    0    url_hash_url_id_seq    SEQUENCE OWNED BY     K   ALTER SEQUENCE public.url_hash_url_id_seq OWNED BY public.band_url.url_id;
          public       
   webcrawler    false    216            
           2604    30231    band band_id    DEFAULT     l   ALTER TABLE ONLY public.band ALTER COLUMN band_id SET DEFAULT nextval('public.band_band_id_seq'::regclass);
 ;   ALTER TABLE public.band ALTER COLUMN band_id DROP DEFAULT;
       public       
   webcrawler    false    215    214    215                       2604    30240    band_url url_id    DEFAULT     r   ALTER TABLE ONLY public.band_url ALTER COLUMN url_id SET DEFAULT nextval('public.url_hash_url_id_seq'::regclass);
 >   ALTER TABLE public.band_url ALTER COLUMN url_id DROP DEFAULT;
       public       
   webcrawler    false    216    217    217            �          0    30228    band 
   TABLE DATA           2   COPY public.band (band_id, band_name) FROM stdin;
    public       
   webcrawler    false    215          �          0    30237    band_url 
   TABLE DATA           w   COPY public.band_url (url_id, band_id, url, hash_value, date_added, last_updated, class_name, last_failed) FROM stdin;
    public       
   webcrawler    false    217   4       �           0    0    band_band_id_seq    SEQUENCE SET     >   SELECT pg_catalog.setval('public.band_band_id_seq', 8, true);
          public       
   webcrawler    false    214            �           0    0    url_hash_url_id_seq    SEQUENCE SET     B   SELECT pg_catalog.setval('public.url_hash_url_id_seq', 15, true);
          public       
   webcrawler    false    216                       2606    30235    band band_pkey 
   CONSTRAINT     Q   ALTER TABLE ONLY public.band
    ADD CONSTRAINT band_pkey PRIMARY KEY (band_id);
 8   ALTER TABLE ONLY public.band DROP CONSTRAINT band_pkey;
       public         
   webcrawler    false    215                       2606    30245    band_url url_hash_pkey 
   CONSTRAINT     X   ALTER TABLE ONLY public.band_url
    ADD CONSTRAINT url_hash_pkey PRIMARY KEY (url_id);
 @   ALTER TABLE ONLY public.band_url DROP CONSTRAINT url_hash_pkey;
       public         
   webcrawler    false    217                       2606    30246    band_url url_hash_band_id_fkey    FK CONSTRAINT     �   ALTER TABLE ONLY public.band_url
    ADD CONSTRAINT url_hash_band_id_fkey FOREIGN KEY (band_id) REFERENCES public.band(band_id);
 H   ALTER TABLE ONLY public.band_url DROP CONSTRAINT url_hash_band_id_fkey;
       public       
   webcrawler    false    217    3854    215            �   "   x�3���su�q�2�tv������� S�      �     x�e��m�0E��] �D��!:A.�L�-�8����urR���?<�����%�}+�u������8[����PCC���Q�T'l��SU@H�02j�[A%�X�T!r wwQ^�Q3� �ɁsH>Dt�V��3�fE���{�q����ڲ�z{����$	�Z��J��ʈ����`����l�1T�J���>K�쑢$�#�k0A��GfBqn�����v�����bynNڜ���s�"IL7��w]�S�g�     