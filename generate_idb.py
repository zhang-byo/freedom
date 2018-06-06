#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import logging, logging.handlers
from util import *

# 程序运行日志文件
log_dir = "./"
logfile = log_dir + 'log_generate_idb.log'
logfile_size = 50 * 1024 * 1024  # 日志文件的最大容量，默认最大为50M
# 配置日志: 2个日志文件副本
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('generate_idb')

handler = logging.handlers.RotatingFileHandler(filename=logfile, maxBytes=logfile_size, backupCount=2, encoding='utf-8')
handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s [ %(name)s : %(levelname)s ] %(message)s')
handler.setFormatter(formatter)

logger.addHandler(handler)


def main(input_file, output_file):
    if os.path.isfile(input_file):
        try:
            generate_i64(input_file, output_file)
        except Exception as e:
            logging.error("生成i64文件出错->" + e)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("参数1： 二进制程序路径 参数2：i64 文件保存路径")
        exit(1)
    main(sys.argv[1], sys.argv[2])
