#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sys
import numpy as np
import pickle
from util import *
import logging, logging.handlers

# 程序运行日志文件
log_dir = "./"
logfile = log_dir + 'log_json_to_feature.log'
logfile_size = 50 * 1024 * 1024  # 日志文件的最大容量，默认最大为50M
# 配置日志: 2个日志文件副本
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('json_to_feature')

handler = logging.handlers.RotatingFileHandler(filename=logfile, maxBytes=logfile_size, backupCount=2, encoding='utf-8')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s [ %(name)s : %(levelname)s ] %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


def handle_dict(data):
    sort_keys = sorted(data.keys())
    if len(sort_keys) > 2:
        adj_matrix = data[sort_keys[-2]]
        # ida 反汇编后得到的该函数名, 暂时未用到
        func_name = data[sort_keys[-1]]
        for n, k in enumerate(sort_keys[:-2]):
            # 对角线元素初始为 1
            adj_matrix[n][n] = 1
            adj_matrix[n].extend(handle_dict_value(data[k]))
    return np.array(adj_matrix, dtype=np.float)


def handle_dict_value(value):
    """
    从一个基本块特征字典中构造该特征向量
    :param value: 基本块特征字典
    :return: 以列表形式返回按标准顺序排列的特征
    """

    row = list()
    keys = value.keys()
    if "String_Constant" in keys:
        string_constant = len(value["String_Constant"])
        row.append(string_constant)
    else:
        row.append(0)

    if "Numberic_Constant" in keys:
        numberic_constant = len(value["Numberic_Constant"])
        row.append(numberic_constant)
    else:
        row.append(0)

    for k in ["No_Tran", "No_Call", "No_Instru", "No_Arith", "No_offspring", "Betweenness"]:
        if k in keys:
            row.append(value[k])
        else:
            row.append(0)

    return row


def write_to_pkl(content, output_dir, filename):
    """
    将内容序列化到磁盘文件中
    :param content: 内容数据
    :param output_dir: 保存的目录
    :param filename: 序列化文件名
    :return: 序列化文件保存路径, 序列化是否成功
    """
    ensure_dir(output_dir)
    filepath = output_dir + os.path.sep + filename
    if not file_exist(filepath):
        with open(filepath, "wb+") as f:
            pickle.dump(content, f)
            return filepath, True
    return filepath, False


def get_all_input_file(input_dir):
    """
    获取输入文件夹下的所有文件
    :param input_dir: 输入文件夹的路径
    :return: 该文件夹下的所有文件
    """
    if os.path.isdir(input_dir):
        all_item = [input_dir + os.path.sep + f.strip() for f in os.listdir(input_dir)]
        all_file = [item for item in all_item if os.path.isfile(item)]
        return all_file
    return []


def main(in_dir, out_dir):
    ensure_dir(out_dir)
    mydict = dict()
    for file in get_all_input_file(in_dir):
        filename = os.path.basename(file)
        dirname = re.split(r"/", os.path.dirname(file))[-1]
        # 文件名为去除 .json 后缀的名字
        if ".json" == filename[-5:]:
            filename = filename[:-5]
        # 读取 JSON 文件得到的是一个字典列表
        data, ok = read_json(file)
        if ok and isinstance(data, list):
            data_len = len(data)
            for i, item in enumerate(data):
                result = handle_dict(item)
                write_to_pkl(result, out_dir, filename + "_" + str(i) + "_" + str(data_len))
                output_file = out_dir + os.path.sep + filename + "_" + str(i) + "_" + str(data_len)
                logger.info("done-> " + output_file)
            mydict[str(dirname + os.path.sep + filename).strip()] = data_len
        else:
            logger.error("main error-> 读取json: " + str(data))
    # 保存基本块数量信息到 info.json 文件
    write_json(mydict, out_dir + os.path.sep + "info.json")
    logger.info("write json->" + out_dir + os.path.sep + "info.json")


def test_json():
    """
    测试作为输入的 json 文件
    :return:
    """
    main("dataset", "result")


def test_pkl():
    """
    测试序列化后的 pkl 文件 是否可以被反序列化得到正确格式的结果
    :return: numpy.ndarray ,数据shape为 (n, n+8)
    """
    with open("result/shareport1_12_127", "rb+") as f:
        ans = pickle.load(f)
        print(type(ans))
        print(ans.shape)
        print(ans)
        return ans


if __name__ == "__main__":
    # test_json()
    # test_pkl()

    if len(sys.argv) < 3:
        print("参数1:", "输入文件夹路径(保存特征数据的json目录)", "参数2:", "保存文件路径")
        exit(-1)

    try:
        main(sys.argv[1], sys.argv[2])
        print("所有任务完成.")
    except Exception as e:
        print("运行脚本出现异常:", e)
    finally:
        print("程序停止！")
