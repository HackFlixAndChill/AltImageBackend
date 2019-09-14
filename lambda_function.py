import json

from image_to_text import all_alt_tags

def getURL(request):
    """Return URL
    """
    return json.loads(request['body'])['URL']

def lambda_handler(event, context):
    # TODO implement
    print("Event: ", event)
    print("Context: ", context)
    
    website_url = getURL(event)
    print("Website URL: ", website_url)
    
    return {
        'statusCode': 200,
        'body': {
            'alt_img_tags': all_alt_tags(website_url)
         }
    }
