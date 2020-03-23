#! /usr/bin/python3
# -*- coding: utf8 -*-
from random import randrange


class KeywordUtil():
    keywords = []
    
    # 初始化时读取关键词文件
    def __init__(self, filename):
        with open(filename, 'r', encoding='utf-8') as keywordfile:
            self.keywords = keywordfile.read().splitlines()

    def getAllKeywords(self):
        """获取文件里所有关键词"""
        return self.keywords

    def getKeywords(self, fromNum, toNum):
        """获取从fromNum到toNum的关键词"""
        return self.keywords[fromNum:toNum]

    def getRandomKeyword(self):
        """随机获取一条关键词"""
        num = randrange(1, len(self.keywords), 1)
        return self.keywords[num]

    def getRandomKeywords(self, num):
        """随机获取num条关键词"""
        randoms = []
        for i in range(num):
            randoms.append(self.getRandomKeyword())
        return randoms
