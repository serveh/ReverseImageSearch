import webbrowser
import requests
import urllib2
from bs4 import BeautifulSoup
import re

def get_soup(url):
    enurl = url.replace('/www.google.com/search?', '/www.google.com/search?hl=en-GB&')
    response = requests.get(enurl, headers={
        "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"})
    html = response.content

    soup = BeautifulSoup(html, "html.parser")
    return soup

def google_reverse_image_search(imageFile, verbose=False):
    searchUrl = 'http://www.google.com/searchbyimage/upload'
    multipart = {'encoded_image': (imageFile, open(imageFile, 'rb')), 'image_content': ''}
    response = requests.post(searchUrl, files=multipart, allow_redirects=False)
    fetchUrl = response.headers['Location']
    # now convert into text by parsing google results
    soup = get_soup(fetchUrl)
    noDesc = soup.find_all(text=re.compile('Tip: Try entering a descriptive word in the search box.'))
    if len(noDesc) > 0:
        imageDesc = 'NoDescriptionFound'
    else:
       elementFound = soup.find_all('a', {'class': 'fKDtNb'})  # text=re.compile('Best guess for this image:.*'))
       imageDesc = elementFound[0].contents[0]
    if verbose:
        webbrowser.open(fetchUrl)  # to open the url in a browser
    return imageDesc


if __name__=="__main__":
    filePath = '/home/srwe/work/project/backstage/apks/com.dianxinos.dxbs_v3.8.5/images/dxad_ad_title_icon.png' #info_icon.png'
    imageDesc=google_reverse_image_search(filePath, True)
    print('The google search term is "{0}"'.format(imageDesc))

#<div class="card-section" style="margin:0 0 16px">  soup.find_all("div", class_="stylelistrow")
#iamde_ic_action_interrogare_refresh.png    ic_contact_phone_black.png