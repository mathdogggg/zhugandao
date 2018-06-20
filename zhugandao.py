#-*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import os, time
import re
url = (r'https://nba.hupu.com/')


#获取主干道热帖标题和链接，返回url和标题
def get_retie_title_url(url):
	index_html = requests.get(url)
	index_html_s = BeautifulSoup(index_html.text,'lxml')
	main_street = index_html_s.find(class_ = 'gray-list main-stem max250')
	url_list = []
	url_name_list = []
	for dd in main_street.find_all('dd',limit = 14):
		url_list.append(dd.a.get('href'))
		url_name_list.append(dd.a.get_text())
	return [url_list,url_name_list] 

#获取热帖正文中的图片列表,利用set去重
def get_pic_url(retie_list,num):
	pic_url_list = set()
	retie_html = requests.get(retie_list[0][num-1])
	retie_html_s = BeautifulSoup(retie_html.text,'lxml')
	retie_content = retie_html_s.find(class_='quote-content')
	for pic_url in retie_content.find_all('img'):
		try:
			original_url = pic_url.get('data-original')
			pic_url_list.add(original_url.split('?')[0])
		except:
			pic_url_list.add(pic_url.get('src'))
	return pic_url_list

#创建以标题命名的文件夹，并返回是否创建成功
def makedir(retie_title):
	path = ('E:\\pic\\zhugandao\\%s' % retie_title)
	if os.path.exists(path):
		return 0
	else:
		os.makedirs(path)
		return path

#获取亮贴中的图片列表

def get_comment_pic_url(retie_list,num):
	comment_pic_url_list = set()
	retie_html = requests.get(retie_list[0][num-1])
	retie_html_s = BeautifulSoup(retie_html.text,'lxml')
	retie_comment = retie_html_s.find(id='readfloor')
	for floor in retie_comment.find_all('table'):
		for pic_url in floor.find_all('img'):			
			try:
				original_url = pic_url.get('data-original')
				comment_pic_url_list.add(original_url.split('?')[0])
			except:
				comment_pic_url_list.add(pic_url.get('src'))
	return comment_pic_url_list


#下载图片，可下载gif、jpg、png格式
def download_pic(pic_url_list,path,pic_from = '正文'):
	a = 1
	for url in pic_url_list :
		if url.endswith('.gif'):
			pic = requests.get(url)
			with open((path+('\\%s-%s.gif' % (pic_from,a))),'wb') as f:
				f.write(pic.content)
				f.close
				print('下载一张%s动图' % pic_from)
			a += 1
		if url.endswith('.jpg'):
			pic = requests.get(url)
			with open((path+('\\%s-%s.jpg' % (pic_from,a))),'wb') as f:
				f.write(pic.content)
				f.close
				print('下载一张%sjpg图' % pic_from)
			a +=1
		if url.endswith('.png'):
			pic = requests.get(url)
			with open((path+('\\%s-%s.png' % (pic_from,a))),'wb') as f:
				f.write(pic.content)
				f.close
				print('下载一张%spng图' % pic_from)
			a +=1

if __name__ == "__main__":
	retie = get_retie_title_url(url)
	a = 1
	for retie_title in retie[1]:
		print(a,'  ',retie_title)
		print('--------------------------------')
		a += 1
	num = int(input('请输入要下载的热帖排序（1-14）'))
	if num < 1 or num > 14:
		print('不合法')
	else:
		path = makedir(retie[1][num-1])
		if path != 0:
			pic_url_list = get_pic_url(retie,num)
			comment_pic_url_list = get_comment_pic_url(retie,num)
			download_pic(pic_url_list,path)
			download_pic(comment_pic_url_list,path,'评论')
		else:
			print('目录已存在，等待虎扑更新')


