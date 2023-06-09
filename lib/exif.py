import os
from PIL import Image
from PIL.ExifTags import (
    GPSTAGS,
    TAGS
)


class Exif:
    def convert_decimal_degrees(self, degree, minutes, seconds, direction):
        """
        Converting to decimal degrees for latitude and longitude.
        """
        decimal_degrees = degree + minutes / 60 + seconds / 3600
        # A value of "S" for South or West will be multiplied by -1
        if direction == "S" or direction == "W":
            decimal_degrees *= -1
        return decimal_degrees

    def create_google_maps_url(self, gps_coords: dict) -> str:
        """
        Process Google Maps Link.
        """
        dec_deg_lat = self.convert_decimal_degrees(
            float(gps_coords["lat"][0]),
            float(gps_coords["lat"][1]),
            float(gps_coords["lat"][2]),
            gps_coords["lat_ref"]
        )
        dec_deg_lon = self.convert_decimal_degrees(
            float(gps_coords["lon"][0]),
            float(gps_coords["lon"][1]),
            float(gps_coords["lon"][2]),
            gps_coords["lon_ref"]
        )
        return f"https://maps.google.com/?q={dec_deg_lat},{dec_deg_lon}"

    def extract_data(self, image_path: str) -> dict:
        """
        Extract all Exif data from image.
        """
        if not os.path.exists(image_path):
            return None
        data = {}
        gps_coords = {}
        image = Image.open(image_path)
        if not image._getexif():
            return None
        for tag, value in image._getexif().items():
            tag_name = TAGS.get(tag)
            if tag_name == "GPSInfo":
                for key, val in value.items():
                    data[GPSTAGS.get(key)] = val
                    if GPSTAGS.get(key) == "GPSLatitude":
                        gps_coords["lat"] = val
                    elif GPSTAGS.get(key) == "GPSLongitude":
                        gps_coords["lon"] = val
                    elif GPSTAGS.get(key) == "GPSLatitudeRef":
                        gps_coords["lat_ref"] = val
                    elif GPSTAGS.get(key) == "GPSLongitudeRef":
                        gps_coords["lon_ref"] = val   
            else:
                data[tag_name] = value
        
        if gps_coords:
            data['gps_coords']={"lat":self.convert_decimal_degrees(float(gps_coords["lat"][0]), float(gps_coords["lat"][1]), float(gps_coords["lat"][2]), gps_coords["lat_ref"]),"lon":self.convert_decimal_degrees(float(gps_coords["lon"][0]), float(gps_coords["lon"][1]), float(gps_coords["lon"][2]), gps_coords["lon_ref"])}
            # print(data['gps_coords'])
            data["GoogleMapsUrl"] = self.create_google_maps_url(gps_coords)
        return data
    
    