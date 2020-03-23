#! /usr/bin/python3
# -*- coding: utf8 -*-
class MatchResult:
    
    def __init__(self):
        self.keyword = ""
        self.count = ""
        self.position = []
        self.source = []
        self.id = []
        self.videotype = []
        
    def getKeyword(self):
        return self.keyword
    def getCount(self):
        return self.count
    def getPositions(self):
        return self.position
    def getSource(self):
        return self.source
    def getId(self):
        return self.id
    def getType(self):
        return self.videotype
    
    def setKeyword(self,q):
        self.keyword = q
    def setCount(self,count):
        self.count = count
    def addPosition(self,position):
        self.position.append(position) 
    def addSource(self,source):
        self.source.append(source )
    def addId(self,id):
        self.id.append(id)
    def addType(self,videotype):
        self.videotype.append(videotype)
    
if __name__ == '__main__':
    pass
