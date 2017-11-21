import os
from flask import Flask, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/home/ubuntu'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key = "super secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


from flask import send_from_directory
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

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
        if stylefile and allowed_file(stylefile.filename) and imagefile and allowed_file(imagefile.filename):
            stylename = secure_filename(stylefile.filename)
            imagename= secure_filename(imagefile.filename)
            stylefile.save(os.path.join(app.config['UPLOAD_FOLDER'], stylename))
            imagefile.save(os.path.join(app.config['UPLOAD_FOLDER'], imagename))
            pathstyle=UPLOAD_FOLDER+"/"+stylename
            pathimage=UPLOAD_FOLDER+"/"+imagename
            dir_path = os.path.dirname(os.path.realpath(__file__))
            flash("Your image will be ready very soon! Wait a bit...")
            os.system("python3 "+ dir_path+"/ArtGenerator.py "+pathimage+ " " + pathstyle)
            
            return redirect(url_for('uploaded_file', filename="generated_image.jpg"))
    return '''
    <!doctype html>
    <title>Upload new File</title>

    <center><img src="/static/title.png"></center><br><br>
    
    <center><form method=post enctype=multipart/form-data>
    <font size="5"><center> Introduce a picture </center> </font>
    <p><input type=file name=file>
    <font size="5"><center> Introduce a style </center> </font>

      <p><input type=file name=style><br><br><br>
         <input type=submit value='Create art!'>
    </form></center>
    </body>
    '''
