import arcpy
import os
import ee
import pandas as pd


#example usage: python Project2.py r'C:\Users\smirhe1\Documents\ShabnamDoc\Documents\LSU\Semesters\Fall2024\GISProgrammingGEOG4057\Finalprojects\project2edit' boundary.csv pnt_elve1 32119

def getGeeElevation(workspace, csv_file, outfc_name, epsg=4326):
    
    """
    workspace: directory that contains inputs and outputs
    csv_file : input csv filename
    outfc_name : output shape filename
    epsg : wkid code for spatial reference, e.g. 4326 for WGS GSC

    """
    csv_file = os.path.join(workspace, csv_file)
    
    data = pd.read_csv(csv_file)
    dem = ee.Image('USGS/3DEP/10m')
    print(epsg)
    geometry = [ee.Geometry.Point([x, y], f'EPSG:{epsg}') for x, y in zip(data['X'], data['Y'])]
    fc = ee.FeatureCollection(geometry)
    origin_info = fc.getInfo()
    sampled_fc = dem.sampleRegions(collection=fc, scale=10, geometries=True)
    sampled_info = sampled_fc.getInfo()
    for ind ,item in enumerate(origin_info['features']):
        item['properties'] = sampled_info['features'][ind]['properties']
    
    fcname = os.path.join(workspace, outfc_name)
    if arcpy.Exists(fcname):
        arcpy.management.Delete(fcname)
    arcpy.management.CreateFeatureclass(workspace, outfc_name, geometry_type='POINT', spatial_reference=epsg)
    arcpy.management.AddField(fcname, field_name='elevation', field_type='FLOAT')
    with arcpy.da.InsertCursor(fcname, ['SHAPE@', 'elevation']) as cursor:
        for feat in origin_info['features']:
            # get the coordinates and convert a point geometry
            coords = feat['geometry']['coordinates']
            pnt = arcpy.PointGeometry(arcpy.Point(coords[0], coords[1]), spatial_reference=32119)
            # get the properties and write it to elevation
            elev = feat['properties']['elevation']
            cursor.insertRow((pnt, elev))
    

def main():
    import sys
    
    try:
        ee.Initialize(project='ee-shmirheidarian')
    except:
        ee.Authenticate()
        ee.Initialize(project='ee-shmirheidarian')

    # Set default values in case no arguments are provided
    if len(sys.argv) < 5:
        workspace = r'C:\Users\smirhe1\Documents\ShabnamDoc\Documents\LSU\Semesters\Fall2024\GISProgrammingGEOG4057\Finalprojects\project2edit'
        csv_file = 'boundary.csv'
        outfc_name = 'pnt_elve1'
        epsg = 32119
    else:
        workspace = sys.argv[1]
        csv_file = sys.argv[2]
        outfc_name = sys.argv[3]
        epsg = int(sys.argv[4])

    getGeeElevation(workspace=workspace, csv_file=csv_file, outfc_name=outfc_name, epsg=epsg)

          

if __name__ == '__main__':
    main()
