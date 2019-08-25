from flask import Flask, render_template

from wtform_fields import *

# COnfigure app
app = Flask(__name__)
app.secret_key = 'topsecret'


@app.route('/', methods=('GET', 'POST'))
def index():

	reg_form = RegistrationForm()

	if reg_form.validate_on_submit():
		print('great')

	return render_template('index.html', form=reg_form)

if __name__ == '__main__':
	app.run(debug=True)