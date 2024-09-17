import os
import arcpy

# Print current working directory
print("Current working directory:", os.getcwd())

# Check if file exists
shapefile_path = os.path.join(os.getcwd(), "no_retail.shp")
print("Shapefile exists:", os.path.exists(shapefile_path))

# Run the Buffer tool
arcpy.analysis.Buffer(
    in_features="no_retail.shp",
    out_feature_class="./retail_buffer.shp",
    buffer_distance_or_field="500 Meters",
    line_side="FULL",
    line_end_type="ROUND",
    dissolve_option="NONE",
    dissolve_field=None,
    method="PLANAR"
)
