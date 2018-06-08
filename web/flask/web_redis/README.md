# Redis的RestFul风格服务端

> [Flask Web Development book](https://www.flaskbook.com/) | [配套源码](https://github.com/miguelgrinberg/flasky-first-edition) | [Click](http://www.jb51.net/books/400693.html)

## 启动服务流程
```sh
    python3 -m venv venv
    source venv/bin/activate
    pip install flask flask_cors redis
    chmod +x app.py
    ./app.py
```

- 退出虚拟环境 deactive, 进入则是 `source venv/bin/activate`

## TODO 
- [ ] 怎么支持宿主机的Redis, 先搞定容器的Redis吧 https://github.com/anapsix/docker-webdis

- [ ] 学习Python的基础语法 尤其是模块

- [ ] Web服务器性能巨差, 还会丢失连接,  gevent 或者nginx来改善

- [ ] http://www.cnblogs.com/Ray-liang/p/4173923.html 学习
- [ ] https://www.jianshu.com/p/679dee0a4193 uwsgi

https://blog.csdn.net/sinat_36651044/article/details/77462831

- [ ] 为什么不能载入图表, 参数都是正确的 
