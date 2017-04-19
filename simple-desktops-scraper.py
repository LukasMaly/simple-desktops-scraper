"""
    Python 3 scraper for 'Simple Desktops'
    MIT License
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
    THE SOFTWARE.
    
"""

import sys, requests, os
from bs4 import BeautifulSoup

# This is where the files are hosted
rooturl= "http://simpledesktops.com"

# Set up Arrays
urls = []
downloadurls = []

"""
    0. define directory
    1. get urls (will ask for indices)
    2. get download urls (pass in urls)
    3. download files (pass in download urls)
    
    This is for downloading the desktop images from simpledesktops.com
    the script takes two inputs, to dictate at which index 
        the snatcher will start and end snatching files.
        
    If unsure, pass in 1 and 3 to the input
    
"""

# Define Functions

def get_urls(): # y = limit of pages, x = start index
    urls =[]                     
    x = int(input(" Select beginning range. Enter '1' for the very beginning: \n "))
    y = int(input(" Select the final page to search:\n "))
    op_commence = ' Operation commencing'
    print(op_commence)
    for z in range(x, y):
        address = rooturl + "/browse/" + str(z)
        r = requests.get(address)
        soup = BeautifulSoup(r.text, 'html.parser')
        # The desktop div links to the various images
        backgrounds = soup.find_all("div", {"class":"desktop"})
        for background in backgrounds:
            link = background.find("a")
            url = rooturl + link["href"]
            urls.append(url)
    return urls

def get_download_urls(urls):
    downloadurls = []
    for url in urls:
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html.parser')
        # Again, the desktop div, links to the download url
        background = soup.find("div", {"class":"desktop"})
        downloadurl = background.find("a")
        downloadurl = rooturl + downloadurl['href']
        downloadurls.append(downloadurl)
    return downloadurls
    
def download_file(downloadurl):
    x = downloads.index(downloadurl)
    filename = '/'.join(urls[x].split('/')[-5:-2])
    path = os.path.join(directory, filename)
    if not os.path.exists(path):
        os.makedirs(path)
    path = path + '/' + urls[x].split('/')[-2] + '.png' 
    # Second to last index is the file name, matching
    # the two url arrays
    r = requests.get(downloadurl, stream=True)
    # MUST HAVE the stream=True parameter
    with open(path, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
    return filename # Why am I returning filename?

def download_files(downloadurls):
    for url in downloadurls:
        download_file(url)

# Init Script        
creating_dir = ' Directory: '  
prep_op = '\n Preparing Operation\n'
prep_op_2 = '\n Primary urls retrieved, getting download links\n'
op = '\n Downloads beginning\n'
success = '\n Your files have been downloaded successfully!\nTry again with a different index'

directory = input(' Select directory to save files into,\n \
if directory doesn\'t exit, it will be \
created: \n ')  
print(creating_dir + directory)
if not os.path.exists(directory):
    os.makedirs(directory)
directory = directory + "/" # is Path

# Feedback Messages
print(prep_op)        
urls = get_urls()
print(prep_op_2)
downloads = get_download_urls(urls)
print(op)
download_files(downloads)
print(success)
