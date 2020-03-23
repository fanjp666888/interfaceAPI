#! /usr/bin/python3
# -*- coding: utf8 -*-
from random import randrange


class FileUtil(object):
    all_lines = []

    def __init__(self, filename):
        """初始化时读取关键词文件"""
        with open(filename, 'r', encoding='utf-8') as textfile:
            self.all_lines = textfile.read().splitlines()

    def getAllLines(self):
        """获取文件里所有行的内容"""
        return self.all_lines

    def getLines(self, fromNum, toNum):
        """获取从fromNum到toNum的行的内容"""
        return self.all_lines[fromNum:toNum]

    def getRandomLine(self):
        """随机获取一行的内容"""
        # randrange ([start,] stop [,step])
        num = randrange(1, len(self.all_lines), 1)
        return self.all_lines[num]

    def getRandomLines(self, num):
        """随机获取num行的内容"""
        randoms = []
        for i in range(num):
            randoms.append(self.getRandomLine())
        return randoms
