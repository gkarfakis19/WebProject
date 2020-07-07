from app import app


@app.route('/')
@app.route('/spandex')
def index():
    return "Hello, Boy!!"
