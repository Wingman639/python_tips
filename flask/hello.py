from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

# @app.route('/hello')
# def hello():
#     return 'Hello, World'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/projects/')
def projects():
    return 'The project page'

@app.route('/about')
def about():
    return 'The about page'


from flask import request

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return 'do_the_login()'
    else:
        return 'show_the_login_form()'


from flask import render_template
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello_template.html', name=name)


from flask import abort, redirect, url_for
@app.route('/toberedi')
def to_be_redirect():
    return redirect(url_for('redirect_dist'))

@app.route('/redirectdist')
def redirect_dist():
    return 'redirect to new page'

@app.errorhandler(404)
def not_found(error):
    return render_template('error_template.html'), 404


from flask import session
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
@app.route('/remember/<name>')
def remember(name=None):
    session['his_name'] = name
    return render_template('hello_template.html', name=name)

@app.route('/tell')
def tell():
    return 'Your name is {name}'.format(name=session['his_name'])

app.logger.debug('A value for debugging')
app.logger.warning('A warning occurred (%d apples)', 42)
app.logger.error('An error occurred')

'''
Linux
$ export FLASK_APP=hello.py
$ flask run
 * Running on http://127.0.0.1:5000/

 $ export FLASK_APP=hello.py
$ python -m flask run
 * Running on http://127.0.0.1:5000/

Windows
SET FLASK_APP=hello.py
flask run
 * Serving Flask app "hello"
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
'''