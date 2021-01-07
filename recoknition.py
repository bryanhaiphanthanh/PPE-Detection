from utils import get_rekonition_client, get_s3_client
import json
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import numpy as np
import os
from s3operations import *

color = {0: 'r', 1: 'g', 2:'y'}
def detect_faces(bucket: str, file_name: str) -> dict:
    client = get_rekonition_client()
    response = client.detect_faces(
        Image={
            'S3Object':{
                'Bucket':bucket,
                'Name':file_name
            }
        },
    )
    
    return response

def detect_ppe(bucket: str, file_name: str) -> dict:
    client = get_rekonition_client()
    response = client.detect_protective_equipment(
        Image = {
            "S3Object": {
                "Bucket": bucket,
                "Name": file_name
            }
        },
        SummarizationAttributes = {
            "MinConfidence": 95,
            "RequiredEquipmentTypes": [
                "FACE_COVER"
            ]
        }
    )
    return response
# print(detect_ppe("ohio-rekog", "maskwearingperson.jpg"))

def check_mask(response: dict) -> list:
    #0: no mask, 1: mask, 2: indeterminate
    summary = get_summary(response)
    mask = []
    i = 0
    while i < len(response['Persons']):
        if i in summary['PersonsWithRequiredEquipment']:
            mask.append(2)
        elif i in summary['PersonsWithoutRequiredEquipment']:
            mask.append(0)
        elif i in summary['PersonsIndeterminate']:
            mask.append(1)
        
        i += 1
    return mask

def print_image(response: dict, file_path: str) -> bool:
    #response is a list of bounds from get_persons_bounds_ppe
    try:
        im = np.array(Image.open(file_path), dtype=np.uint8)
        image = Image.open(file_path)
        imWidth, imHeight = image.size
        fig,ax = plt.subplots(1)
        ax.imshow(im)

        #check who has masks
        mask = check_mask(response)

        #print person's bounds
        bounds = get_persons_bounds_ppe(response)
        i = 0
        for bound in bounds:
            height = bound['Height']
            width = bound['Width']
            top = bound['Top']
            left = bound['Left']
            rect = patches.Rectangle((imWidth*left,imHeight*top),imWidth*width,imHeight*height, linewidth=1,edgecolor=color[mask[i]],facecolor='none')
            # print("Person ", i, ":", mask, "---", color[mask[i]])
            ax.add_patch(rect)
            i += 1

        #print mask's bounds
        plt.show()
        return True
    except Exception as ex:
        print(str(ex))
        return False

def get_persons_ppe(response: dict) -> list:
    i = 0
    persons = []
    for person in response['Persons']:
        persons[i] = person
        i += 1
    
    return persons

def get_persons_bounds_ppe(response: dict) -> list:
    #Return a list of dicts
    #format: [{person1's data}, {person2's data}]
    bounds = []
    for person in response['Persons']:
        bounds.append(person['BoundingBox'])
    
    return bounds

def test_complete_ppe_detection(file_path = None) -> bool:
    try:
        file_path, file_name = upload_file_s3(file_path)
        response = detect_ppe("ohio-rekog", file_name)
        delete_file_s3(file_name)

        # print(check_mask(response))
        print_image(response, file_path)
        return True
    except Exception as ex:
        print(str(ex))
        return "fail"

def get_summary(response: dict) -> dict:
    return response['Summary']




print("-------------------------------------------------Start total test-------------------------------------------------")
response = test_complete_ppe_detection()
print(response)
print("--------------------------------------------------End total test--------------------------------------------------")
