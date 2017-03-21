from flask import Flask, render_template, request, url_for, redirect, send_from_directory
from werkzeug import secure_filename
import os
from visual import visioning
app = Flask(__name__)

UPLOAD_FOLDER = './tempaudio'
IMAGE_FOLDER = "./static/picture"
app.config['UPLOAD_FOLDER']= UPLOAD_FOLDER
app.config['IMAGE_FOLDER']= IMAGE_FOLDER

@app.route('/upload', methods = ['GET', 'POST'])
def upload_file():
  if request.method == 'POST':
      f = request.files['file']
      filename = secure_filename(f.filename)
      global artpiece
      artpiece = request.form['artpiece']
      f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      imfile = os.path.join(app.config['IMAGE_FOLDER'], artpiece + ".png")
      visioning(filename, artpiece)
      
      ## deletes music file, since this should only be temporary
      os.remove(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      return render_template('image.html', name=artpiece, piece= imfile)
  else:
      return render_template('upload.html')

@app.route('/')
def index():
    return redirect(url_for('upload_file'))

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/gallery')
def gallery():
    return render_template('gallery.html')

if __name__ == "__main__":
    app.run(debug=True)
