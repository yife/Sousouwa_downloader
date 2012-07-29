#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import htmlentitydefs
import codecs
import urllib2
from BeautifulSoup import BeautifulSoup
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# 実体参照 & 文字参照を通常の文字に戻す
def htmlentity2unicode(text):
    # 正規表現のコンパイル
    reference_regex = re.compile(u'&(#x?[0-9a-f]+|[a-z]+);', re.IGNORECASE)
    num16_regex = re.compile(u'#x\d+', re.IGNORECASE)
    num10_regex = re.compile(u'#\d+', re.IGNORECASE)
     
    result = u''
    i = 0
    while True:
        # 実体参照 or 文字参照を見つける
        match = reference_regex.search(text, i)
        if match is None:
            result += text[i:]
            break
         
        result += text[i:match.start()]
        i = match.end()
        name = match.group(1)
         
        # 実体参照
        if name in htmlentitydefs.name2codepoint.keys():
            result += unichr(htmlentitydefs.name2codepoint[name])
        # 文字参照
        elif num16_regex.match(name):
            # 16進数
            result += unichr(int(u'0'+name[1:], 16))
        elif num10_regex.match(name):
            # 10進数
            result += unichr(int(name[1:]))
 
    return result

def removeSpaceEntity(s):
    pattern = re.compile('(&#160;|&ensp;|&emsp;)')
    return pattern.sub('', s)

def convertEntity(s):
	pattern = re.compile('(&#([0-9a-fA-F]{4});)')
	return pattern.sub(lambda x: unichr(int(x.group(2), 16)), s)

def convertSousouwaEntity(s):
	pattern = re.compile(r'&amp;#039;')
	tmp = pattern.sub('\'', s)
	pattern = re.compile(r'&#039;')
	tmp = pattern.sub('\'', s)
	return tmp

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
	spaceRemover = re.compile(r'^( |　|	|\n)+')
	tmp = spaceRemover.sub('', s)
	spaceRemover = re.compile(r'( |　|	|\n)+$')
	return spaceRemover.sub('', tmp)

def unescape(s):
	s = removeSpaceEntity(s)
	s = convertEntity(s)
	s = tagRemove(s)
	return s

def titleEscape(s):
	s = tagRemove(s)
	s = spaceRemove(s)
	s = convertEntity(s)
	s = convertSousouwaEntity(s)
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

	# title = unescape(str(title))
	body = unescape(str(body))
	aft = unescape(str(aft))
	title = titleEscape(str(title))

	#書き出す先のフォルダがあるかどうか確認し、なければ作成
	if os.path.exists("./sousouwa_ss") == False:
		os.mkdir('./sousouwa_ss')

	filename = './sousouwa_ss/' + title + '.html'

	#koboはhtmlとして認識させないと文字化けするので、htmlスニペットを用意
	htmlWrapBefore = '<?xml version="1.0" encoding="Shift_JIS"?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xml:lang="ja" ><body><pre>'
	htmlWrapAfter = "</pre></body></html>"

	#ファイルに書き出す
	sjisWriter = codecs.open(filename, 'w', 'cp932')
	sjisWriter.write(htmlWrapBefore)
	sjisWriter.write(body) # 引数の文字列をファイルに書き込む
	sjisWriter.write(htmlWrapAfter)

	#処理完了をコンソールに伝える
	print title
	print 'is downloaded successfully.'
 
if __name__ == '__main__':
	main()