import os
from lib.exif import Exif
from lib.mapbox_fun import mapbox_reverse


def main():
    cwd = os.getcwd()
    
    os.chdir(os.path.join(cwd, "Images"))
    files = os.listdir()
      
    
    if len(files) == 0:    
        print("You don't have have files in the ./images folder.")    
        exit()
        
    # Loop through the files in the Images directory:

    for file in files:
        file = os.path.join(os.getcwd(),file)
        try:
            # image_path = str(input("ENTER_IMAGE_PATH:"))
            exif = Exif()
            
            exif_data = exif.extract_data(file)
            # print(exif_data)
            if exif_data is not None:
                if 'gps_coords' in exif_data:      
                    result = mapbox_reverse(exif_data['gps_coords']['lat'], exif_data['gps_coords']['lon'])   
                    #POI from Lat Lon             
                    print(f"{file}:{exif_data['gps_coords']}::POI={result['features'][0]['place_name']}")  
                        # 
            
        except IOError:        
            print(f"File format not supported for the given file: {file}") 
    
                                                             
if __name__ == "__main__":
    main()