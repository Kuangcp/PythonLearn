# Redis的RestFul风格服务端

> [Flask Web Development book](https://www.flaskbook.com/) | [配套源码](https://github.com/miguelgrinberg/flasky-first-edition) | [Click](http://www.jb51.net/books/400693.html)

## 启动服务流程
```sh
    virtualenv --no-site-packages web_redis_lib
    source web_redis_lib/bin/activate
    pip install flask flask_cors
    chmod +x app.py
    ./app.py
```

## TODO 
- [ ] 怎么支持宿主机的Redis, 先搞定容器的Redis吧 https://github.com/anapsix/docker-webdis

- [ ] 学习Python的基础语法 尤其是模块

- [ ] Web服务器性能巨差, 还会丢失连接,  gevent 或者nginx来改善