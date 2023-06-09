from google.cloud import storage
import io
import os
from google.cloud import vision

def vision_annotate(file_name):
    os.environ["GCLOUD_PROJECT"] = "lustrous-stone-381304"

    # Create a client object for interacting with GCP Storage
    client = storage.Client()

    # Define the name of the bucket and file name to upload
    bucket_name = 'imagerekobucket9490913'
    # file_name = 'C:/Users/bhanu/programming/Image_Recognition/Images/pisa.jpg'
    Image_Dir = os.path.dirname(os.path.abspath(file_name))
    os.chdir(Image_Dir)
    # Get the bucket object to upload the file to
    bucket = client.bucket(bucket_name)

    # Create a blob object with the file name to upload
    blob = bucket.blob(file_name)

    file = file_name.split('/')[-1]
    # Upload the image file to GCP Storage
    with open(file, 'rb') as f:
        blob.upload_from_file(f)

    # Fetch the GSUtil URI of the uploaded file
    file_name = 'gs://{}/{}'.format(bucket_name, file)

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Loads the image into memory
    with io.open(file, 'rb') as image_file:
        content = image_file.read()
    image = vision.Image(content=content)

    # Performs landmark detection on the image
    response = client.landmark_detection(image=image)

    landmarks = response.landmark_annotations
    
    landmark_labels = []
    cnt = 0
    for landmark in landmarks:
        print(landmark)
        print(landmark.description)
        print(landmark.locations)
        print(landmark.score)
        landmark_labels.append([{"label":landmark.description, "location":landmark.locations, "score":landmark.score}])
        cnt = cnt+1

    return landmark_labels