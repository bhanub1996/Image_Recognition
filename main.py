import os
import csv
from lib.exif import Exif
from lib.mapbox_fun import mapbox_reverse, mapbox_forward
from lib.gcp_vision import vision_annotate 
from lib.aws_rekognition import Image_annotation_aws


def main():
    cwd = os.getcwd()
    
    os.chdir(os.path.join(cwd, "Images"))
    files = os.listdir()
      
    
    if len(files) == 0:    
        print("You don't have have files in the ./images folder.")    
        exit()

    dict_label = {'file':'', 'Coords from Exif': '', 'POI': '', 'gcp_vision_annotation':'','aws_rekognition_label':''}
    csv_file_name = 'image_labelling.csv'
    fieldnames = dict_label.keys()

    with open(csv_file_name, 'w', newline='') as csvfile:
    
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        
    # Loop through the files in the Images directory:

        for file in files:
            file = os.path.join(os.getcwd(),file)
            try:
                # image_path = str(input("ENTER_IMAGE_PATH:"))
                exif = Exif()
                dict_label = {'file':file, 'Coords from Exif': '', 'POI': '','gcp_vision_annotation':'','aws_rekognition_label':''}
                exif_data = exif.extract_data(file)
                # print(exif_data)
                if exif_data is not None:
                    if 'gps_coords' in exif_data:      
                        result = mapbox_reverse(exif_data['gps_coords']['lat'], exif_data['gps_coords']['lon'])   
                        #POI from Lat Lon             
                        print(f"{file}:{exif_data['gps_coords']}::POI={result['features'][0]['place_name']}")
                        # result = mapbox_forward(result['features'][0]['place_name'])  
                        # print(result)

                        
                        dict_label['Coords from Exif']=exif_data['gps_coords']
                        dict_label['POI']=result['features'][0]['place_name']

                vision_response=vision_annotate(file)
                dict_label['gcp_vision_annotation']=vision_response

                aws_response = Image_annotation_aws(file)
                dict_label['aws_rekognition_label']=aws_response
                    
                    # dict_label['Exif_Data']=exif_data
                writer.writerow(dict_label)
                
                
            except IOError:        
                print(f"File format not supported for the given file: {file}") 
    
main()                                                            
# print(vision_annotate())
# print(Image_annotation_aws())

