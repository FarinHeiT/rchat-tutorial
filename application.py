from flask import Flask, render_template, redirect, url_for


from wtform_fields import *
from models import *

# Configure app
app = Flask(__name__)
app.secret_key = 'topsecret'


# Configure DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://hpxyudbuipqkzx:407174d5c63e42b31a1800a0cdbe7e0fcbbfdd97b88f695c571219eb41cd6461@ec2-54-83-201-84.compute-1.amazonaws.com:5432/d80tqsaa7a8g17'
db = SQLAlchemy(app)


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

		return redirect(url_for('login'))

	return render_template('index.html', form=reg_form)


@app.route('/login', methods=('GET', 'POST'))
def login():

	login_form = LoginForm()

	# Allow login if validation was successful
	if login_form.validate_on_submit():
		return "Logged in"


	return render_template('login.html', form=login_form)


if __name__ == '__main__':
	app.run(debug=True)