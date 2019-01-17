"""
    反正我也不会数据库什么的, 数据存储全靠键值对
    
    那就普通的json编辑就行了
    
    <TODO>: 改写为数据库操作

    基于K.I.S.S.编写
"""
__author__ = 'Camber'
import os,sys,logging,json
class jsonHandler(object):
    def __init__(self,path='./userDatas.json'):
        _path = path
    