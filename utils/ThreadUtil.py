#! /usr/bin/python3
# -*- coding: utf8 -*-
import threading


class ThreadUtil():
    def __init__(self):
        pass
    
    @staticmethod
    def runMultiThreading(totalThread, len_total, targetMethod, argsMethod):
        #global lock
        #lock=threading.Lock()
        threads = []
        gap = int(len_total / totalThread) 
        for i in range(totalThread):
            #thread = 'thread%s' % i
            if i == 0:
                thread = threading.Thread(target=targetMethod, args=(argsMethod(0, gap),))
            elif totalThread == i+1:
                thread = threading.Thread(target=targetMethod, args=(argsMethod(i*gap, len_total),))
            else:
                thread = threading.Thread(target=targetMethod, args=(argsMethod(i*gap, (i+1)*gap),))
            threads.append(thread) 
        # 循环开启线程
        for i in range(totalThread):
            threads[i].start()
        # 等待所有线程完成
        for t in threads:
            t.join()
    
    @staticmethod
    def runDBMultiThreading(totalThread, len_total, targetMethod, allkeywords,):
        #global lock
        #lock=threading.Lock()
        threads = []
        gap = int(len_total / totalThread) 
        for i in range(totalThread):
            #thread = 'thread%s' % i
            if i == 0:
                thread = threading.Thread(target=targetMethod,args=(allkeywords[0:gap],))
            elif totalThread == i+1:
                thread = threading.Thread(target=targetMethod,args=(allkeywords[i*gap:len_total],))
            else:
                thread = threading.Thread(target=targetMethod,args=(allkeywords[i*gap:(i+1)*gap],))
            threads.append(thread) 
        # 循环开启线程
        for i in range(totalThread):
            threads[i].start()
        # 等待所有线程完成
        for t in threads:
            t.join()