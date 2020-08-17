from sqlalchemy import Column, Integer, String, Sequence, JSON, DateTime, MetaData, Table, \
    create_engine
from sqlalchemy.sql import func
from geoalchemy2 import Geometry

from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

engine = create_engine(
    f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}', echo=True)

metadata = MetaData()


polygon_table = Table(
    'gis_polygon',
    metadata,
    Column('id', Integer, Sequence('gis_polygon_id_seq'), primary_key=True),
    Column('class_id', Integer),
    Column('name', String),
    Column('props', JSON),
    Column('geom', Geometry(srid=4326, geometry_type='POLYGON')),
    Column('_created', DateTime(timezone=False), server_default=func.now()),
    Column('_updated', DateTime(timezone=False), onupdate=func.now()),
)

metadata.create_all(engine)

conn = engine.connect()

