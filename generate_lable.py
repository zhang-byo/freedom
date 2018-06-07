#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os
import sys
from util import *

PLATFORM = ["ARM", "MIPS", "PPC", "X64", "X86"]
OPTION = ["O0", "O1", "O2", "O3", "Os"]
# 正样本
positive_file = "positive_sample"
# 负样本
negative_file = "negative_sample"


def handle_line(text):
    result = list()
    step1 = list()
    for platform in PLATFORM:
        for option in OPTION:
            step1.append(platform + "/" + option + "/" + text)
    for left in step1:
        for right in step1:
            if left == right:
                continue
            one_sample = left + " " + right + " 1\n"
            result.append(one_sample)
    return result


def generate_positive(one_line):
    result = list()
    one_line = one_line.strip()
    idx = one_line.find('/', 7)
    if -1 != idx:
        text = one_line[idx:]
        for platform in PLATFORM:
            for option in OPTION:
                one_result = one_line + " pkl/" + platform + "/" + option + text + " 1\n"
                result.append(one_result)
    return result


def main(input_file, output_dir):
    ensure_dir(output_dir)
    # 正样本
    positive_number = 0
    with open(input_file, "r", encoding="utf-8") as f:
        p_file = output_dir + os.path.sep + positive_file
        if file_exist(p_file):
            os.remove(p_file)
        with open(p_file, "w+", encoding="utf-8") as pf:
            for line in f:
                one_sample = generate_positive(line)
                pf.writelines(one_sample)
                positive_number += 1
                print("done->", line.strip())
            print("正样本数量为:", positive_number * 25)

    # p_file = output_dir + os.path.sep + "positive_sample"
    # with open(p_file, "w", encoding="utf-8") as f:
    #     f.writelines(positive_result)
    # print("正样本数量为:", len(positive_result))
    # # 负样本
    # n_file = output_dir + os.path.pathsep + "negative_sample"
    # pass


def test():
    main("dataset/all_pkl", "./")


if __name__ == "__main__":
    test()
    # if len(sys.argv) < 3:
    #     print("从pkl文件列表生成正负样本标签对")
    #     print("参数1: 文件列表文件路径 参数2: 结果保存目录")
    #     exit(1)
    # main(sys.argv[0], sys.argv[1])
    print("done.")
