import os
import pickle
import time
import PIL
from PIL import Image
import copy
import random
#from reverseImageSearch import google_reverse_image_search
from azureAnalyzeImage import reverse_image_search


def resize_small_image(img, baseSize=50):

    smallImg = img  # open the image file
    # img.verify()
    imageSize = smallImg.size
    minSize = min(imageSize[0], imageSize[1])
    ratio = baseSize / float(minSize)
    s0 = int(float(imageSize[0]) * ratio)
    s1 = int(float(imageSize[1]) * ratio)
    resizedImg = smallImg.resize((s0, s1), PIL.Image.ANTIALIAS)
    return resizedImg
    #resizedImg.save('img2.png')


transactions = 5000
counter=0
d = '/home/srwe/work/project/backstage/apks'
apps = [os.path.join(d, o) for o in os.listdir(d)
        if os.path.isdir(os.path.join(d, o))]
try:
    with open('processedApps.list', 'r') as processedFile:
        processedAppList = pickle.load(processedFile)
except (IOError, SyntaxError) as e:
    processedAppList = []

bStatus = True  # this flags indicate whether server has been accessed successfully
if counter < transactions and bStatus:
    for appDir in apps:
        imageDir = os.path.join(appDir, 'images/')
        if os.path.isdir(imageDir):     # and appDir not in processedAppList:
            try:
                with open(os.path.join(appDir, 'processedImageList.list'), 'r') as imgList:
                    procImageList = pickle.load(imgList)
            except (IOError, SyntaxError) as e:
                procImageList = []

            imageListFile = open(os.path.join(appDir, 'imageListAzure.txt'), 'w')

            for imgfn in os.listdir(imageDir):
                fileName = os.path.join(imageDir, imgfn)
                origFname = copy.deepcopy(fileName)
                if imgfn not in procImageList:
                    try:
                        img = Image.open(fileName)  # open the image file
                        print('processing {0} ...'.format(origFname))
                        #img.verify()    # verify that it is, in fact an image
                        imSz = img.size
                        if imSz[0] < 50 or imSz[1] < 50:    # resize images smaller than 50*50
                            tmp=resize_small_image(img)
                            fileName ='tmpResizedImg.png'
                            tmp.save(fileName)
                        #t = random.uniform(10, 20)
                        time.sleep(3.2)
                        imageCap, imageTags, bStatus = reverse_image_search(fileName) # finding a description for image from google search
                        if bStatus:
                            counter=+1
                            print(counter)
                            print('"{0}"'.format(imageCap.encode('utf-8').strip()))
                            imageListFile.write('\n{}; {}; '.format(imgfn, imageCap.encode('utf-8').strip()))
                            for tag in imageTags:
                                imageListFile.write('{}, '.format(tag.strip()))
                            procImageList.append(imgfn)
                            with open(os.path.join(appDir,'processedImageList.list'), 'w') as imgList:
                                pickle.dump(procImageList, imgList)
                            imageListFile.flush()
                        else:
                            print('Error processing the requested image: {}.\nQuitting the script.'.format(fileName))
                            quit()

                    except (IOError, SyntaxError) as e:
                        print('Bad file:', origFname)

            imageListFile.close()

            processedAppList.append(appDir)
            with open('processedApps.list', 'w') as processedFile:
                pickle.dump(processedAppList, processedFile)
else:
    print("<<<<<<<<<<<<<  process 5000 images >>>>>>>>>>>>>")
    exit(0)
