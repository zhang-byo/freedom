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


def is_pkl_exists(prefix, pkl):
    if file_exist(prefix + os.path.sep + pkl):
        return True
    return False


def generate_positive(one_line):
    result = list()
    one_line = one_line.strip()
    idx = one_line.find('/', 10)
    if -1 != idx:
        text = one_line[idx:]
        for platform in PLATFORM:
            for option in OPTION:
                right_part = "pkl/" + platform + "/" + option + text.strip()
                if is_pkl_exists("/home/ubuntu/disk/hdd_2/iie/dataset", right_part):
                    one_result = one_line + " " + right_part + " 1\n"
                    result.append(one_result)
                    print("正样本done->", one_result.strip(), end="")
                else:
                    print("not exist->~/disk/hdd_2/iie/dataset" + os.path.sep + right_part)
    return result


def is_negative_couple(left_part, right_part):
    left_part = left_part.strip()
    right_part = right_part.strip()
    # 左侧组件
    idx_left = left_part.find('/', 10)
    if -1 != idx_left:
        left = left_part[idx_left:]
        # 右侧组件
        idx_right = right_part.find('/', 10)
        if -1 != idx_right:
            right = right_part[idx_right:]
            if left == right:
                return False
            else:
                return True
        else:
            return False
    else:
        return False


def shuffle_all_lable(p, n):
    p = p.extend(n)
    random.shuffle(p)
    return p


def main(input_file, output_dir):
    ensure_dir(output_dir)
    # 正样本
    positive_number = 0
    with open(input_file, "r", encoding="utf-8") as f:
        all_pkl_list = f.readlines()
        # 正样本标签保存路径
        p_file = output_dir + os.path.sep + positive_file
        if file_exist(p_file):
            os.remove(p_file)
        with open(p_file, "w+", encoding="utf-8") as pf:
            for line in all_pkl_list:
                one_sample = generate_positive(line)
                pf.writelines(one_sample)
                positive_number += 1
            print("正样本数量为:", positive_number * 25)
        # 负样本
        negative_number = 0
        # 负样本标签保存路径
        n_file = output_dir + os.path.sep + negative_file
        if file_exist(n_file):
            os.remove(n_file)
        with open(n_file, "w+", encoding="utf-8") as nf:
            while True:
                if negative_number > positive_number * 2:
                    break
                left_id = get_random_int(0, len(all_pkl_list) - 1)
                right_id = get_random_int(0, len(all_pkl_list) - 1)
                if is_negative_couple(all_pkl_list[left_id], all_pkl_list[right_id]):
                    one_sample = all_pkl_list[left_id].strip() + " " + all_pkl_list[right_id].strip() + " 0\n"
                    negative_number += 1
                    nf.write(one_sample)
                    print("负样本done->", one_sample, end="")
            print("负样本数量为:", negative_number)
    # 正负样本标签对无序混合
    with open(output_dir + os.path.sep + "lables") as f:
        p_result = read_list(p_file)
        n_result = read_list(n_file)
        all_lables = shuffle_all_lable(p_result, n_result)
        f.writelines(all_lables)
    print("labels done->", output_dir + os.path.sep + "lables")


def test():
    main("dataset/all_pkl", "./")


if __name__ == "__main__":
    # test()
    if len(sys.argv) < 3:
        print("从pkl文件列表生成正负样本标签对")
        print("参数1: 文件列表文件路径 参数2: 结果保存目录")
        exit(1)
    main(sys.argv[1], sys.argv[2])
    print("done.")
