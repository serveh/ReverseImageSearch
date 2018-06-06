import urllib2
import requests
#myproject..: Key 1: c7e8d27cc3214207bbe7c939aad9e06b  Key 2: 9a353aa77dda4eff81a2ca341ea501bb
#bc781e989bd74d55bb8e042c51995e58"  #key2: 4f24b38e2fcf40eaaacc39a9e75a9bbf
#"3aa744deae1241eeab90f67102c15360"  #Key 2: 5c9a08acd00f4ca9b13fdf05dc72baca
subscription_key = "c7e8d27cc3214207bbe7c939aad9e06b"   #"060e528d77b747de83a1e4832a7d6d4d" Key 2: 35ec4bbe2779479dbab4e49c8923567c srweuniversity
assert subscription_key

vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/" #https://westcentralus.api.cognitive.microsoft.com/vision/v2.0
vision_analyze_url = vision_base_url + "analyze"


def reverse_image_search(imageFile, verbose=False):
    bProcessed = True  # A flag to indicate whether the script successfully got the response from Azure server
    with open(imageFile, 'rb') as f:
        img_data = f.read()
    header  = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }
    param   = {'visualFeatures':'Description'} #Categories,Description,Color
    try:
        response = requests.post(vision_analyze_url, headers=header, params=param, data=img_data)
        response.raise_for_status()

        # The 'analysis' object contains various fields that describe the image. The most
        # relevant caption for the image is obtained from the 'descriptions' property.
        analysis = response.json()
        #print(analysis)
        if len(analysis["description"]["captions"]) >0 :
            image_caption = analysis["description"]["captions"][0]["text"].capitalize()
        else:
            image_caption = "NoCaption"
        if len(analysis ["description"]["tags"]) >0:
            image_tag = analysis["description"]["tags"]
        else:
            image_tag = ['NoTags']
    except IOError as err :
        bProcessed = False
        print('Error while processing {}'.format(imageFile))
        print ('HTTP Error: {}, reason: {}.\nRaw error: "{}"'.format(err.response.status_code, err.response.reason, err))
        #print (err)
        image_caption = "InvalidCaption"
        image_tag = ['InvalidTags']

    return image_caption,image_tag, bProcessed


if __name__=="__main__":
    filePath = '/home/srwe/work/project/backstage/apks/com.facebook.orca_v12.0.0.21.14/images/icon_rotate_normal.png'
    #'/home/srwe/work/project/backstage/apks/com.jb.zcamera/images/filter_store_details_share.png' #info_icon.png'
    imageDesc, tags, bStatus = reverse_image_search(filePath, True)
    if bStatus:
        print('The google search term is "{0}"'.format(imageDesc))
    else:
        print('Error processing the requested image: {}'.format(filePath))



# Display the image and overlay it with the caption.
# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
'''
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
image = Image.open(BytesIO(requests.get(image_url).content))
plt.imshow(image)
plt.axis("off")
_ = plt.title(image_caption, size="x-large", y=-0.1)
'''