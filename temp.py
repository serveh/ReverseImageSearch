import os
import pickle
from PIL import Image
import time
from azureAnalyzeImage import google_reverse_image_search

imageDir = '/home/srwe/work/project/backstage/apks/com.vertaler.deen/images/'
imageListFile = open(os.path.join(imageDir, 'imageList.txt'), 'w')
for imgfn in os.listdir(imageDir):
        file = os.path.join(imageDir, imgfn)
        try:
            img = Image.open(file)  # open the image file
            img.verify()  # verify that it is, in fact an image
            imSz = img.size
            if imSz[0] > 49 and imSz[1] > 49:
                print('processing {0} ...'.format(file))
                imageCap, imageTags= google_reverse_image_search(file) # finding a description for image from google search
                print('"{0}"'.format(imageCap.encode('utf-8').strip()))
                imageListFile.write('\n{}; {}; '.format(imgfn, imageCap.encode('utf-8').strip()))
                for tag in imageTags:
                    imageListFile.write('{}, '.format(tag.strip()))
        except (IOError, SyntaxError) as e:
            print('Bad file:', file)

imageListFile.close()
