## 55156爬图片
> 目标网站 [www.55156.com](http://www.55156.com) 目前只是单线程,把脚本放在服务器跑一晚上就有一大堆图片url了, 下载也是单线程, 更改多线程ing

- 使用 python3 simple.py 即可开始爬取图片URL, 当然要先配置好redis
    - simple_pro.py 是图形化的操作
- 使用 python3 download.py 即可开始下载图片, 先配置好下载文件夹
- python3 将所有图片生成md文件 [高耗流量,慎点](https://github.com/Kuangcp/PythonLearn/tree/master/learning/Spider/scrpy_learn/55156/result)

