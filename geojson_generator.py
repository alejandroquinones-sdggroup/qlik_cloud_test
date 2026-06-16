import json
import os

def generate_hq_geojson(lat, lon, base_geojson=None, filename="headquarters.geojson"):
    """
    Generates HQ building parts and appends them to base_geojson if provided.
    If base_geojson is None, it initializes a new FeatureCollection.
    """
    # 1. Initialize or use the provided GeoJSON object
    if base_geojson is None:
        geojson_data = {
            "type": "FeatureCollection",
            "features": []
        }
    else:
        geojson_data = base_geojson

    # Relative offsets (Grounded wings + raised windows)
    building_parts = [
        {"type": "body", "offset": [[0.0, 0.005], [0.003, 0.005], [0.003, 0.0], [0.0, 0.0], [0.0, 0.005]]},
        {"type": "body", "offset": [[-0.0007, 0.003], [0.0, 0.003], [0.0, 0.0], [-0.0007, 0.0], [-0.0007, 0.003]]},
        {"type": "body", "offset": [[0.003, 0.003], [0.0037, 0.003], [0.0037, 0.0], [0.003, 0.0], [0.003, 0.003]]},
        {"type": "window", "offset": [[0.0004, 0.004], [0.0007, 0.004], [0.0007, 0.0015], [0.0004, 0.0015], [0.0004, 0.004]]},
        {"type": "window", "offset": [[0.0013, 0.004], [0.0016, 0.004], [0.0016, 0.0015], [0.0013, 0.0015], [0.0013, 0.004]]},
        {"type": "window", "offset": [[0.0024, 0.004], [0.0027, 0.004], [0.0027, 0.0015], [0.0024, 0.0015], [0.0024, 0.004]]}
    ]

    for part in building_parts:
        abs_coords = [[lon + x, lat + y] for x, y in part["offset"]]
        
        is_window = part["type"] == "window"
        properties = {
            "fill": "#2C3E50" if is_window else "#808080",
            "fill-opacity": 0.9 if is_window else 0.7,
            "stroke": "#000000",
            "stroke-width": 1
        }

        # Append directly to the geojson_data features list
        geojson_data["features"].append({
            "type": "Feature",
            "properties": properties,
            "geometry": {
                "type": "Polygon",
                "coordinates": [abs_coords]
            }
        })

    # Save to current directory
    file_path = os.path.join(os.getcwd(), filename)
    with open(file_path, 'w') as f:
        json.dump(geojson_data, f, indent=2)
    
    return geojson_data

# Example of looping through multiple coordinates:
if __name__ == "__main__":
    locations = [
        (36.704872, -4.421733), # Málaga
        (40.4505, -3.6898),     # Madrid Bernabéu
        (40.4193, -3.6931)      # Madrid Cibeles
    ]
    
    current_geojson = None
    
    for lat, lon in locations:
        current_geojson = generate_hq_geojson(lat, lon, base_geojson=current_geojson)
    
    print(f"Generated {len(locations)} buildings in headquarters.geojson")