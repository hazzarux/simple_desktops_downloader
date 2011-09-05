# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


####################################### IMPORTS
import re
import urllib2, urllib
import time
####################################### IMPORTS

####################################### VARIABLES
browselist=["http://simpledesktops.com/browse/"]
introlinks=[]
filelinks=[]
dict_files={}
####################################### VARIABLES

####################################### FUNCTIONS
def get_html(url): #get the html source of a body
        response = urllib2.urlopen(url)
        html = response.read()
        return html

def find_all_links(html): #look up all links in a html source
        linklist = re.findall('<a href="(.*?)">',html)
        return linklist

def add_main_url(relative):
        relative="http://simpledesktops.com"+relative
        return relative

def define_image_extension(link):
        source=get_html(link)
        extension=".x"
        if "\xFF\xD8" in source:
                extension=".jpg"
        if "\x89PNG\r\n\x1A\n" in source:
                extension=".png"
        return extension

def get_html_2(url): #uses urllib instead of urllib2
	response = urllib.urlopen(url)
	html = response.read()
	response.close()
	return html

def get_last_page():
	i = 1
	count = 2
	while (i == 1):
		url="http://simpledesktops.com/browse/"+str(count)+"/"
		print "checking "+url
		body=get_html_2(url)
		if "simply not here" in body:
			break
		if not "simply not here" in body:
			count=count+1
	count=count-1
	return count
####################################### FUNCTIONS

start=time.time()

last_page=get_last_page()

for i in range(2, last_page):
	browse_link="http://simpledesktops.com/browse/"+str(i)+"/"
	print "adding "+browse_link+" to browselist"
	browselist.append(browse_link)
print browselist
browselist_duration=time.time()-start

print "created browselist","(",browselist_duration,"sec)"

for link in browselist:
        html = get_html(link)
        linkslist = find_all_links(html)
        for linkl in linkslist:
                if "desktops" in linkl:
                        linkl = add_main_url(linkl)
                        if linkl not in introlinks:
                                print linkl
                                introlinks.append(linkl)
                        
print introlinks
introlinks_duration=time.time()-start

print "got all introlinks","(",introlinks_duration,"sec)"

for introlink in introlinks:
        intro_html = get_html(introlink)
        filelist = find_all_links(intro_html)
        intro_keyword=introlink.rstrip("/")
        intro_keyword=intro_keyword.split("/")[-1]
        print intro_keyword
        #print filelist
        for filelistlink in filelist:
                if "download" in filelistlink:
                        filelistlink=add_main_url(filelistlink)
                        if filelistlink not in dict_files:
                                print filelistlink
                                dict_files[filelistlink]=intro_keyword

print dict_files
filelinks_duration=time.time()-start
print "got all filelinks","(",filelinks_duration,"sec)"

for link in dict_files:
        extension=define_image_extension(link)
        keyword=dict_files[link]
        output_path="C:\Users\\xoxo\Desktop\img\\"+keyword+extension
        print output_path
        print "downloading "+keyword+extension
        urllib.urlretrieve(link, output_path)