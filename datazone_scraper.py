__author__ = 'Modulo'

import requests
import xml.etree.ElementTree
import _mysql


def sparql(code):
    q = """
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
        PREFIX statistical-geography: <http://statistics.data.gov.uk/def/statistical-geography#>
        PREFIX boundary-change: <http://statistics.data.gov.uk/def/boundary-change/>
        PREFIX statistical-entity: <http://statistics.data.gov.uk/def/statistical-entity#>
        PREFIX geopos: <http://www.w3.org/2003/01/geo/wgs84_pos#>
        PREFIX osspatial: <http://data.ordnancesurvey.co.uk/ontology/spatialrelations/>
        PREFIX bestfit: <http://statistics.data.gov.uk/def/hierarchy/best-fit#>
        CONSTRUCT {
            # constructing properties of http://statistics.data.gov.uk/id/statistical-geography/""" + code + """
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> rdf:type ?var_1_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> rdfs:label ?var_2_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> skos:notation ?var_3_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> statistical-geography:officialname ?var_4_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> boundary-change:originatingChangeOrder ?var_5_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> boundary-change:changeOrderTitle ?var_6_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> boundary-change:operativedate ?var_7_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> boundary-change:terminateddate ?var_8_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> statistical-geography:status ?var_9_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> statistical-geography:parentcode ?var_10_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> statistical-entity:code ?var_11_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> statistical-entity:owner ?var_12_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> geopos:long ?var_13_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> geopos:lat ?var_14_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> osspatial:northing ?var_15_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> osspatial:easting ?var_16_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> <http://statistics.data.gov.uk/def/spatialrelations/within#lsoa> ?var_17_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> <http://statistics.data.gov.uk/def/spatialrelations/within#msoa> ?var_18_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> <http://statistics.data.gov.uk/def/spatialrelations/within#lad> ?var_19_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> bestfit:ward ?var_20_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> bestfit:primarycareorganisation ?var_21_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> bestfit:strategichealthauthority ?var_22_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> bestfit:parliamentaryconstituency ?var_23_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> bestfit:europeanelectoralregion ?var_24_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> statistical-geography:hasExteriorEastNorthPolygon ?var_25_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> statistical-geography:hasInteriorEastNorthPolygon ?var_26_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> statistical-geography:hasExteriorLatLongPolygon ?var_27_0 .
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> statistical-geography:hasInteriorLatLongPolygon ?var_28_0 .
        }  WHERE {
          # identifying properties of http://statistics.data.gov.uk/id/statistical-geography/""" + code + """
          {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> rdf:type ?var_1_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> rdfs:label ?var_2_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> skos:notation ?var_3_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> statistical-geography:officialname ?var_4_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> boundary-change:originatingChangeOrder ?var_5_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> boundary-change:changeOrderTitle ?var_6_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> boundary-change:operativedate ?var_7_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> boundary-change:terminateddate ?var_8_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> statistical-geography:status ?var_9_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> statistical-geography:parentcode ?var_10_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> statistical-entity:code ?var_11_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> statistical-entity:owner ?var_12_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> geopos:long ?var_13_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> geopos:lat ?var_14_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> osspatial:northing ?var_15_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> osspatial:easting ?var_16_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> <http://statistics.data.gov.uk/def/spatialrelations/within#lsoa> ?var_17_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> <http://statistics.data.gov.uk/def/spatialrelations/within#msoa> ?var_18_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> <http://statistics.data.gov.uk/def/spatialrelations/within#lad> ?var_19_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> bestfit:ward ?var_20_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> bestfit:primarycareorganisation ?var_21_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> bestfit:strategichealthauthority ?var_22_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> bestfit:parliamentaryconstituency ?var_23_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> bestfit:europeanelectoralregion ?var_24_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> statistical-geography:hasExteriorEastNorthPolygon ?var_25_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> statistical-geography:hasInteriorEastNorthPolygon ?var_26_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> statistical-geography:hasExteriorLatLongPolygon ?var_27_0 .
          } UNION {
            <http://statistics.data.gov.uk/id/statistical-geography/""" + code + """> statistical-geography:hasInteriorLatLongPolygon ?var_28_0 .
          }
        }
    """
    return q


def query(n):
    zone = "S0" + (str)(1000001 + n)

    values = {'query': sparql(zone)}
    r = requests.post("http://statistics.data.gov.uk/sparql", values)

    tree = xml.etree.ElementTree.XML(r.text)

    polygons_xml = tree[0].findall("{http://statistics.data.gov.uk/def/statistical-geography#}hasExteriorLatLongPolygon")
    polygons = []

    for polygon in polygons_xml:
        polygon_txt = polygon.text.split(' ')

        polygon = []
        i = 0
        count = 0
        x_centre = 0
        y_centre = 0

        while i < len(polygon_txt)-1:
            x = float(polygon_txt[i])
            y = float(polygon_txt[i+1])
            polygon.append((x, y))
            x_centre += x
            y_centre += y

            count += 1
            i += 2
        centre = (x_centre/count, y_centre/count)

        polygons.append((polygon, centre))

    part_of = tree[0][0].attrib.values()[0].split('/')[-1]

    return (zone, part_of, polygons)

def insertPolygons(data, db):
    zone = data[0]
    polygons = data[2]

    for (polygon, (centre_x, centre_y)) in polygons:
        q_polygon = "INSERT INTO `datazone_polygons`(`datazone`, `centre_x`, `centre_y`) VALUES ('{0}', '{1}', '{2}')".format(zone, centre_x, centre_y)
        db.query(q_polygon)
        polygon_id = db.insert_id()
        print "- {0} polygon {1} inserted".format(zone, polygon_id)

        q_vertices = "INSERT INTO `datazone_vertices`(`polygon_id`, `coord_x`, `coord_y`) VALUES "

        values = []
        for (coord_x, coord_y) in polygon:
            values.append("('{0}', '{1}', '{2}', '{3}' )".format(zone, polygon_id, coord_x, coord_y))

        q_vertices += ' , '.join(values)

        db.query(q_vertices)
        print "-- {0} polygon {1} - {2} vertices inserted".format(zone, polygon_id, len(polygon))

    print "{0} - {1} polygon(s) inserted".format(zone, len(polygons))

def updateDatazones(data, db):
    zone = data[0]
    part_of = data[1]

    q = "UPDATE `datazones` SET `partof`= '{0}' WHERE code='{1}'".format(part_of, zone)
    db.query(q)
    print "{0} update OK!".format(zone)

db =_mysql.connect(host="localhost",user="ilwhack14", passwd="hackathon",db="ilwhack14")
for n in xrange(6505):
    data = query(n)
    updateDatazones(data, db)
    insertPolygons(data, db)
