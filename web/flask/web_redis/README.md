# Redis的RestFul风格服务端

> [Flask Web Development book](https://www.flaskbook.com/) | [配套源码](https://github.com/miguelgrinberg/flasky-first-edition) | [Click](http://www.jb51.net/books/400693.html)

## 启动服务流程
_第一次运行_
```sh
    apt install python3-venv
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    chmod +x main.py
    ./main.py
```
- 之后就只需
    - 启动虚拟环境`source venv/bin/activate ` 
    - 启动 `./main.py`

- 退出虚拟环境 `deactive` 

### 按键分析模块

![](https://raw.githubusercontent.com/Kuangcp/ImageRepos/master/Image/WebRedis/line-area.png)

## TODO 
- [ ] 怎么支持宿主机的Redis, 先搞定容器的Redis吧 https://github.com/anapsix/docker-webdis

- [ ] 学习Python的基础语法 尤其是模块

- [ ] Web服务器性能巨差, 还会丢失连接,  gevent 或者nginx来改善

- [ ] http://www.cnblogs.com/Ray-liang/p/4173923.html 学习
- [ ] https://www.jianshu.com/p/679dee0a4193 uwsgi

https://blog.csdn.net/sinat_36651044/article/details/77462831

- [ ] 更改交互逻辑, 怎么处理多数据类型

