#! /usr/bin/python3
# -*- coding: utf8 -*-
class SearchedResult:
    
    def __init__(self):
        self.__keyword    = ""
        self.__position   = ""
        self.__title      = ""
        self.__videoid    = ""
        self.__source     = ""
        self.__area       = ""
        self.__director   = ""
        self.__actor      = ""
        self.__description= ""
        self.__videotype  = ""
        self.__year       = ""

    def get_keyword(self):
        return self.__keyword

    def set_keyword(self, value):
        self.__keyword = value

    def get_year(self):
        return self.__year

    def set_year(self, value):
        self.__year = value

    def get_videotype(self):
        return self.__videotype

    def set_videotype(self, value):
        self.__videotype = value

    def get_position(self):
        return self.__position

    def get_title(self):
        return self.__title

    def get_videoid(self):
        return self.__videoid

    def get_source(self):
        return self.__source

    def get_area(self):
        return self.__area

    def get_director(self):
        return self.__director

    def get_actor(self):
        return self.__actor

    def get_description(self):
        return self.__description

    def set_position(self, value):
        self.__position = value

    def set_title(self, value):
        self.__title = value

    def set_videoid(self, value):
        self.__videoid = value

    def set_source(self, value):
        self.__source = value

    def set_area(self, value):
        self.__area = value

    def set_director(self, value):
        self.__director = value

    def set_actor(self, value):
        self.__actor = value

    def set_description(self, value):
        self.__description = value
    year = property(get_year, set_year, None, None)
    keyword = property(get_keyword, set_keyword, None, None)

if __name__ == '__main__':
    pass
