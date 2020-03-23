#! /usr/bin/python3
# -*- coding: utf8 -*-
import re
import socket
import urllib
import requests
from urllib.error import HTTPError
from bs4 import BeautifulSoup
from builtins import AttributeError

socket.setdefaulttimeout(60)

class SpiderUtil():
    
    @staticmethod
    def getSoupContent(url):
        '''根据搜索url，获取soup''' 
        #headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        try:
            request = urllib.request.Request(url=url, headers=headers)
            response = urllib.request.urlopen(request,timeout=30)
        except HTTPError:
            return ""
        except socket.timeout:
            return ""
        #ssl._create_default_https_context = ssl._create_unverified_context
        soup = BeautifulSoup(response,'html.parser',from_encoding="gb18030")
        return soup
    
    #Example: findContentbyTag(soup,"div") 
    @staticmethod
    def findContentbyTag(soup,tag):
        return soup.find_all(tag)
    
    #Example: findContentby2Tags(soup,"div","a") 
    @staticmethod
    def findContentby2Tags(soup,tag1,tag2):
        return soup.find_all(tag1,tag2)
    
    #Example: findContentbyTagClass(soup,"div","positive-box clearfix") 
    @staticmethod
    def findContentbyTagClass(soup,tag,classvalue):
        return soup.find_all(tag, class_=classvalue)
    
    #Example: getContentbyTagAttrs(soup,"input[id=totalCount]","value")
    @staticmethod
    def getContentbyTagAttrs(soup,tag,attrs):
        '''获取召回总数'''
        return soup.select(tag)[0].attrs[attrs]
    
    #Example: findContentbyRe(soup,"^p")
    @staticmethod
    def findContentbyRe(soup,pattern):
        return soup.find_all(re.compile(pattern))
    
    @staticmethod
    def getBrand(soup): 
        '''根据搜索关键词，获取的品牌名'''  
        try:
            link_brand = soup.find_all('a', class_='goods-list')
        except AttributeError:
            return "未命中"
        if len(link_brand)==0:
            brand = "未命中"
        else:
            brand = link_brand[0].em.text
        #logger.debug("Brand = %s" % brand)
        return brand
    
    @staticmethod 
    def getTitlesFromPage(soup):
        v_list = []
        vid_list = []
        vtype_list = []
        try:  
            link_video = soup.find_all('div', class_='positive-box clearfix')
        except AttributeError:
            return [v_list,vid_list,vtype_list]
        num_found = len(link_video)
        if num_found!=0:
            for num in range(num_found):
                v_list.append(link_video[num].find('a').attrs['title'])
                temp = (link_video[num].find('a').attrs['ext_info']).split("'")
                if temp[3]!="":
                    vid_list.append(temp[3])
                else:
                    vid_list.append("第三方")
                vtype_list.append(link_video[num].find('span','video-config').text.replace("\\n",""))
            return [v_list,vid_list,vtype_list]
        else:
            return [v_list,vid_list,vtype_list]
    
    @staticmethod
    # num:召回结果数
    def getTitles(soup,num):
        '''获取召回数目范围内的所有标题'''
        titles = []    
        link_title = soup.find_all('div',class_='img-block')
        if len(link_title)==0:
            return titles
        else:
            for i in range(len(link_title)):
                if i==num:
                    return titles
                else:
                    title = link_title[i].img.attrs['alt']
                    titles.append(title)
            return titles
    
    @staticmethod
    # num:召回结果数
    def getAuxdescription(soup, num):
        '''获取召回数目范围内的所有卖点'''
        Auxdescriptions = []
        link_title = soup.find_all('div', class_='img-block')
        if len(link_title) == 0:
            return Auxdescriptions
        else:
            for i in range(len(link_title)):
                if i == num:
                    return Auxdescriptions
                else:
                    Auxdescription = link_title[i].a.attrs['title']
                    Auxdescriptions.append(Auxdescription)
            return Auxdescriptions
    
    @staticmethod
    def getStoreName(soup,num):
        '''获取召回数目范围内的店铺名称'''
        StoreNames = []
        link_title = soup.find_all('div', class_='store-stock')
        if len(link_title) == 0:
            return StoreNames
        else:
            for i in range(len(link_title)):
                if i == num:
                    return StoreNames
                else:
                    StoreName = link_title[i].a.text
                    StoreNames.append(StoreName)
            return StoreNames
            
    @staticmethod
    # num:召回结果页数
    def getPageNum(soup):
        '''获取召回页数'''  
        searchcontent = soup.find_all('span',class_='fl')
        return searchcontent[0].contents[3].text
    
    @staticmethod
    def getTotalCount(soup):
        '''获取召回总数'''
        if soup.select('input[id=totalCount]')!=[]: #考虑没有商品召回的情况
            return soup.select('input[id=totalCount]')[0].attrs['value']
        else: 
            return 0
        
    @staticmethod
    def getCategory(soup):
        category = soup.find_all('div',class_='class-relevant')
        try:
            category = category[0].text.strip().replace("\n"," | ")
        except IndexError:
            category = "未命中"
        return category
    
    @staticmethod
    def getHtml(url):
        '''根据搜索url，获取html'''
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}
        socket.setdefaulttimeout(20)
        try:
            response = requests.get(url,headers=headers).text
        except HTTPError:
            return ""
        except socket.timeout:
            return ""
        return response