--
-- PostgreSQL database dump
--

-- Dumped from database version 17.5 (Debian 17.5-1.pgdg110+1)
-- Dumped by pg_dump version 17.5

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: ogr_system_tables; Type: SCHEMA; Schema: -; Owner: YOURUSER
--

CREATE SCHEMA ogr_system_tables;


ALTER SCHEMA ogr_system_tables OWNER TO YOURUSER;

--
-- Name: postgis; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS postgis WITH SCHEMA public;


--
-- Name: EXTENSION postgis; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION postgis IS 'PostGIS geometry and geography spatial types and functions';


--
-- Name: event_trigger_function_for_metadata(); Type: FUNCTION; Schema: ogr_system_tables; Owner: YOURUSER
--

CREATE FUNCTION ogr_system_tables.event_trigger_function_for_metadata() RETURNS event_trigger
    LANGUAGE plpgsql
    AS $$
DECLARE
    obj record;
BEGIN
  IF has_schema_privilege('ogr_system_tables', 'USAGE') THEN
   IF has_table_privilege('ogr_system_tables.metadata', 'DELETE') THEN
    FOR obj IN SELECT * FROM pg_event_trigger_dropped_objects()
    LOOP
        IF obj.object_type = 'table' THEN
            DELETE FROM ogr_system_tables.metadata m WHERE m.schema_name = obj.schema_name AND m.table_name = obj.object_name;
        END IF;
    END LOOP;
   END IF;
  END IF;
END;
$$;


ALTER FUNCTION ogr_system_tables.event_trigger_function_for_metadata() OWNER TO YOURUSER;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: metadata; Type: TABLE; Schema: ogr_system_tables; Owner: YOURUSER
--

CREATE TABLE ogr_system_tables.metadata (
    id integer NOT NULL,
    schema_name text NOT NULL,
    table_name text NOT NULL,
    metadata text
);


ALTER TABLE ogr_system_tables.metadata OWNER TO YOURUSER;

--
-- Name: metadata_id_seq; Type: SEQUENCE; Schema: ogr_system_tables; Owner: YOURUSER
--

CREATE SEQUENCE ogr_system_tables.metadata_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE ogr_system_tables.metadata_id_seq OWNER TO YOURUSER;

--
-- Name: metadata_id_seq; Type: SEQUENCE OWNED BY; Schema: ogr_system_tables; Owner: YOURUSER
--

ALTER SEQUENCE ogr_system_tables.metadata_id_seq OWNED BY ogr_system_tables.metadata.id;


--
-- Name: administrative_divisions; Type: TABLE; Schema: public; Owner: YOURUSER
--

CREATE TABLE public.administrative_divisions (
    id bigint NOT NULL,
    geom public.geometry(MultiPolygon,7801),
    obns_num character varying(254),
    obns_cyr character varying(254),
    obns_lat character varying(254)
);


ALTER TABLE public.administrative_divisions OWNER TO YOURUSER;

--
-- Name: sofia_land_items; Type: TABLE; Schema: public; Owner: YOURUSER
--

CREATE TABLE public.sofia_land_items (
    ogc_fid integer NOT NULL,
    wkb_geometry public.geometry(Polygon,7801),
    area numeric(30,15),
    perim numeric(50,30),
    cadimm double precision,
    cadnum character varying(254),
    cadreg double precision,
    cattype character varying(254),
    ekatte character varying(254),
    ekattefn character varying(254),
    immaddr character varying(254),
    oldident character varying(254),
    parcel character varying(254),
    place character varying(254),
    propcode character varying(254),
    proptype character varying(254),
    purpcode character varying(254),
    purptype character varying(254),
    quarname character varying(254),
    quarter character varying(254),
    regname character varying(254),
    strename character varying(254),
    strnum character varying(254),
    usecode character varying(254),
    usetype character varying(254),
    validate character varying(254)
);


ALTER TABLE public.sofia_land_items OWNER TO YOURUSER;

--
-- Name: sofia_land_items_ogc_fid_seq; Type: SEQUENCE; Schema: public; Owner: YOURUSER
--

CREATE SEQUENCE public.sofia_land_items_ogc_fid_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.sofia_land_items_ogc_fid_seq OWNER TO YOURUSER;

--
-- Name: sofia_land_items_ogc_fid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: YOURUSER
--

ALTER SEQUENCE public.sofia_land_items_ogc_fid_seq OWNED BY public.sofia_land_items.ogc_fid;


--
-- Name: metadata id; Type: DEFAULT; Schema: ogr_system_tables; Owner: YOURUSER
--

ALTER TABLE ONLY ogr_system_tables.metadata ALTER COLUMN id SET DEFAULT nextval('ogr_system_tables.metadata_id_seq'::regclass);


--
-- Name: sofia_land_items ogc_fid; Type: DEFAULT; Schema: public; Owner: YOURUSER
--

ALTER TABLE ONLY public.sofia_land_items ALTER COLUMN ogc_fid SET DEFAULT nextval('public.sofia_land_items_ogc_fid_seq'::regclass);


--
-- Name: metadata metadata_schema_name_table_name_key; Type: CONSTRAINT; Schema: ogr_system_tables; Owner: YOURUSER
--

ALTER TABLE ONLY ogr_system_tables.metadata
    ADD CONSTRAINT metadata_schema_name_table_name_key UNIQUE (schema_name, table_name);


--
-- Name: administrative_divisions administrative_divisions_pk; Type: CONSTRAINT; Schema: public; Owner: YOURUSER
--

ALTER TABLE ONLY public.administrative_divisions
    ADD CONSTRAINT administrative_divisions_pk PRIMARY KEY (id);


--
-- Name: sofia_land_items sofia_land_items_pkey; Type: CONSTRAINT; Schema: public; Owner: YOURUSER
--

ALTER TABLE ONLY public.sofia_land_items
    ADD CONSTRAINT sofia_land_items_pkey PRIMARY KEY (ogc_fid);


--
-- Name: sofia_land_items_wkb_geometry_geom_idx; Type: INDEX; Schema: public; Owner: YOURUSER
--

CREATE INDEX sofia_land_items_wkb_geometry_geom_idx ON public.sofia_land_items USING gist (wkb_geometry);


--
-- Name: ogr_system_tables_event_trigger_for_metadata; Type: EVENT TRIGGER; Schema: -; Owner: YOURUSER
--

CREATE EVENT TRIGGER ogr_system_tables_event_trigger_for_metadata ON sql_drop
   EXECUTE FUNCTION ogr_system_tables.event_trigger_function_for_metadata();


ALTER EVENT TRIGGER ogr_system_tables_event_trigger_for_metadata OWNER TO YOURUSER;

--
-- PostgreSQL database dump complete
--

