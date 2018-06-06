#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os
import json
import logging, logging.handlers

IDA_ENGINE_PATH = "/usr/local/ida/idal64"
IDA_START = os.getcwd() + os.path.sep + "shell/ida_start.sh"

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


def write_json(content, filepath):
    """
    写入数据到 JSON 文件，返回文件的路径
    :param content: 写入到 json 文件中的内容
    :param filepath: json文件路径
    :return: 文件路径
    """
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(content, f)
        return filepath, True
    return None, False


def generate_i64(binary_path, idb_store_path, ida_start=IDA_START, ida_engine_path=IDA_ENGINE_PATH):
    """
    生成二进制程序的 i64 文件并保存到指定目录(i64文件名可同时指定, 未指定则与二进制程序同名)
    :param binary_path: 二进制程序路径
    :param idb_store_path: i64 文件保存路径
    :param ida_start: 启动 ida 的脚本
    :param ida_engine_path: idal64 的路径
    :return: 生成的 i64 文件的路径
    """
    if os.path.exists(ida_engine_path):
        # ida 加载二进制文件并将 ida 的i64文件保存到指定位置
        os.system('/bin/bash %s %s %s %s' % (ida_start, ida_engine_path, binary_path, idb_store_path))
        # i64 文件保存在当前目录下时，其默认名字与二进制程序名相同
        if idb_store_path == "." or idb_store_path == "./":
            return os.path.basename(binary_path) + ".i64"
        elif idb_store_path[-4:] == ".i64":
            # 指定 i64 文件保存路径时, 输入带有文件名后缀 .i64
            return idb_store_path
        else:
            return idb_store_path + ".i64"
