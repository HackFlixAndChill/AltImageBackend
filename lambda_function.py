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
    
    alt_tags = all_alt_tags(website_url)
    print("ALL ALT TAGS: ", alt_tags)
    
    return {
        'statusCode': 200,
        'body': json.dumps({
            'alt_img_tags': alt_tags
         })
    }
