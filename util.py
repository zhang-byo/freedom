#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import logging, logging.handlers

# 程序运行日志文件
log_dir = "./"
logfile = log_dir + 'log_util.log'
logfile_size = 50 * 1024 * 1024  # 日志文件的最大容量，默认最大为50M
# 配置日志: 2个日志文件副本
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('util')

handler = logging.handlers.RotatingFileHandler(filename=logfile, maxBytes=logfile_size, backupCount=2, encoding='utf-8')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s [ %(name)s : %(levelname)s ] %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


def file_exist(filepath):
    if os.path.isfile(filepath):
        return True
    return False


def dir_exist(dirpath):
    if os.path.isdir(dirpath):
        return True
    return False


def ensure_dir(dirpath):
    """
    检查目标文件夹是否存在,不存在则直接递归创建文件夹
    :param dirpath: 目标文件夹
    :return:
    """
    if not dir_exist(dirpath):
        os.makedirs(dirpath)


def read_json(filepath):
    """
    读取 JSON 文件，返回文件内容和读取状态
    :param filepath: json文件路径
    :return: (文件内容, 读取状态)
    """
    if not file_exist(filepath):
        logger.error("文件不存在-> " + filepath)
        return "", False

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data, True
