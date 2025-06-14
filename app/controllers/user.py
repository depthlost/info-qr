
import io
import qrcode
from flask import render_template, abort, url_for, send_file
from app.models import User

def sign_up():
    return render_template("create_user.html")

def create_user():
    pass

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