import os
from flask import Flask, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/ubuntu'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
from flask import send_from_directory

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if ('file' not in request.files) or ('style' not in request.files):
            flash('No file part')
            return redirect(request.url)
        stylefile = request.files['style']
        imagefile= request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if stylefile.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if stylefile and allowed_file(stylefile.filename):
            filename = secure_filename(stylefile.filename)
            stylefile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
   <body style="background-color:white;">
    <center><img src="/static/title.png"></center><br><br>
    
    <center><form method=post enctype=multipart/form-data>
    <font size="5"><center> Introduce a picture </center> </font>

    <p><input type=file name=file>
    <font size="5"><center> Introduce a style </center> </font>

      <p><input type=file name=style><br><br><br>
         <input type=submit value='Upload both pictures'>
    </form></center>
    </body>
    '''
