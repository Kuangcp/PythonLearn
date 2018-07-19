from app import app

@app.route('/')
def index():
    return '<a href="http://127.0.0.1:22334/static/index.html"><button>index</button></a>'
