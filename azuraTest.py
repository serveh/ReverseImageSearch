import requests

subscription_key = "bc781e989bd74d55bb8e042c51995e58"  #key2: 4f24b38e2fcf40eaaacc39a9e75a9bbf
assert subscription_key

vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/" #https://westcentralus.api.cognitive.microsoft.com/vision/v1.0
vision_analyze_url = vision_base_url + "analyze"

filePath = '/home/srwe/work/project/backstage/apks/com.whatsapp/images/icon.png'
with open(filePath, 'rb') as f:
    img_data = f.read()
header  = {
    'Content-Type': 'application/octet-stream',
    'Ocp-Apim-Subscription-Key': subscription_key,
}
param   = {'visualFeatures': 'Description'} #Categories,Description,Color
response = requests.post(vision_analyze_url, headers=header, params=param, data=img_data)
response.raise_for_status()

# The 'analysis' object contains various fields that describe the image. The most
# relevant caption for the image is obtained from the 'descriptions' property.
analysis = response.json()

image_caption = analysis["description"]["captions"][0]["text"].capitalize()
image_tag = analysis["description"]["tags"]


print('The google search term is "{0}"'.format(image_caption))

