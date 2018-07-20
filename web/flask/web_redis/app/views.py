from app import app

@app.route('/')
def index():
    return '<a href="/static/index.html"><button>index</button></a>'
