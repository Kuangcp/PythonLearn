#!/bin/dash

# 把图片链接分开来, 方便细颗粒管理
title=''
cd tests/test
total=1
cat ../../imgfile | while read line
do 
    title=`echo $line | grep '='`
    # echo $title
    if [ "$title"z != 'z' ];then
        echo $title
        cd ../../ && mkdir -p $title && cd "$title"
    else
        total=`expr $total + 1`;
        filename=`echo $line | colrm 1 43`
        printf ">>>>>>当前第:"$total
        # echo "curl -o $filename -H \"Cookie: _cnzz=1101; fist_user=1\" $line"
        curl -o $filename -H "Cookie: _cnzz=1101; fist_user=1" $line
    fi
    # sleep 2

done
cd /home/kcp/PycharmProjects/PythonMythLearn/learning/Spider/scrpy_learn/53eo/img
echo "实际下载"`ls -lR|grep "^-"|wc -l`"个"