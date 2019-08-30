from time import localtime, strftime
from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_login import LoginManager, login_user, current_user, login_required, logout_user
from flask_socketio import SocketIO, send, emit, join_room, leave_room


from wtform_fields import *
from models import *

# Configure app
app = Flask(__name__)
app.secret_key = 'topsecret'


# Configure DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hpxyudbuipqkzx:407174d5c63e42b31a1800a0cdbe7e0fcbbfdd97b88f695c571219eb41cd6461@ec2-54-83-201-84.compute-1.amazonaws.com:5432/d80tqsaa7a8g17'
db = SQLAlchemy(app)


# Initialize Flask-SocketIO
# ping_timeout - timeout begore for triggering disconnect event
# ping_interval - inteval between pinging with server
socketio = SocketIO(app, ping_timeout=5, ping_interval=2)

ROOMS = [
	'lounge',
	'news',
	'games',
	'coding'
]

USERS = {}

# Configure flask login
login = LoginManager(app)
login.init_app(app)

@login.user_loader
def load_user(id):
	return User.query.get(int(id))


@app.route('/', methods=('GET', 'POST'))
def index():

	reg_form = RegistrationForm()

	# Update DB if validation was successful
	if reg_form.validate_on_submit():
		username = reg_form.username.data
		password = reg_form.password.data

		# Password hash
		hashed_pswd = pbkdf2_sha256.hash(password)

		user = User(username=username, password=hashed_pswd)
		db.session.add(user)
		db.session.commit()

		flash('Registered successfully, please login.')
		return redirect(url_for('login'))

	return render_template('index.html', form=reg_form)


@app.route('/login', methods=('GET', 'POST'))
def login():

	login_form = LoginForm()

	# Allow login if validation was successful
	if login_form.validate_on_submit():
		user_object = User.query.filter_by(username=login_form.username.data).first()
		login_user(user_object)
		
		return redirect(url_for('chat'))


	return render_template('login.html', form=login_form)


@app.route('/chat', methods=('GET', 'POST'))
def chat():
	# if not current_user.is_authenticated:
	# 	flash('Please login.', 'danger')
	# 	return redirect(url_for('login'))
	return render_template('chat.html', username=current_user.username, rooms=ROOMS)


@app.route('/logout', methods=['GET'])
def logout():
	logout_user()

	# Second argument - category
	flash('You have logged out successfully', 'succes')

	return redirect(url_for('login'))


@app.route('/rooms_info')
def rooms_info():
	'''  Info about users for dev purposes only '''
	return jsonify(USERS)

@app.route('/room_users')
def room_users():
	''' Returns JSON with list of users in each room '''
	result = {}
	for room in ROOMS:
		result[room] = dict([user for user in USERS.items() if user[1]['room'] == room])
	return jsonify(result)


@socketio.on('message')
def message(data):
	print(f'\n\n\n{data}\n\n\n')
	send({'msg': data['msg'],
		  'username': data['username'],
		  'time_stamp': strftime('%b-%d %I:%M%p', localtime()),
		}, room=data['room'])


@socketio.on('join')
def join(data):

	USERS[request.sid] = {'username': data['username'],
						  'room': data['room'].lower()}
	join_room(data['room'])
	send({'msg': data['username'] + " has joined the " + data['room']}, room=data['room'])


@socketio.on('leave')
def leave(data):
	USERS.pop(request.sid)
	leave_room(data['room'])
	send({'msg': data['username'] + " has left the " + data['room']}, room=data['room'])


@socketio.on('disconnect')
def disconnect():
	print('disconnecting')
	USERS.pop(request.sid)


if __name__ == '__main__':
	socketio.run(app, debug=True)