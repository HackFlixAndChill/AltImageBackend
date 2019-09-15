from botocore.vendored import requests
import json
import os
import get_img_srcs
from base64 import b64decode
import re
import boto3
import time

dynamodb = boto3.client('dynamodb')

MS_VISION_ENDPOINT = "hackmitvision.cognitiveservices.azure.com"
MS_VISION_KEY = os.environ.get("MS_VISION_KEY")
URL = "https://{endpoint}/vision/v2.0/analyze".format(endpoint=MS_VISION_ENDPOINT)

VISION_HEADERS = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': MS_VISION_KEY,
}


VISION_PARAMS = {
    "visualFeatures": "Description",
}

def bytes_to_img(imageBytes):
    # sub out the damn metadata
    imgdata = re.sub('^data:image/.+;base64,', '', imageBytes)

    # decode bytes
    imgdata = b64decode(imgdata)

    return imgdata

def get_classification(url):
    headers = {
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': MS_VISION_KEY,
    }
    print( re.match('^data:image/.+;base64.*', url))
    if re.match('^data:image/.+;base64.*', url):
        body = bytes_to_img(url)
        headers["Content-Type"] = 'application/octet-stream'
    else:
        body = json.dumps({"url": url})
    
    response = requests.post(URL,
                                data=body,
                                params=VISION_PARAMS,
                                headers=headers).json()
    if "description" not in response:
        return "No tag available"

    description = response["description"]
    if len(description["captions"]) != 0:
        return sorted(description["captions"], key=lambda x: x["confidence"], reverse=True)[0]["text"]
    elif len(description["tags"]) != 0:
        return description["tags"][0]
    else:
        return "No tag available"

local_cache = {}
def get_description(url):
    description = get_classification(url)
    dynamodb.put_item(TableName='imageDescriptions', Item={'imageId':{'S':url},
                    'description':{'S':description}, 
                    'ttl':{'N':str(int(time.time())+60*60*6)}})
    local_cache[url] = description
    return description
        
def batch_request(batch_items):
    print("dynamo cache request made")
    print(batch_items)
    descriptions = {}
    response = dynamodb.batch_get_item(RequestItems={'imageDescriptions': {'Keys': batch_items}})
    print(response)
    for item in response["Responses"]["imageDescriptions"]:
        descriptions[item["imageId"]["S"]] = item["description"]["S"]
    return descriptions
        
        
        

def all_alt_tags(site_url):
    img_srcs = get_img_srcs.get_img_srcs(site_url)
    descriptions = {}
    remaining = []
    for key in img_srcs:
        if key in local_cache:
            descriptions[key] = local_cache[key]
        else:
            remaining.append(key)
    
    # descriptions = {}
    batch_items = []
    for key in remaining:
        batch_items.append({'imageId':{'S':key}})
        if len(batch_items) == 100:
            dynamo_cache = batch_request(batch_items)
            local_cache.update(dynamo_cache)
            descriptions.update(dynamo_cache)
            batch_items = []
    if len(batch_items) != 0:
        dynamo_cache = batch_request(batch_items)
        local_cache.update(dynamo_cache)
        descriptions.update(dynamo_cache)
        
    total = set(key for key in img_srcs)
    remaining = total - set(descriptions.keys())
    
    remaining_descriptions = { key: get_description(key) for key in remaining}
    descriptions.update(remaining_descriptions)
    print(img_srcs)
    return descriptions