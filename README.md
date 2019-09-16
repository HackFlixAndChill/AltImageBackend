# Web Accessibility Backend

## Description
Sitting behind an AWS API Gateway, our Lambda function accepts a URL and returns a dictionary of the alt texts for all of the images at the given URL.

## Architecture
![technology stack diagram of our web accessibility technology including services like AWS and Azure](/techstack.jpg)

We utilized AWS's API Gateway to communicate with our AWS Lambda computational unit. The Lambda function is responsible for generating the alt text for the image. This utilizes Azure's Computer Vision API to do so. Although computationally expensive, our software is heavily optimized and implements a 2-layer cache system, with the 1st layer as warm Lambda storage and the 2nd layer as AWS DynamoDB. In this way, once a page's alt texts have been generated and cached once, any users of the page will effectively instantly have access to them. Very little data is passed between the client & API Gateway (only a URL and a dictionary of alt texts), meaning that alt texts will (generally) be available before the images actually load. Thus, it also benefits people with limited internet access.
