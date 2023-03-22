import boto3


def Image_annotation_aws(image_file_path):
    # Initialize AWS clients
    try:
        s3_client = boto3.client('s3')
        rekognition_client = boto3.client('rekognition')

        # Define S3 bucket name and image file path
        bucket_name = 'imagerekobucket9490913'
        # image_file_path = 'C:/Users/bhanu/programming/Image_Recognition/Images/jovyn-chamb-iWMfiInivp4-unsplash.jpg'
        file = image_file_path.split('/')[-1]
        # Upload image to S3 bucket
        with open(image_file_path, 'rb') as f:
            s3_client.upload_fileobj(f, bucket_name, file)

        # Detect location in the image using Rekognition
        response = rekognition_client.detect_labels(
            Image={
                'S3Object': {
                    'Bucket': bucket_name,
                    'Name': file,
                },
            },
            MaxLabels=1000,
            MinConfidence=80,
        )

        # print(response)
        # Print detected location information

        for label in response['Labels']:

            for label_l in label['Categories']:
            
                if 'Popular Landmarks' in label_l['Name']:              # and label['Name'] != 'Landmark':
                    print('Detected landmark in the Image:', label['Name'])
            #         for instance in label['Instances']:
            #             print(instance['Landmark']['Type'], ':', instance['BoundingBox'])

                    return response



        # file_obj = open("MyFile.txt","a")
        # file_obj.writelines(str(response['Labels']))
        # # file_obj.writelines(response.content)
        # file_obj.close()

    except Exception as e:        
                print(f"File format not supported for the given file:") 