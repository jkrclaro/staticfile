from flask import (
    Blueprint,
    request,
    redirect,
    render_template,
    url_for,
    current_app,
    session,
    flash
)
from flask_login import login_user, logout_user, login_required, current_user

from src import token, google_recaptcha
from src.channelry.models import db
from src.channelry.models.auth import User
from src.channelry.forms.auth import (
    SignupForm,
    LoginForm,
    ForgotPasswordForm,
    ResetPasswordForm,
    ConfirmForm
)
from src.channelry import helper


auth_bp = Blueprint('auth', __name__)


def validate_recaptcha():
    recaptcha = {'site_key': google_recaptcha.site_key}
    if request.method == 'POST':
        recaptcha_response = request.form.get('g-recaptcha-response')
        if recaptcha_response:
            data = {
                'response': recaptcha_response,
                'remoteip': request.remote_addr
            }
            recaptcha['recaptcha'] = google_recaptcha.verify(data)
        else:
            recaptcha['recaptcha'] = 'Please complete the CAPTCHA.'
    return recaptcha


@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    recaptcha = validate_recaptcha()
    form = SignupForm()
    if form.validate_on_submit() and not recaptcha.get('recaptcha'):
        email = form.email.data
        password = form.password.data
        name = form.name.data
        user = User(email, password, name=name)
        user_exist = User.query.filter_by(email=email).first()
        if user_exist:
            form.email.errors = ['Email is already taken']
        else:
            db.session.add(user)
            db.session.commit()
            helper.email_confirmation()
            login_user(user)
            return redirect(url_for('dashboard.index'))
    return render_template('auth/signup.html', form=form, **recaptcha)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    recaptcha = {}
    if session.get('attempt'):
        recaptcha = {'site_key': google_recaptcha.site_key}
        g_recaptcha_response = request.form.get('g-recaptcha-response')
        if request.method == 'POST':
            if not g_recaptcha_response:
                recaptcha['recaptcha'] = 'Please complete the CAPTCHA ' \
                                        'to complete your login.'
            else:
                data = {
                    'response': g_recaptcha_response,
                    'remoteip': request.remote_addr
                }
                recaptcha['recaptcha'] = google_recaptcha.verify(data)
    form = LoginForm(request.form)
    if form.validate_on_submit() and not recaptcha.get('recaptcha'):
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if not user or not user.password_match(password):
            form.email.errors = ['Wrong email or password']
            session['attempt'] = True
            recaptcha = {'site_key': google_recaptcha.site_key}
        else:
            session.pop('attempt', None)
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard.index'))

    return render_template('auth/login.html', form=form, **recaptcha)


@auth_bp.route('/logout')
def logout():
    logout_user()
    session.pop('resend', None)
    return redirect(url_for('home.index'))


@auth_bp.route('/confirm', methods=['GET', 'POST'])
def confirm():
    logout_user()
    template = 'auth/confirm.html'
    confirm_token = request.args.get('t', '')
    token_decrypted = token.decrypt(confirm_token)
    if not confirm_token and not token_decrypted:
        return render_template(template)

    form = ConfirmForm()

    old_email = token_decrypted.get('old_email')
    new_email = token_decrypted.get('new_email')
    email = token_decrypted.get('email')
    form.email.data = new_email if new_email else email
    if form.validate_on_submit():
        password = form.password.data
        email = old_email if old_email else email
        user = User.query.filter_by(email=email).first()
        current_app.logger.debug(user)
        if not user or not user.password_match(password):
            form.password.errors = ['Wrong password.']
        else:
            if new_email:
                user.email = new_email
            user.is_confirmed = True
            db.session.add(user)
            db.session.commit()
            login_user(user)

            if new_email and old_email:
                helper.email_change_email_success(email)
                flash('Your email address was successfully changed', 'success')
            else:
                flash('Your email address have been confirmed', 'success')
            return redirect(url_for('dashboard.index'))
    return render_template(template, form=form)


@auth_bp.route('/email/resend')
@login_required
def resend():
    # TODO: Should be a post
    helper.email_confirmation()
    session['resend'] = True
    return redirect(url_for('dashboard.index'))


@auth_bp.route('/forgot', methods=['GET', 'POST'])
def forgot():
    template = 'auth/forgot.html'
    recaptcha = validate_recaptcha()
    form = ForgotPasswordForm()
    if form.validate_on_submit() and not recaptcha.get('recaptcha'):
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        if user:
            helper.email_reset()
        return render_template(template)
    return render_template(template, form=form, **recaptcha)


@auth_bp.route('/reset', methods=['GET', 'POST'])
def reset():
    logout_user()

    template = 'auth/reset.html'
    reset_token = request.args.get('t', '')
    if not reset_token and not token.decrypt(reset_token):
        return render_template('auth/reset.html')

    form = ResetPasswordForm()
    if form.validate_on_submit():
        reset_token_in_form = request.form.get('reset_token')
        token_decrypted = token.decrypt(reset_token_in_form)
        if not token_decrypted:
            render_template(template)

        email = token_decrypted.get('email')
        user = User.query.filter_by(email=email).first()
        password_hashed = user.password_hash(form.password.data)
        user.password = password_hashed.decode('utf8')
        db.session.add(user)
        db.session.commit()
        helper.email_reset_success()
        login_user(user)
        flash('Successfully changed your Channelry password', 'success')
        return redirect(url_for('dashboard.index'))

    return render_template(template, form=form, reset_token=reset_token)


@auth_bp.route('/settings')
def settings():
    return render_template('auth/settings.html')


@auth_bp.route('/billing')
def billing():
    return render_template('auth/billing.html')