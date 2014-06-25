from bs4 import BeautifulSoup
from urllib2 import urlopen
import datetime
import urllib2, cookielib
from appscript import app, mactypes
import urllib
import os
import subprocess
import time
from PIL import Image
import signal
import struct
from array import array
#import httplib

#httplib.HTTPConnection.debuglevel = 1

init_url = "http://www.gocomics.com/"

hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}

SCRIPT = """/usr/bin/osascript<<END
	tell application "Finder"
	set desktop picture to POSIX file "%s"
	end tell
	END"""

path = "/Users/timothyling/Desktop/comics"

def get_strip(comic_name):
	date = get_date()
	url = init_url+comic_name+"/"+date
	req = urllib2.Request(url,headers=hdr)
	try:
		html_obj = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		print e.fp.read()
	content = html_obj.read()
	soup_obj = BeautifulSoup(content,"lxml")
	locate_div = soup_obj.find("p","feature_item")
	web = locate_div.img["src"]
	return web 

def download_pic(url, counter):
	temp = "daily" + str(counter) + ".jpg"
	os.chdir(path)
	image = urllib.URLopener()
	image.retrieve(url, temp)
	counter += 1


def set_pic(filename):
	print filename
	proc = subprocess.Popen(SCRIPT%filename, stdout=subprocess.PIPE, shell=True, preexec_fn=os.setsid)
	os.killpg(proc.pid, signal.SIGTERM)

def get_date():
	today = datetime.date.today()
	year = today.year
	month = today.month
	if month < 10:
		month = "0" + str(month)
	day = today.day
	if day < 10:
		day = "0" + str(day)
	date = str(year) + "/" + str(month) + "/" + str(day)
	return date 

def comic_list():
	counter = 1
	file_obj = open("comic_list.txt","r")
	for name in file_obj:
		url = get_strip(name.strip())
		download_pic(url,counter)
		counter += 1

def stitch_comics():
	counter = 1
	x_coord = 0
	y_coord = 200
	new_im = Image.new("RGB",(1200,1152))
	
	for num in range(0,4):
		temp = "daily" + str(counter) + ".jpg"
		im = Image.open(temp)
		a = im.size
		new_im.paste(im,(x_coord,y_coord))
		int1 = a[1]
		b = int1
		y_coord += b
		counter += 1
	
	x_coord = 600
	y_coord = 200
	
	for num in range (4,6):
		temp = "daily" + str(counter) + ".jpg"
		im = Image.open(temp)
		a = im.size
		new_im.paste(im,(x_coord,y_coord))
		int1 = a[1]
		b = int1
		y_coord += b
		counter += 1
	new_im.save("sunday.jpg")
	

comic_list()
stitch_comics()
filename = path + "/sunday.jpg"
set_pic(filename)




