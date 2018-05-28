#!/bin/bash
if [ $# -lt 2 ];then
    echo "批量打包指定目录下的文件，保存到指定位置."
    echo "参数1: 源文件夹 参数2: 保存路径"
    exit 2
fi

if [ ! -d ${2} ];then
    echo ${2}, "目录不存在."
    echo "创建文件夹-> ${2}"
    mkdir -p "${2}"
fi

cd $1
for item in $(ls "../$1" |tr " " "_");do
    filename=$(echo "${item}" |tr "_" " ")
    zip -q -r ${2}/"${item}".zip "${filename}"
    echo "done->${2}/${item}.zip"
done

echo "所有文件压缩完成."
