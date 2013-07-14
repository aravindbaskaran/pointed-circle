import sqlite3
from flask import Flask, render_template, request, make_response, url_for, g
import main
import json
import utils
app = Flask(__name__)
DATABASE = 'dbs/wishd.db'

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = connect_to_database()
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def hello_world():
    return render_template("home.html") #'Hello World!'
@app.route('/twitter/<query>')
def onlyTwitter(query):
	return (json.dumps(main.twitterSearch(query)), 200, {'content-type': "application/json"})
@app.route('/search/<query>')
def searchQuery(query):
	app.logger.debug("Query - " + query)
	#response.headers.add('content-type', "application/json")
	return (json.dumps(main.search(query)), 200, {'content-type': "application/json"})
@app.route('/continue/', methods=['POST'])
def continueOp():
	content = request.json['content']
	return (json.dumps(main(query=content.query, prevResult=content.prevResult, type=content.type)), 200, {'content-type', "application/json"})
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response
@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id
app.debug = True
utils.logger = app.logger
if __name__ == '__main__':
    app.run()