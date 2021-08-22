from flask import Flask

app = Flask(__name__)

@app.route("/spotifycallback")
def hola(req):
    print(req)
