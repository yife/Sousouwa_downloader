#!/usr/bin/env python
# -*- coding: utf-8 -*-

import codecs
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def removeSpaceEntity(s):
    pattern = re.compile('(&#160;|&ensp;|&emsp;)')
    return pattern.sub('', s)

def convertEntity(s):
	pattern = re.compile('(&#([0-9a-fA-F]{4});)')
	return pattern.sub(lambda x: unichr(int(x.group(2), 16)), s)

def brRemove(s):
	brRemover = re.compile(r'<br.*?>')
	return brRemover.sub('', s)

def divRemove(s):
	divRemover = re.compile(r'(<div.*?>|</div>)')
	return divRemover.sub('', s)

def tagRemove(s):
	tagRemover = re.compile(r'(<.*?>|</.*?>)')
	return tagRemover.sub('', s)

def spaceRemove(s):
	spaceRemover = re.compile(r'( |　|	|\n)')
	return spaceRemover.sub('', s)

def unescape(s):
	s = removeSpaceEntity(s)
	s = convertEntity(s)
	s = tagRemove(s)
	return s

def main():
	argvs = sys.argv
	url = sys.argv[1]
	# url = 'http://coolier-new.sytes.net:8080/sosowa/ssw_l/?mode=read&key=1342594292&log=0'
	html = urllib2.urlopen(url).read().decode('cp932')
	soup = BeautifulSoup(html)
	title = soup.find('title')
	body = soup.find("div", attrs={"class": "contents ss"})
	aft = soup.find("div", attrs={"class": "aft"})

	title = unescape(str(title))
	body = unescape(str(body))
	aft = unescape(str(aft))

	title = spaceRemove(title)

	filename = title + '.html'

	htmlWrapBefore = '<?xml version="1.0" encoding="Shift_JIS"?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja" ><body><pre>'
	htmlWrapAfter = "</pre></body></html>"

	sjisWriter = codecs.open(filename, 'w', 'cp932')
	sjisWriter.write(htmlWrapBefore)
	sjisWriter.write(body) # 引数の文字列をファイルに書き込む
	sjisWriter.write(htmlWrapAfter)

 
if __name__ == '__main__':
	main()