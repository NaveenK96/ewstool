from flask import Flask
from flask import request
import sqlite3
from flask import render_template

app = Flask(__name__)

assignments = {}

@app.route('/')
def hello(name=None):
	return render_template('index.html')

# @app.route('/<name>', methods=['GET', 'POST'])
# def hello2(name=None):
# 	# if request.method == 'POST':
# 	# 	commentInfo = request.form.get('replyTo', None).split(" ")
# 	# 	commentText = request.form.get('newcomment', None)
# 	# 	con = sqlite3.connect("comments.db")
# 	# 	cursor = con.cursor()
# 	# 	insertComment(commentInfo, commentText, cursor)
# 	# 	con.commit()
# 	# 	con.close()
# 	return render_template('files.html', name=assignments[name], comments=commentList)

if __name__ == '__main__':
	app.run()
