
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user, login_required
from app import app
from app.forms import SignUpForm, LogInForm, AddressForm 
from app.models import User, Sign 



@app.route('/')
def index():
    return render_template('index.html')


@app.route('/snapshot')
@login_required
def snapshot():
    users=User.query.order_by(User.date_created.desc()).all()
    return render_template ('snapshot.html', users = users)

@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        print('Sign Up has been created!')
        # Get data from form
        email = form.email.data
        username = form.username.data
        password = form.password.data
        print(email, username, password)
        # Check to see if we have a user with username and/or password:
        check_sign = Sign.query.filter( (Sign.username == username) | (Sign.email == email) ).first()
        if check_sign is not None:
            flash('User with username and/or email already exists', 'danger')
            return redirect(url_for('signup'))
        # Add a new user to the database
        new_sign = Sign(email=email, username=username, password=password)
        # Flash a success message
        flash(f"{new_sign} has successfully signed up!", "success")
        # Redirect back to home
        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LogInForm()
    if form.validate_on_submit():
        # Get the form data
        username = form.username.data
        password = form.password.data
        # Check to see if there is a user with that username and password
        sign = Sign.query.filter_by(username=username).first()
        if sign is not None and sign.check_password(password):
            # log the user in
            login_user(sign)
            flash(f"{sign} is now logged in.", 'primary')
            return redirect(url_for('directory'))
        else:
            flash('Incorrect username and/or password. Please try again.', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('index'))

@app.route('/directory', methods=['GET','POST'])
@login_required
def directory():
    form = AddressForm()
    if form.validate_on_submit():
        print('Hooray your phone number has been registered!')
        # Get data from form
        first = form.first.data
        last = form.last.data
        phone = form.phone.data
        address = form.address.data
        print(first, last, phone, address)
        # Add a new user to the database
        new_user = User(first=first, last=last, phone=phone, address=address, sign_id = current_user.id)
        # Flash a success message
        flash("You have successfuly signed up!", "success")
        # Redirect back to home
        return redirect(url_for('index'))
    return render_template('phonebook.html', form=form)

@app.route('/snapshot/<user_id>')
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        flash(f"Post with id #{user_id} does not exist", "warning")
        return redirect(url_for('index'))
    return render_template('snapshot.html', user=user)


@app.route('/snapshot/<user_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_user(user_id):
    user = User.query.get(user_id)
    if not user:
        flash(f"Post with id #{user_id} does not exist", "warning")
        return redirect(url_for('index'))
    if user.author != current_user:
        flash('You do not have permission to edit this post', 'danger')
        return redirect(url_for('index'))
    form = AddressForm()
    if form.validate_on_submit():
        # Get the form data
        new_first = form.first.data
        new_last = form.last.data
        new_phone = form.phone.data
        new_address = form.address.data
        # update the post
        user.update(first=new_first, last=new_last, phone=new_phone, address=new_address, )
        flash(f"{user.title} has been updated", "success")
        return redirect(url_for('get_user', user_id=user.id))
    return render_template('editbook.html', user=user, form=form)


@app.route('/snapshot/<user_id>/delete')
@login_required
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        flash(f"Post with id #{user_id} does not exist", "warning")
        return redirect(url_for('index'))
    if user.author != current_user:
        flash('You do not have permission to delete this post', 'danger')
        return redirect(url_for('index'))
    user.delete()
    flash(f"{user.phone} has been deleted", 'info')
    return redirect(url_for('index'))