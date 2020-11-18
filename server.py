from flask import Flask, escape, url_for

app = Flask(__name__)

feed = ''
with open('feedgra.xml', 'r') as f:
    feed = f.read()

@app.route('/rss')
def rss():
    return feed

if __name__ =="__main__":
    app.run('0.0.0.0', debug=False, port=8000)