from flask import Flask, render_template

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

	if reg_form.validate_on_submit():
		username = reg_form.username.data
		password = reg_form.password.data

		# Check username exists
		user_object = User.query.filter(username==username).first()
		if user_object:
			return 'username already taken :('

		user = User(username=username, password=password)
		db.session.add(user)
		db.session.commit()
		return 'Inserted into DB'

	return render_template('index.html', form=reg_form)

if __name__ == '__main__':
	app.run(debug=True)