# coding=utf-8
# Date: 15/9/11
# Time: 下午4:11
# Email:fanjunwei003@163.com
import os

__author__ = '范俊伟'


def del_all_mirations(root):
    for i in os.listdir(root):
        if i != '__init__.py':
            path = os.path.join(root, i)
            print path
            os.remove(path)


def for_each_file(root):
    for i in os.listdir(root):
        path = os.path.join(root, i)
        if os.path.isdir(path):
            if i == 'migrations':
                del_all_mirations(path)
            else:
                for_each_file(path)


path = os.path.dirname(__file__)

for_each_file(path)
