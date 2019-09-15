from botocore.vendored import requests
import json
import os
import get_img_srcs

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

def get_classification(url):
    body = {"url": url}
    response = requests.post(URL,
                                data=json.dumps(body),
                                params=VISION_PARAMS,
                                headers=VISION_HEADERS)
    description = response.json()["description"]
    if len(description["captions"]) != 0:
        return sorted(description["captions"], key=lambda x: x["confidence"], reverse=True)[0]["text"]
    elif len(description["tags"]) != 0:
        return description["tags"][0]
    else:
        return "No tag available"


def all_alt_tags(site_url):
    img_srcs = get_img_srcs.get_img_srcs(site_url)
    print(img_srcs)
    return { key: get_classification(image_url) for key, image_url in img_srcs.items()}
