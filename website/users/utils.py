import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_filenname = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/profile_pics', picture_filenname)
    picture_size = (125, 125)
    i = Image.open(form_picture)
    image = i.resize(picture_size, Image.ANTIALIAS)
    left = (image.width - picture_size[0]) // 2
    upper = (image.height - picture_size[1]) // 2
    right = left + picture_size[0]
    lower = upper + picture_size[1]
    box = (left, upper, right, lower)
    cropped_image = image.crop(box)
    cropped_image.save(picture_path)

    return picture_filenname

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Reset Password Link',
                  sender = 'william.peterson@entegritypartners.com',
                  recipients = [user.email])
    msg.body = f"""
To reset your password, visit the following link.
{url_for('users.reset_token', token = token, _external = True)}

If you did not request this password reset, please ignore this email and no changes will be made.
"""
    #mail.send(msg)

    