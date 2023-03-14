'''
    Generate mesh json file based on shapefile
'''

import geopandas as gpd
from shapely.geometry import Point
import json
import mapbox_earcut as earcut
import numpy as np
import pandas as pd
import os
import struct

def break_into_binary(filepath, filename, data, types, dataTypes):

    for index, type in enumerate(types):

        readCoords = 0

        floatList = []

        for i in range(len(data['data'])):
            geometry = data['data'][i]['geometry']

            newValue = [readCoords, len(geometry[type])] # where this vector starts and its size

            readCoords += len(geometry[type])

            floatList += geometry[type].copy()

            geometry[type] = newValue

        fout = open(os.path.join(filepath,filename+'_'+type+'.data'), 'wb')

        buf = struct.pack(str(len(floatList))+dataTypes[index], *floatList)

        fout.write(buf)
        fout.close()

        json_object = json.dumps(data)

        with open(os.path.join(filepath,filename+".json"), "w") as outfile:
            outfile.write(json_object)

def generateLayerFromShp(filepath, bbox, layerName, styleKey):
    '''
        In the same folder as the .shp file there must be a .prj and .shx files   

        The bounding box must be in the 4326 projection

        Only works for 2D geometries

        Returns gdf in 3395
    '''

    bbox_series_4326 = gpd.GeoSeries([Point(bbox[1], bbox[0]), Point(bbox[3], bbox[2])], crs=4326)
    
    loaded_shp = gpd.read_file(filepath, bbox=bbox_series_4326)

    bbox_series_4326 = bbox_series_4326.to_crs(3395)

    loaded_shp = loaded_shp.to_crs(3395)
    loaded_shp = loaded_shp.clip([bbox_series_4326[0].x, bbox_series_4326[0].y, bbox_series_4326[1].x, bbox_series_4326[1].y])

    zip_code_name = []
    zip_code_coordinates = []

    data = []
    objectId = []
    coordinates_geometries = []
    coordinates_ids = []
    coord_id_counter = 0

    for id, row in enumerate(loaded_shp.iloc):

        objectId.append(id)

        geometries = []
        if row['geometry'].geom_type == 'MultiPolygon':
            geometries = list(row['geometry'])
        elif row['geometry'].geom_type == 'Polygon':
            geometries = [row['geometry']]

        coordinates = []
        indices = []
        count = 0

        for geometry in geometries:
            points = np.array(geometry.exterior.coords[0:-1]) # remove last one (repeated)
            rings = np.array([len(points)])

            ind = earcut.triangulate_float64(points, rings)
            ind = (ind+count).tolist()
            indices += ind

            points = points.flatten().tolist()

            for i in range(0, len(points), 2):
                coordinates.append(points[i])
                coordinates.append(points[i+1])
                coordinates_geometries.append(Point(points[i], points[i+1]))
                coordinates_ids.append(coord_id_counter)
                coord_id_counter += 1
                coordinates.append(0)

                zip_code_name.append(str(id))


            count = int(len(coordinates)/3)
        
        zip_code_coordinates += coordinates

        data.append({
            "geometry": {
                "coordinates": [round(item,4) for item in coordinates.copy()],
                "indices": indices.copy()
            }
        })

    outputfile = os.path.join(os.path.dirname(filepath), layerName+'.json') 

    with open(outputfile, "w", encoding="utf-8") as f:
        
        result = {
            "id": layerName,
            "type": "TRIANGLES_3D_LAYER",
            "renderStyle": ["FLAT_COLOR"],
            "styleKey": styleKey,
            "visible": True,
            "selectable": False,
            "skip": False,
            "data": data
        }

        types = []
        dataTypes = []

        if('coordinates' in result['data'][0]['geometry']):
            types.append("coordinates")
            dataTypes.append("d")

        if('normals' in result['data'][0]['geometry']):
            types.append("normals")
            dataTypes.append("f")

        if('indices' in result['data'][0]['geometry']):
            types.append("indices")
            dataTypes.append("I")

        if('ids' in result['data'][0]['geometry']):
            types.append("ids")
            dataTypes.append("I")

        break_into_binary(os.path.dirname(filepath), layerName, result, types, dataTypes)

        layer_json_str = str(json.dumps(result))
        f.write(layer_json_str)

    loaded_shp['id'] = objectId

    coordinates_gdf = gpd.GeoDataFrame({'geometry': coordinates_geometries, "id": coordinates_ids}, crs=3395)

    output_abstract = {"id": "zipName", "coordinates": [round(item,4) for item in zip_code_coordinates], "values": zip_code_name}

    with open(os.path.join(os.path.dirname(filepath), 'zipName.json') , "w", encoding="utf-8") as f:
        
        output_str = str(json.dumps(output_abstract))
        f.write(output_str)

    return {'objects': loaded_shp, 'coordinates': coordinates_gdf, 'coordinates3d': None}