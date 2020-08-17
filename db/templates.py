get_polygon: str = """select id, name, class_id, props, _created, _updated,
                st_asgeojson(gis_polygon.geom)::json -> 'coordinates' as geom
                from gis_polygon where id={} order by id desc;"""

get_polygons: str = """select id, name, class_id, props, _created, _updated,
                st_asgeojson(gis_polygon.geom)::json -> 'coordinates' as geom
                from gis_polygon order by id desc;"""

create_polygon: str = """insert into gis_polygon (id, class_id, name, props, geom)
            values (nextval('gis_polygon_id_seq'), {}, '{}', '{}',
                ST_GeomFromEWKT('SRID=4326; POLYGON(({}))'))
            returning id, class_id, name, props, st_asgeojson(geom)::json -> 
            'coordinates' as geom;"""

update_polygon: str = """update gis_polygon set class_id={}, name='{}',
                       props='{}', geom=ST_GeomFromEWKT(
                           'SRID=4326; POLYGON(({}))') where id={}
                    returning id, class_id, name, props, 
                    st_asgeojson(geom)::json -> 'coordinates' as geom;"""



