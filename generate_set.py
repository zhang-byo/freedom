#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
from util import *

# 原始样本对标签文件
origin = "dataset/list"
# 保存节点块数量信息的 json 文件
suffix = "info.json"
# 各个目录下的节点块信息 json 文件
arm_gcc = "ARM-gcc-default/" + suffix
mips_gcc = "MIPS-gcc-default/" + suffix
ppc_gcc = "PPC-gcc-default/" + suffix
x86_gcc = "X86-gcc-default" + suffix
x64_clang_o0 = "X64-clang-O0/" + suffix
x64_clang_o1 = "X64-clang-O1/" + suffix
x64_clang_o2 = "X64-clang-O2/" + suffix
x64_clang_o3 = "X64-clang-O3/" + suffix
x64_clang_os = "X64-clang-Os/" + suffix
x64_gcc_o0 = "X64-gcc-O0/" + suffix
x64_gcc_o1 = "X64-gcc-O1/" + suffix
x64_gcc_o2 = "X64-gcc-O2/" + suffix
x64_gcc_o3 = "X64-gcc-O3/" + suffix
x64_gcc_os = "X64-gcc-Os/" + suffix
x64_icc_o0 = "X64-icc-O0/" + suffix
x64_icc_o1 = "X64-icc-O1/" + suffix
x64_icc_o2 = "X64-icc-O2/" + suffix
x64_icc_o3 = "X64-icc-O3/" + suffix
x64_icc_os = "X64-icc-Os/" + suffix
# 所有节点块信息 json 文件
all_info_json = "dataset/" + suffix

OUTPUT_FILE = "result/aaaa"


def main():
    if not file_exist(origin):
        print("原始标签样本不存在.", origin)
        return
    if not file_exist(all_info_json):
        print("所有节点块信息 json 文件不存在。", all_info_json)
        return

    origin_json, ok = read_json(all_info_json)
    if not ok:
        print("读取json文件出错。", origin_json)
        return

    count = 0
    ma = 0
    with open(origin, "r", encoding="utf-8") as f:
        for line in f:
            ma = ma + 1
            temp_list = re.split(r"\s+", line)
            if len(temp_list) < 3:
                print("不符合格式行->", line)
            g1 = temp_list[0]
            g2 = temp_list[1]
            label = int(temp_list[2])
            if label < 1:
                label = -1

            if g1 in origin_json.keys() and g2 in origin_json.keys():
                if 1 == label and origin_json[g1] != origin_json[g2]:
                    print(origin_json[g1], origin_json[g2])
                    count = count + 1
    print("done.", ma, count)


if __name__ == "__main__":
    main()
