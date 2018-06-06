
from PIL import Image
from os import listdir
from os.path import splitext


fil='/home/srwe/Desktop/wic_big_rain.webp'

target_directory = '.'
imageTypes = ['.png', '.jpg', '.jpeg', '.bmp']
target = '.png'

filename, extension = splitext(fil)
extension = extension.lower()
try:
    if extension not in ['.py', target]:
        im = Image.open(filename + extension)
        im.save(filename + target)
except OSError:
    print('Cannot convert %s' % file)

    '''
    try:

        im = Image.open(fileName).convert("RGB")
        im.save(fileName, "jpeg")

    except (IOError, SyntaxError, ZeroDivisionError) as e:
        print('Bad file:', file)

        tmp = resize_small_image(img)
        fileName = 'tmpResizedImg.png'
        tmp.save(fileName)
    '''