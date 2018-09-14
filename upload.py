from flask import Flask, request, render_template, redirect, url_for, send_from_directory, session
import os
from werkzeug.utils import secure_filename
# from datetime import datetime

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


UPLOAD_FOLDER = './static/images'
ALLOWED_EXTENSIONS = set({'jpg', 'jpeg', 'png', 'gif'})
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = os.urandom(24)
# limit upload file sieze : 1MB
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024


def allowed_file(filename):
    # filename = re.search("(?<!\.)\w+", filename).group(0) + "." + 'jpg'
    return '.' in filename and \
        filename.rsplit(".", 1)[1] in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        img_file = request.files['img_file']
        if img_file and allowed_file(img_file.filename):
            filename = secure_filename(img_file.filename)
            img_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_url = '/images/' + filename
            return render_template('index.html', img_url=img_url)
        else:
            return '''<p>許可されていない拡張子です</p> '''
    else:
        return redirect(url_for('index'))


@app.route('/images/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOADED_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debag=True, host='0.0.0.0', port=5000)
