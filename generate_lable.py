#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import os
import sys

PLATFORM = ["ARM", "MIPS", "PPC", "X64", "X86"]
OPTION = ["O0", "O1", "O2", "O3", "Os"]


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


def main(input_file, output_dir):
    positive_result = list()
    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            content = handle_line(line.strip())
            positive_result.extend(content)
    # 正样本
    p_file = output_dir + os.path.sep + "positive_sample"
    with open(p_file, "w", encoding="utf-8") as f:
        f.writelines(positive_result)
    print("正样本数量为:", len(positive_result))
    # 负样本
    n_file = output_dir + os.path.pathsep + "negative_sample"
    pass


def test():
    main("dataset/unique_bins", "./")


if __name__ == "__main__":
    test()
    # if len(sys.argv) < 3:
    #     print("参数1: 所有二进制文件列表文件路径 参数2: 结果保存目录")
    #     exit(1)
    # main(sys.argv[0], sys.argv[1])
    print("done.")
