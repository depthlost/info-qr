
import io
import qrcode
from flask import render_template, abort, url_for, send_file, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import User
from app.forms import SignUpForm

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

    return redirect(url_for("show_user", user_id=user.id))

def sign_in():
    pass

def authenticate():
    pass

def sign_out():
    pass

def show_user(user_id):
    user = User.get(user_id)

    if not user:
        abort(404)
    
    return render_template("show_user.html", user=user)

def edit_user(user_id):
    pass

def update_user(user_id):
    pass

def get_user_qrcode(user_id):
    data = url_for(endpoint="show_user", user_id=user_id, _external=True)
    
    qr_code = qrcode.QRCode(version=1, box_size=10, border=4)
    qr_code.add_data(data)
    qr_code.make(fit=True)
    image = qr_code.make_image(fill_color="black", back_color="white")

    buffer = io.BytesIO()
    image.save(buffer, format="PNG")
    buffer.seek(0)

    return send_file(buffer, mimetype='image/png')