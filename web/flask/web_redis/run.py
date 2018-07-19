#!venv/bin/python3
from app import app

print('主页 http://127.0.0.1:22334/static/index.html')
print('api  http://127.0.0.1:22334/redis/api/v1.0/')
app.run(debug = True, port=22334, host='0.0.0.0')
