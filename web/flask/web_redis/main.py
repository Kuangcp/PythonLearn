#!venv/bin/python3
from config import app

if __name__ == '__main__':
    print('主页 http://127.0.0.1:22334/static/key/index.html')
    # TODO 127.0.0.1 0.0.0.0 docker 和宿主机
    app.run(debug=True, port=22334, host='0.0.0.0')
