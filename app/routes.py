from flask import render_template, flash, redirect, url_for,send_file
from app import app
from app.forms import LoginForm,ImageSelectorForm
from app.imageprocess import imageencode
from app.filehandler import image_flush
import os

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Plasmidon'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user,posts=posts, active_home="active")

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         flash(f'Login requested for user {form.username.data}, remember_me={form.remember_me.data}')
#         return redirect(url_for('index'))
#     return render_template('login.html', title='Sign In', form=form)


@app.route('/imageprocess', methods=['GET', 'POST'])
def imageprocess():
    form = ImageSelectorForm()
    if form.validate_on_submit():
        f=open("Message.txt","w+")
        f.write(form.message.data)
        f.close()
        imageencode(form.message_key.data,form.message_terminator.data,"sample.png")
        #image_flush("app/static/encodedsamples/*","app/static/encodedsamples/encodedsample" + str(form.message_key.data) + ".png")
        return render_template('imageprocess.html', title='Image Process', form=form,active_imageprocess="active", image=("static/encodedsamples/encodedsample"+str(form.message_key.data)+".png"))
    image_flush("app/static/encodedsamples/*")
    return render_template('imageprocess.html', title='Image Process', form=form, active_imageprocess="active")
