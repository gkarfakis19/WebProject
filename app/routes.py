from flask import render_template, flash, redirect, url_for, send_file, request, send_from_directory, make_response
from werkzeug.exceptions import abort

from app import app, photos
from app.forms import ImageSelectorForm,ImageSelectorUploadForm
from app.imageprocess_generator import imageencode
from app.imagedecode_generator import imagedecode
from app.filehandler import image_flush

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'George K'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Test!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'Test 2!'
        }
    ]
    return render_template('index.html', title='Home', user=user, active_home="active")

@app.route('/imageprocess', methods=['GET', 'POST'])
def imageprocess():
    form = ImageSelectorForm()
    string_seed=form.message_key.data
    if request.method == "POST":
        if request.data==b'' and form.image_used.data=="custom":
            return render_template('imageprocess.html', title='Image Process', form=form, active_imageprocess="active")
        if 'photo_upload' in request.files and form.image_used.data=="custom":
            filename = photos.save(request.files['photo_upload'])
            imageencode(form.message_key.data,form.message_terminator.data,"Uploads/"+filename,form.message.data)
            return render_template('imageprocess.html', title='Image Process', form=form, active_imageprocess="active",image=("static/encodedsamples/encodedsample" + str(ord(string_seed[0])) + ".png"))
        imageencode(form.message_key.data,form.message_terminator.data,"sample.png",form.message.data)
        return render_template('imageprocess.html', title='Image Process', form=form,active_imageprocess="active", image=("static/encodedsamples/encodedsample"+str(ord(string_seed[0]))+".png"))
    image_flush("app/static/encodedsamples/*")
    return render_template('imageprocess.html', title='Image Process', form=form, active_imageprocess="active")


@app.route('/imagedecode',methods=['GET','POST'])
def imagedecrypter():
    form=ImageSelectorUploadForm()
    if request.method == 'POST' and 'photo_upload' in request.files: #if image uploaded
        filename = photos.save(request.files['photo_upload'])
        result, decode_content=imagedecode(form.message_key.data,"app/static/Uploads/"+filename)
        if result==-1:
            decode_content="Decryption unsuccessful."
        else:
            decode_content="Decryption successful: \n"+decode_content
        decode_content = decode_content.split("\n")
        image_flush("app/static/Uploads/*", None)
        return render_template('imageprocess.html', title='Image Decoded', form=form, active_imagedecode="active", text=decode_content)
    return render_template('imageprocess.html', title='Image Decode',form=form, active_imagedecode="active", upload="yes")


@app.route('/api/encode',methods=['POST'])
def api_encode_handler():
    if "message" not in request.args:
        abort(403)
    elif "key" not in request.args:
        abort(403)
    terminator=True
    if request.args.get("terminate")=="false":
        terminator=False
    imageencode(request.args.get("key"), terminator, "sample.png",request.args.get("message"))
    return send_from_directory("static/encodedsamples","encodedsample"+str(ord(request.args.get("key")[0]))+".png")

@app.route('/api/decode',methods=['POST'])
def api_decode_handler():
    if "key" not in request.args:
        abort(403)
    if 'photo_upload' in request.files:
        filename = photos.save(request.files['photo_upload'])
        result, decode_content =imagedecode(request.args.get("key"),"app/static/Uploads/"+filename)
        if result==-1:
            decode_content="Decryption unsuccessful."
        else:
            f=open("DecodedMessage.txt", "r")
            decode_content="Decryption successful: \n"+decode_content
        image_flush("app/static/Uploads/*", None)
        return make_response(decode_content)
    else:
        abort(403)
