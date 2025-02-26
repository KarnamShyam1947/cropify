from flask import Blueprint, render_template, redirect, request, url_for, flash, session
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from Forms import ForgotPasswordForm, LoginForm, RegisterForm, SetPasswordForm
from App import bcrypt, db, mail, app
from flask_mail import  Message
from Models import *
import threading

auth = Blueprint('auth', __name__)

tokenizer = URLSafeTimedSerializer('this-is-secret')

@auth.route('/login', methods = ['GET', 'POST'])
def login():    
    form = LoginForm()

    if form.validate_on_submit():
        email = form.username.data
        password = form.password.data
        
        user = UserModel.query.filter_by(email = email).first()

        if user is None :
            flash("invalid email or password", "danger")
            return redirect(url_for('auth.login'))
        
        hashed_password = user.password
        if not bcrypt.check_password_hash(hashed_password, password):
            flash("invalid email or password", "danger")
            return redirect(url_for('auth.login'))
        
        if user.isVerified == 0:
            token = tokenizer.dumps(email)
            link = url_for('auth.activate', token=token, _external=True)

            print(link)
            threading.Thread(target=send_activation_mail, args=(user, link, )).start()
            flash(f"Your email is not verified. Please check your inbox", "danger")
            return redirect(url_for('auth.login'))
        
        else:
            # set session
            session['name'] = user.name
            session['id'] = user.id
            return redirect(url_for('main.index'))

    return render_template('auth/login.html', form=form)

@auth.route('/register', methods = ['GET', 'POST'])
def register():

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        password1 = form.password1.data

        if password != password1:
            flash("danger : passwords didn't match", 'danger')
            return redirect(url_for('auth.register'))
        
        user = UserModel.query.filter_by(email = email).first()
        if user is not None:
            flash("danger : email already in use", 'danger')
            return redirect(url_for('auth.register'))
        
        new_user = UserModel(name = username, email = email, password = bcrypt.generate_password_hash(password), isVerified=0, role="farmer")
        db.session.add(new_user)
        db.session.commit()

        token = tokenizer.dumps(email)
        link = url_for('auth.activate', token=token, _external=True)

        print(link)
        threading.Thread(target=send_activation_mail, args=(new_user, link, )).start()

        flash("Account created successfully. Don't forgot to activation it", "success")
        return redirect(url_for('auth.login'))

    
    return render_template('auth/register.html', form=form)

@auth.route('/activate/<token>')
def activate(token):
    try:
        email = tokenizer.loads(token, 3600)

        user = UserModel.query.filter_by(email = email).first()

        if user is None :
            flash("invalid token", "danger")
            return redirect(url_for('auth.login')) 
        
        else:
            user.isVerified = 1
            db.session.add(user)
            db.session.commit()

            flash("verified successfully", "success")
            return redirect(url_for('auth.login'))
        
    except SignatureExpired:
        flash("Link expired", "danger")
        return redirect(url_for('auth.login')) 
    
    except BadSignature:
        flash("Invalid link", "danger")
        return redirect(url_for('auth.login')) 

@auth.route('/logout')
def logout():
    session.pop('name', None)
    session.pop('id', None)
    return redirect(url_for('main.index'))

@auth.route('/forgot-password', methods = ['GET', 'POST'])
def forgot_password():
    form = ForgotPasswordForm()

    if form.validate_on_submit():
        email = form.email.data

        user = UserModel.query.filter_by(email = email).first()

        if user is None:
            flash("Email not registered.....!!!", "danger")
            return redirect(url_for('auth.forgot_password'))
        
        else:
            token = tokenizer.dumps(email)
            link = url_for('auth.validate_token', token=token, _external=True)
            print(f"\n{link}\n")

            threading.Thread(target=send_password_reset_mail, args=(user, link, )).start()

            flash("Check your inbox for password reset link", "danger")
            return redirect(url_for('auth.forgot_password'))

    return render_template('auth/forgot-password.html', form=form)

@auth.route('/validate-token/<token>')
def validate_token(token):
    try:
        email = tokenizer.loads(token, 3600)

        user = UserModel.query.filter_by(email = email).first()

        if user is None :
            flash("invalid url", "danger")
            return redirect(url_for('auth.login')) 
        
        else:
            session['forgot_password_email'] = email
            return redirect(url_for('auth.set_password'))
        
    except SignatureExpired:
        flash("Link expired", "danger")
        return redirect(url_for('auth.login')) 
    
    except BadSignature:
        flash("Invalid link", "danger")
        return redirect(url_for('auth.login')) 

@auth.route('/set-password', methods = ['GET', 'POST'])
def set_password():
    form = SetPasswordForm()
    if 'forgot_password_email' not in session:
        flash("403 : forbidden", "danger")
        return redirect(url_for('auth.login'))
    
    else:
        if form.validate_on_submit():
            password1 = form.password.data

            email = session['forgot_password_email']
            user = UserModel.query.filter_by(email = email).first()

            user.password = bcrypt.generate_password_hash(password1)

            db.session.add(user)
            db.session.commit()

            flash("password changed successfully.....!!!", "success")

            session.pop('forgot_password_email', None)

            return redirect(url_for("auth.login"))

        return render_template('auth/set-password.html', form = form)

@auth.route('/change-password', methods = ['GET', 'POST'])
def change_password():

    if 'user_email' not in session:
        flash("403 : forbidden", "danger")
        return redirect(url_for('auth.login'))

    email = session.get('user_email')
    
    if request.method == 'POST':
        current_user = UserModel.query.filter_by(email=email).first()

        old_password = request.form.get("old_password")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        current_password = current_user.password
        if not bcrypt.check_password_hash(current_password, old_password):
            flash("Old password doesn\'t match.....!!!", "danger")
            return redirect(url_for("auth.change_password"))
        
        if password1 != password2:
            flash("conform password doesn\'t match", "danger")
            return redirect(url_for("auth.change_password"))
        
        else:
            current_user.password = bcrypt.generate_password_hash(password1)

            db.session.add(current_user)
            db.session.commit()

            flash("Password changed successfully", "success")
            return redirect(url_for("auth.change_password"))

    return render_template('auth/change-password.html')

def send_activation_mail(user, link):
    with app.app_context():
        print('started..........')
        msg = Message('Activate your account', recipients=[user.email, ], sender='ecsgps.project@gmail.com')

        msg.html = render_template('email/active.html', name=user.name, link=link)

        mail.send(msg)

        print("Send successfully.........")

def send_password_reset_mail(user, link):
    with app.app_context():
        print('started..........')
        msg = Message('Password Reset link', recipients=[user.email, ], sender='ecsgps.project@gmail.com')

        msg.html = render_template('email/forgot-password.html', name=user.name, link=link)

        mail.send(msg)

        print("Send successfully.........")
