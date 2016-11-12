from flask import Flask, request, render_template, url_for
import sqlite3

app = Flask(__name__)

assignments = {}

@app.context_processor
def inject_static():
    return dict(css_url=url_for('static', filename='styles.css'),
                js_url=url_for('static', filename='index.js'),
                title="the bourne interface")

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
