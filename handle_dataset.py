#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import pickle as pkl
import numpy as np
from util import *

# 路径前缀
pre_path = "/home/ubuntu/disk/hdd_2/iie/dataset/"
# 定义最大节点数，小于该节点即进行填充0
MAX_NODE = 1024
# 特征的维度
FEATURE_NODE = 8


def generate_pkl(content):
    new_content = np.zeros((MAX_NODE, MAX_NODE + FEATURE_NODE), dtype=np.float)
    g = content[:, :-8]
    e = content[:, -8:]
    old_node = g.shape[0]

    if old_node <= MAX_NODE:
        new_content[0:old_node, 0:old_node] = g
        new_content[0:old_node, MAX_NODE:] = e
    else:
        new_content[0:MAX_NODE, 0:MAX_NODE] = g[0:MAX_NODE, 0:MAX_NODE]
        new_content[0:MAX_NODE, MAX_NODE:] = e[0:MAX_NODE, MAX_NODE:]
    return new_content


def handle_line(input_pkl):
    if file_exist(input_pkl):
        with open(input_pkl, "rb") as f:
            origin = pkl.load(f)
            return generate_pkl(origin)


def write_pkl(content, file_path):
    try:
        with open(file_path, "wb") as f:
            pkl.dump(content, f)
            return True
    except Exception as e:
        print("write pkl error->", file_path, e)
        return False


def main(input_file):
    if file_exist(input_file):
        with open(input_file, "r", encoding="utf-8") as f:
            for line in f:
                line = pre_path + line.strip()
                new_pkl = handle_line(line)
                if write_pkl(new_pkl, line):
                    print("done->", line)
                else:
                    print("error->", line)


def test():
    handle_line("dataset/text+time_human")
    with open("dataset/text+time_human", "rb") as f:
        c = pkl.load(f)
        print(type(c))
        print(c.shape)
        print(c)


if __name__ == "__main__":
    # test()
    if len(sys.argv) < 2:
        print("参数1:", "保存pkl路径的列表文件路径(直接覆盖原始的pkl文件)")
        exit(-1)

    try:
        main(sys.argv[1])
        print("所有任务完成.")
    except Exception as e:
        print("运行脚本出现异常:", e)
    finally:
        print("程序停止！")
