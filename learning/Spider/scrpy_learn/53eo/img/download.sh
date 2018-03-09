#!/bin/dash

# 把图片链接分开来, 方便细颗粒管理
basePath=`pwd`'/'
title=''
total=1

# 根据传入的参数创建目录和下载图片
downByURL(){
    line=$1
    title=`echo $line | grep '='`
    # echo $title
    if [ "$title"z != 'z' ];then
        echo $title
        # cd $basePath
        mkdir -p $basePath$title && cd $basePath$title
        echo "mkdir -p $basePath$title && cd $basePath$title"
    else
        total=`expr $total + 1`;
        # 将URL截取为文件名, 很容易出问题, 如果域名更换了
        filename=`echo $line | colrm 1 46`
        
        echo $line
        echo $filename
        printf ">>>>>>当前第:"$total
        # echo "curl -o $filename -H \"Cookie: _cnzz=1101; fist_user=1\" $line"
        curl -o $filename -H "Cookie: _cnzz=1101; fist_user=1" $line
    fi
    # sleep 2
}
downImg(){
    cat $1 | while read line
    do 
        downByURL $line
    done
    cd $basePath && echo "实际下载"`ls -lR|grep "^-"|wc -l`"个"
}

case $1 in 
	-d | d)
        downImg $2
	;;
    -re | re)
        echo "在某文件下下载图片"
    ;;
    -h | h)
        echo "-d|d file  使用对应的配置文件进行下载"
    ;;
esac
