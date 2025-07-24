
import io
import qrcode
from flask import current_app, render_template, abort, url_for, send_file, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.forms import SignUpForm, SignInForm
from app.session import get_authenticated_user_id, get_authenticated_user, login_user, logout_user

def sign_up():
    return render_template("sign_up.html", form=SignUpForm())

def create_user():
    form = SignUpForm()

    if not form.validate_on_submit():
        return render_template("sign_up.html", form=form)

    user = User(
        name=form.name.data,
        surname=form.surname.data,
        email=form.email.data,
        password=generate_password_hash(form.password.data)
    )
    user.create()
    
    login_user(user)

    return redirect(url_for("home_user", user_id=user.id))

def sign_in():
    user = get_authenticated_user()

    if user:
        return redirect(url_for("home_user", user_id=user.id))
    
    return render_template("sign_in.html", form=SignInForm())

def authenticate():
    form = SignInForm()

    if form.validate_on_submit():
        user = User.get_by_email(form.email.data)

        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for("home_user", user_id=user.id))
        
        auth_error = True
    else:
        auth_error = False
    
    return render_template("sign_in.html", form=form, auth_error=auth_error)

def sign_out():
    logout_user()
    
    return redirect(url_for("main"))

def home_user(user_id):
    user = User.get(user_id)

    if not user:
        abort(404)
    elif user.id != get_authenticated_user_id():
        return redirect(url_for("show_user", user_id=user.id))

    return render_template("home_user.html", user=user)

def show_user(user_id):
    user = User.get(user_id)

    if not user:
        abort(404)
    
    return render_template("show_user_info.html", user=user, is_owner_user=user.id == get_authenticated_user_id())

def get_user_qrcode(user_id):
    data = current_app.config["BASE_URL"] + url_for(endpoint="show_user", user_id=user_id)
    
    qr_code = qrcode.QRCode(version=1, box_size=10, border=4)
    qr_code.add_data(data)
    qr_code.make(fit=True)
    image = qr_code.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png')