#!venv/bin/python3
from config import app

if __name__ == '__main__':
    print('主页 http://127.0.0.1:22334/static/key/index.html')
    app.run(debug=True, port=22334)
