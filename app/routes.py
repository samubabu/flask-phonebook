from crypt import methods
from flask import render_template, redirect, url_for, flash
from app import app
from app.forms import SignUpForm
from app.models import User



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/directory', methods=['GET','POST'])
def directory():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Hooray your phone number has been registered!')
        # Get data from form
        first = form.first.data
        last = form.last.data
        phone = form.phone.data
        address = form.address.data
        print(first, last, phone, address)
        # Add a new user to the database
        new_user = User(first=first, last=last, phone=phone, address=address)
        # Flash a success message
        flash("You have successfuly signed up!", "success")
        # Redirect back to home
        return redirect(url_for('index'))
    return render_template('phonebook.html', form=form)