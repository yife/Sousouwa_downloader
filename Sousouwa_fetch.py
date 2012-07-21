#!/usr/bin/env python
# -*- coding: utf-8 -*-

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
	html = urllib2.urlopen(url).read().decode('sjis')
	soup = BeautifulSoup(html)
	title = soup.find('title')
	body = soup.find("div", attrs={"class": "contents ss"})
	aft = soup.find("div", attrs={"class": "aft"})

	title = unescape(str(title))
	body = unescape(str(body))
	aft = unescape(str(aft))

	title = spaceRemove(title)

	filename = title + '.txt'

	f = open(filename, 'w') # 書き込みモードで開く
	f.write(body) # 引数の文字列をファイルに書き込む
	f.close() # ファイルを閉じる
 
if __name__ == '__main__':
	main()